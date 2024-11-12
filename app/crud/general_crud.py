# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-06-20
"""
import pandas as pd
from sqlalchemy.orm import Session, aliased
from sqlalchemy import extract

import crud
import schemas
import models
import datetime as dt


def get_site_by_uid(db: Session, site_uid: int):
    return db.query(models.Site).filter(models.Site.site_uid == site_uid).first()


def get_site_by_code(db: Session, site_code: str):
    return db.query(models.Site).filter(models.Site.site_code == site_code).first()


def add_site(db: Session, site: schemas.SiteBase):
    new_site = models.Site(name=site.site_name,
                           code=site.site_code,
                           latitude=site.latitude,
                           longitude=site.longitude,
                           approach=site.approach,
                           region=site.region,
                           notes=site.notes)
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return new_site


def add_installation(db: Session, installation: schemas.InstallationBase):
    new_installation = models.Installation(installation_code=installation.installation_code,
                                           installation_name=installation.installation_name,
                                           installation_type=installation.installation_type,
                                           site_uid=installation.site_uid,
                                           latitude=installation.latitude,
                                           longitude=installation.longitude,
                                           notes=installation.notes,
                                           status=installation.status)
    db.add(new_installation)
    db.commit()
    db.refresh(new_installation)
    return new_installation


def get_installation_by_code(db: Session, installation_code: str):
    return db.query(models.Installation).filter(models.Installation.installation_code == installation_code).first()


def get_installation_by_uid(db: Session, installation_uid: int):
    return db.query(models.Installation).filter(models.Installation.installation_uid == installation_uid).first()


def get_installation_visit_by_date_and_code(db: Session, installation_uid: int, visit_date: dt.datetime):
    return db.query(models.InstallationVisit) \
        .filter((models.InstallationVisit.visit_date == visit_date)
                & (models.InstallationVisit.installation_uid == installation_uid)).first()


def add_installation_visit(db: Session, installation_visit: schemas.InstallationVisitBase):
    new_installation_visit = models.InstallationVisit(installation_uid=installation_visit.installation_uid,
                                                      roa=installation_visit.record_of_activities,
                                                      visit_dt=installation_visit.visit_date.replace(microsecond=0),
                                                      party=installation_visit.field_party,
                                                      notes=installation_visit.notes)
    db.add(new_installation_visit)
    db.commit()
    db.refresh(new_installation_visit)
    return new_installation_visit


def add_al_probe_measurement(db: Session, al_probe_measurement: schemas.ALProbeMeasurementBase):
    new_al_probe_measurement = models.ALProbeMeasurement(
        installation_visit_uid=al_probe_measurement.installation_visit_uid,
        probe_number=al_probe_measurement.probe_number,
        measurement=al_probe_measurement.measurement,
        probe_maxed=al_probe_measurement.probe_maxed)
    db.add(new_al_probe_measurement)
    db.commit()
    db.refresh(new_al_probe_measurement)
    return new_al_probe_measurement


def get_al_probe_measurement_by_installation_visit_uid_and_probe_number(db: Session, installation_visit_uid: int,
                                                                        probe_number: int):
    return db.query(models.ALProbeMeasurement). \
        filter((models.ALProbeMeasurement.installation_visit_uid == installation_visit_uid)
               & (models.ALProbeMeasurement.probe_number == probe_number)).first()


def get_logger_by_sn(db: Session, logger_sn: str):
    return db.query(models.Logger).filter(models.Logger.logger_serial_number == logger_sn).first()


def get_logger_by_uid(db: Session, logger_uid: int):
    return db.query(models.Logger).filter(models.Logger.logger_uid == logger_uid).first()


def get_logger_by_sn_and_type(db: Session, logger_sn: str, logger_type):
    return db.query(models.Logger).filter((models.Logger.logger_serial_number == logger_sn)
                                          & (models.Logger.logger_type == logger_type)).first()


def update_logger_type(db: Session, logger_uid: int, logger_type: str):
    db_logger = db.query(models.Logger).filter(models.Logger.logger_uid == logger_uid).first()
    db_logger.logger_type = logger_type
    db.commit()
    db.refresh(db_logger)
    return db_logger


def update_logger_battery_year(db: Session, logger_uid: int, battery_year: int):
    db_logger = db.query(models.Logger).filter(models.Logger.logger_uid == logger_uid).first()
    db_logger.battery_year = battery_year
    db.commit()
    db.refresh(db_logger)
    return db_logger


def add_logger(db: Session, logger: schemas.LoggerBase):
    new_logger = models.Logger(logger_serial_number=logger.logger_serial_number,
                               logger_type=logger.logger_type,
                               battery_year=logger.battery_year,
                               asset_tag=logger.asset_tag)
    db.add(new_logger)
    db.commit()
    db.refresh(new_logger)
    return new_logger


def get_most_recent_deployment_by_installation_and_logger_uid(db: Session, logger_uid: int, installation_uid: int):
    deployments = \
        db.query(models.LoggerDeployment).filter((models.LoggerDeployment.installation_uid == installation_uid)
                                                 & (models.LoggerDeployment.logger_uid == logger_uid)).all()
    most_recent_deployment = None
    most_recent_installation_visit = None
    most_recent_is_extraction = False
    for deployment in deployments:
        if deployment.deployment_visit_uid is None:
            db_iv = crud.get_installation_visit_by_uid(db=db, uid=deployment.extraction_visit_uid)
        else:
            db_iv = crud.get_installation_visit_by_uid(db=db, uid=deployment.deployment_visit_uid)
        visit_date = db_iv.visit_date
        if most_recent_installation_visit is None or visit_date > most_recent_installation_visit.visit_date:
            if deployment.deployment_visit_uid is None:
                most_recent_is_extraction = True
            most_recent_deployment = deployment
            most_recent_installation_visit = db_iv

        elif visit_date == most_recent_installation_visit.visit_date:
            if most_recent_is_extraction and deployment.deployment_visit_uid is not None:
                most_recent_is_extraction = False
                most_recent_deployment = deployment
                most_recent_installation_visit = db_iv
    return most_recent_deployment


def get_previous_unclosed_logger_deployment_at_installation(logger_uid: int, installation_uid: int,
                                                            visit_date: dt.datetime, return_closest: bool,
                                                            db: Session):
    deployments = db.query(models.LoggerDeployment.logger_deployment_uid,
                           models.LoggerDeployment.logger_uid,
                           models.LoggerDeployment.installation_uid,
                           models.LoggerDeployment.deployment_visit_uid,
                           models.InstallationVisit.visit_date) \
        .outerjoin(models.InstallationVisit,
                   models.LoggerDeployment.deployment_visit_uid == models.InstallationVisit.installation_visit_uid) \
        .filter((models.LoggerDeployment.installation_uid == installation_uid)
                & (models.LoggerDeployment.logger_uid == logger_uid)
                & (models.LoggerDeployment.extraction_visit_uid.is_(None))).all()
    deployments_df = pd.DataFrame(deployments, columns=["deployment_uid", "logger_uid", "installation_uid",
                                                        "deployment_visit_uid", "deployment_date"])

    if deployments_df.empty:
        return None
    elif len(deployments_df.index) == 1:
        deployment_uid = int(deployments_df.iloc[0]["deployment_uid"])
        return db.query(models.LoggerDeployment) \
            .filter(models.LoggerDeployment.logger_deployment_uid == deployment_uid).all()
    else:
        if return_closest:
            deployments_df["time_difference"] = visit_date - deployments_df["deployment_date"]
            closest_uid = deployments_df.loc[
                deployments_df["time_difference"] == deployments_df["time_difference"].min()]["deployment_uid"]
            return db.query(models.LoggerDeployment) \
                .filter(models.LoggerDeployment.logger_deployment_uid == closest_uid).all()

        else:
            deployment_uids = tuple(deployments_df["deployment_uid"])
            return db.query(models.LoggerDeployment) \
                .filter(models.LoggerDeployment.logger_deployment_uid.in_(deployment_uids)).all()


def get_installation_visit_by_uid(db: Session, uid: int):
    return db.query(models.InstallationVisit).filter(models.InstallationVisit.installation_visit_uid == uid).first()


def get_all_deployments_at_installation_uid(db: Session, installation_uid: int):
    return db.query(models.LoggerDeployment).filter(models.LoggerDeployment.installation_uid == installation_uid).all()


def add_logger_deployment(db: Session, logger_deployment: schemas.LoggerDeploymentBase):
    new_logger_deployment = models.LoggerDeployment(installation_uid=logger_deployment.installation_uid,
                                                    logger_uid=logger_deployment.logger_uid,
                                                    deployment_visit_uid=logger_deployment.deployment_visit_uid,
                                                    extraction_visit_uid=logger_deployment.extraction_visit_uid)
    db.add(new_logger_deployment)
    db.commit()
    db.refresh(new_logger_deployment)
    return new_logger_deployment


def close_logger_deployment(db: Session, logger_deployment_uid: int, installation_visit_uid: int):
    db_logger_deployment = crud.get_logger_deployment_by_uid(db=db, uid=logger_deployment_uid)
    db_logger_deployment.extraction_visit_uid = installation_visit_uid
    db.commit()
    db.refresh(db_logger_deployment)
    return db_logger_deployment


def get_logger_deployment_by_extraction_visit_uid(extraction_uid: int, db: Session):
    return db.query(models.LoggerDeployment) \
        .filter(models.LoggerDeployment.extraction_visit_uid == extraction_uid).first()


def get_logger_deployment_by_deployment_visit_uid(deployment_uid: int, db: Session):
    return db.query(models.LoggerDeployment) \
        .filter(models.LoggerDeployment.deployment_visit_uid == deployment_uid).first()


def get_logger_deployment_by_uid(uid: int, db: Session):
    return db.query(models.LoggerDeployment).filter(models.LoggerDeployment.logger_deployment_uid == uid).first()


def get_logger_download_by_uid(logger_download_uid: int, db: Session):
    return db.query(models.LoggerDownload) \
        .filter(models.LoggerDownload.logger_download_uid == logger_download_uid).first()


def get_logger_download_by_deployment_uid(deployment_uid: int, db: Session):
    return db.query(models.LoggerDownload).filter(models.LoggerDownload.logger_deployment_uid == deployment_uid).first()


def add_logger_download(logger_download: schemas.LoggerDownloadBase, db: Session):
    new_logger_download = models.LoggerDownload(logger_uid=logger_download.logger_uid,
                                                logger_deployment_uid=logger_download.logger_deployment_uid,
                                                download_date=logger_download.download_date.replace(microsecond=0),
                                                download_quality=logger_download.download_quality)
    db.add(new_logger_download)
    db.commit()
    db.refresh(new_logger_download)
    return new_logger_download


def get_logger_history_at_installation(installation_uid: int, db: Session):
    deployment_loggers = aliased(models.Logger)
    deployment_records = aliased(models.LoggerDeployment)
    extraction_loggers = aliased(models.Logger)
    extraction_records = aliased(models.LoggerDeployment)

    return db.query(models.InstallationVisit.installation_visit_uid,
                    models.InstallationVisit.visit_date,
                    models.InstallationVisit.field_party,
                    models.InstallationVisit.record_of_activities,
                    models.InstallationVisit.notes,
                    deployment_records.logger_uid.label("logger_deployed_uid"),
                    deployment_loggers.logger_serial_number.label("logger_deployed"),
                    deployment_loggers.logger_type.label("logger_deployed_type"),
                    extraction_records.logger_uid.label("logger_extracted_uid"),
                    extraction_loggers.logger_serial_number.label("logger_extracted"),
                    extraction_loggers.logger_type.label("logger_extracted_type")) \
        .outerjoin(deployment_records,
                   models.InstallationVisit.installation_visit_uid == deployment_records.deployment_visit_uid) \
        .outerjoin(deployment_loggers,
                   (models.InstallationVisit.installation_visit_uid == deployment_records.deployment_visit_uid)
                   & (deployment_records.logger_uid == deployment_loggers.logger_uid)) \
        .outerjoin(extraction_records,
                   models.InstallationVisit.installation_visit_uid == extraction_records.extraction_visit_uid) \
        .outerjoin(extraction_loggers,
                   (models.InstallationVisit.installation_visit_uid == extraction_records.extraction_visit_uid)
                   & (extraction_records.logger_uid == extraction_loggers.logger_uid)) \
        .filter(models.InstallationVisit.installation_uid == installation_uid).all()


def get_al_probe_history_at_installation(installation_uid: int, db: Session):
    return db.query(models.ALProbeMeasurement.probe_number,
                    models.ALProbeMeasurement.measurement,
                    models.ALProbeMeasurement.probe_maxed,
                    models.InstallationVisit.visit_date) \
        .join(models.InstallationVisit) \
        .filter(models.InstallationVisit.installation_uid == installation_uid).all()


def get_installations_at_site(site_uid: int, db: Session):
    return db.query(models.Installation).filter(models.Installation.site_uid == site_uid).all()


def get_all_installations_of_type(installation_type: str, db: Session):
    return db.query(models.Installation).filter(models.Installation.installation_type == installation_type).all()


def get_most_recent_installation_visit_at_installation(installation_uid: int, db: Session):
    installation_visits = db.query(models.InstallationVisit) \
        .filter(models.InstallationVisit.installation_uid == installation_uid).all()
    if installation_visits:
        data = pd.DataFrame([obj.__dict__ for obj in installation_visits])
        return installation_visits[data.index[data["visit_date"].argmax()]]
    return None


def get_all_installation_visits_in_year(year: int, db: Session):
    deployment_loggers = aliased(models.Logger)
    deployment_records = aliased(models.LoggerDeployment)
    extraction_loggers = aliased(models.Logger)
    extraction_records = aliased(models.LoggerDeployment)

    return db.query(models.InstallationVisit.field_party,
                    models.InstallationVisit.visit_date,
                    models.InstallationVisit.record_of_activities,
                    models.InstallationVisit.notes,
                    models.Installation.installation_name,
                    models.Installation.installation_code,
                    models.Installation.installation_type,
                    models.Installation.latitude,
                    models.Installation.longitude,
                    deployment_records.logger_uid.label("logger_deployed_uid"),
                    deployment_loggers.logger_serial_number.label("logger_deployed"),
                    deployment_loggers.logger_type.label("logger_type_deployed"),
                    deployment_loggers.battery_year.label("logger_deployed_battery_year"),
                    extraction_records.logger_uid.label("logger_extracted_uid"),
                    extraction_loggers.logger_serial_number.label("logger_extracted"),
                    extraction_loggers.logger_type.label("logger_type_extracted"),
                    models.Cable.connector_type,
                    models.StickUp.measurement.label("stick_up")) \
        .outerjoin(models.Installation,
                   models.InstallationVisit.installation_uid == models.Installation.installation_uid) \
        .outerjoin(deployment_records,
                   models.InstallationVisit.installation_visit_uid == deployment_records.deployment_visit_uid) \
        .outerjoin(deployment_loggers,
                   (models.InstallationVisit.installation_visit_uid == deployment_records.deployment_visit_uid)
                   & (deployment_records.logger_uid == deployment_loggers.logger_uid)) \
        .outerjoin(extraction_records,
                   models.InstallationVisit.installation_visit_uid == extraction_records.extraction_visit_uid) \
        .outerjoin(extraction_loggers,
                   (models.InstallationVisit.installation_visit_uid == extraction_records.extraction_visit_uid)
                   & (extraction_records.logger_uid == extraction_loggers.logger_uid)) \
        .outerjoin(models.Cable, models.InstallationVisit.installation_uid == models.Cable.installation_uid) \
        .outerjoin(models.StickUp,
                   models.InstallationVisit.installation_visit_uid == models.StickUp.installation_visit_uid) \
        .filter(extract('year', models.InstallationVisit.visit_date) == year).all()


def get_dump_for_region(region: str, db: Session):
    deployment_loggers = aliased(models.Logger)
    deployment_records = aliased(models.LoggerDeployment)
    extraction_loggers = aliased(models.Logger)
    extraction_records = aliased(models.LoggerDeployment)

    data = db.query(models.InstallationVisit.field_party,
                    models.InstallationVisit.visit_date,
                    models.InstallationVisit.record_of_activities,
                    models.InstallationVisit.notes,
                    models.Installation.installation_name,
                    models.Installation.installation_code,
                    models.Installation.installation_type,
                    models.Installation.latitude,
                    models.Installation.longitude,
                    deployment_records.logger_uid.label("logger_deployed_uid"),
                    deployment_loggers.logger_serial_number.label("logger_deployed"),
                    deployment_loggers.logger_type.label("logger_type_deployed"),
                    deployment_loggers.battery_year.label("logger_deployed_battery_year"),
                    extraction_records.logger_uid.label("logger_extracted_uid"),
                    extraction_loggers.logger_serial_number.label("logger_extracted"),
                    extraction_loggers.logger_type.label("logger_type_extracted"),
                    models.Cable.connector_type,
                    models.StickUp.measurement.label("stick_up"),
                    models.Site.region) \
        .outerjoin(models.Installation,
                   models.InstallationVisit.installation_uid == models.Installation.installation_uid) \
        .outerjoin(deployment_records,
                   models.InstallationVisit.installation_visit_uid == deployment_records.deployment_visit_uid) \
        .outerjoin(deployment_loggers,
                   (models.InstallationVisit.installation_visit_uid == deployment_records.deployment_visit_uid)
                   & (deployment_records.logger_uid == deployment_loggers.logger_uid)) \
        .outerjoin(extraction_records,
                   models.InstallationVisit.installation_visit_uid == extraction_records.extraction_visit_uid) \
        .outerjoin(extraction_loggers,
                   (models.InstallationVisit.installation_visit_uid == extraction_records.extraction_visit_uid)
                   & (extraction_records.logger_uid == extraction_loggers.logger_uid)) \
        .outerjoin(models.Cable, models.InstallationVisit.installation_uid == models.Cable.installation_uid) \
        .outerjoin(models.StickUp,
                   models.InstallationVisit.installation_visit_uid == models.StickUp.installation_visit_uid) \
        .outerjoin(models.Site,
                   (models.InstallationVisit.installation_uid == models.Installation.installation_uid)
                   & (models.Installation.site_uid == models.Site.site_uid)) \
        .filter(models.Site.region == region).all()

    data_df = pd.DataFrame(data,
                           columns=["recorded_by", "visit_date", "record_of_activities", "notes", "installation_name",
                                    "installation_code", "installation_type", "latitude", "longitude",
                                    "logger_deployed_uid", "logger_deployed", "logger_type_deployed",
                                    "logger_deployed_battery_year", "logger_extracted_uid", "logger_extracted",
                                    "logger_type_extracted", "connector_type", "stick_up", "region"])
    output_df = pd.DataFrame(columns=data_df.columns)
    for code in data_df["installation_code"].unique():
        subset = data_df.loc[data_df["installation_code"] == code]

        output_df.loc[len(output_df.index)] = subset.loc[subset["visit_date"] == subset["visit_date"].max()].iloc[0]
    return output_df


def get_readable_logger_deployments(logger_deployment_uid_list: list[int], db: Session):
    deployment_visits = aliased(models.InstallationVisit)
    extraction_visits = aliased(models.InstallationVisit)
    return db.query(models.LoggerDeployment.logger_deployment_uid,
                    models.Installation.installation_code,
                    models.Logger.logger_serial_number,
                    deployment_visits.visit_date.label("deployment_date"),
                    extraction_visits.visit_date.label("extraction_date"),
                    deployment_visits.record_of_activities.label("deployment_roa"),
                    deployment_visits.notes.label("deployment_notes")) \
        .outerjoin(models.Installation,
                   models.LoggerDeployment.installation_uid == models.Installation.installation_uid) \
        .outerjoin(models.Logger,
                   models.LoggerDeployment.logger_uid == models.Logger.logger_uid) \
        .outerjoin(deployment_visits,
                   models.LoggerDeployment.deployment_visit_uid == deployment_visits.installation_visit_uid) \
        .outerjoin(extraction_visits,
                   models.LoggerDeployment.extraction_visit_uid == extraction_visits.installation_visit_uid) \
        .filter(models.LoggerDeployment.logger_deployment_uid.in_(logger_deployment_uid_list)).all()


def edit_logger_in_deployment_record(logger_deployment_uid: int, new_logger_uid: int, db: Session):
    deployment = db.query(models.LoggerDeployment) \
        .filter(models.LoggerDeployment.logger_deployment_uid == logger_deployment_uid).first()
    deployment.logger_uid = new_logger_uid
    db.commit()
    db.refresh(deployment)
    return deployment


def get_logger_currently_deployed(installation_uid: int, db: Session):
    deployments = pd.DataFrame([d.__dict__ for d in
                                get_all_deployments_at_installation_uid(installation_uid=installation_uid, db=db)])
    if not deployments.empty:
        readable_deployments = pd.DataFrame(
            get_readable_logger_deployments(logger_deployment_uid_list=list(deployments["logger_deployment_uid"]),
                                            db=db),
            columns=["logger_deployment_uid", "installation_code", "logger_sn", "deployment_date", "extraction_date",
                     "deployment_roa", "deployment_notes"])
        readable_deployments.sort_values(by="deployment_date", inplace=True, ascending=False)
        deployment_uid = None
        for i, r in readable_deployments.iterrows():
            if pd.isna(r["extraction_date"]):
                deployment_uid = r["logger_deployment_uid"]
                break
        if deployment_uid is None:
            return None
        deployment_record = deployments.loc[deployments["logger_deployment_uid"] == deployment_uid].iloc[0]
        logger_uid = deployment_record["logger_uid"]
        return get_logger_by_uid(logger_uid=int(logger_uid), db=db)
    else:
        return None


def get_all_visits_to_installation(installation_uid: int, db: Session):
    return db.query(models.InstallationVisit) \
        .filter(models.InstallationVisit.installation_uid == installation_uid).all()


def get_closest_installation_visit(installation_uid: int, date: dt.datetime, db: Session,
                                   max_difference_hours: int = None, linked_to_deployment: bool = False):
    installation_visit_table = \
        pd.DataFrame([d.__dict__ for d in get_all_visits_to_installation(installation_uid=installation_uid, db=db)])
    if installation_visit_table.empty:
        return None
    installation_visit_table["time_difference"] = abs(installation_visit_table["visit_date"] - date)
    if max_difference_hours is not None:
        within_tolerance = installation_visit_table.loc[
            installation_visit_table["time_difference"].dt.total_seconds() <= max_difference_hours * 3600].copy()
    else:
        within_tolerance = installation_visit_table.copy()
    within_tolerance.sort_values(by="time_difference", inplace=True)
    if linked_to_deployment:
        closest = None
        for i, r in within_tolerance.iterrows():
            if get_logger_deployment_by_extraction_visit_uid(r["installation_visit_uid"], db=db) is not None \
                    or get_logger_deployment_by_deployment_visit_uid(r["installation_visit_uid"], db=db):
                closest = within_tolerance.loc[i]
                break
    else:
        closest = within_tolerance.loc[
            within_tolerance["time_difference"] == within_tolerance["time_difference"].min()].iloc[0]
    if closest is not None:
        return get_installation_visit_by_uid(uid=int(closest["installation_visit_uid"]), db=db)
    else:
        return None


def update_installation(uid: int, db: Session, installation_code: str | None = None,
                        installation_name: str | None = None, installation_type: str | None = None,
                        latitude: float | None = None, longitude: float | None = None, notes: str | None = None,
                        site_uid: int | None = None):
    db_installation = get_installation_by_uid(db=db, installation_uid=uid)
    if installation_code is not None:
        db_installation.installation_code = installation_code
    if installation_name is not None:
        db_installation.installation_name = installation_name
    if installation_type is not None:
        db_installation.installation_type = installation_type
    if latitude is not None:
        db_installation.latitude = latitude
    if longitude is not None:
        db_installation.longitude = longitude
    if notes is not None:
        if db_installation.notes is None:
            db_installation.notes = notes
        else:
            db_installation.notes = f"{db_installation.notes}\n{notes}"
    if site_uid is not None:
        db_installation.site_uid = site_uid
    db.commit()
    db.refresh(db_installation)
    return db_installation


def update_logger_download(db: Session, logger_download_uid: int, logger_uid: int | None = None,
                           logger_deployment_uid: int | None = None, download_date: dt.datetime | None = None,
                           download_quality: str | None = None):
    db_logger_download = get_logger_download_by_uid(logger_download_uid=logger_download_uid, db=db)
    if logger_uid is not None:
        db_logger_download.logger_uid = logger_uid
    if logger_deployment_uid is not None:
        db_logger_download.logger_deployment_uid = logger_deployment_uid
    if download_date is not None:
        db_logger_download.download_date = download_date
    if download_quality is not None:
        db_logger_download.download_quality = download_quality
    db.commit()
    db.refresh(db_logger_download)
    return db_logger_download


def delete_logger_deployment(db: Session, logger_deployment_uid: int):
    db_logger_deployment = get_logger_deployment_by_uid(uid=logger_deployment_uid, db=db)
    db.delete(db_logger_deployment)
    db.commit()
    return logger_deployment_uid


def get_installation_pair(db: Session, installation_uid: int):
    forward = db.query(models.InstallationPair) \
        .filter(models.InstallationPair.installation_uid_1 == installation_uid).first()
    if forward is None:
        backward = db.query(models.InstallationPair) \
            .filter(models.InstallationPair.installation_uid_2 == installation_uid).first()
        return backward
    else:
        return forward


def add_installation_pair(db: Session, installation_pair: schemas.InstallationPairBase):
    new_installation_pair = models.InstallationPair(installation_uid_1=installation_pair.installation_uid_1,
                                                    installation_uid_2=installation_pair.installation_uid_2)
    db.add(new_installation_pair)
    db.commit()
    db.refresh(new_installation_pair)
    return new_installation_pair

