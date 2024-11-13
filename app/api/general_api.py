# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-06-20
"""

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Union
import numpy as np
import datetime as dt
import pandas as pd

from app import schemas
from app import crud
from .api import app, get_db, check_tz_aware
from app.output_data_structures import output_schemas as ods_schemas

logger_type_list = ["RBR - seacon", "RBR - impulse", "RBR - bendix", "HOBO U22", "HOBO U23", "Vemco",
                    "Campbell Sci. CR300", "RBR - unknown", "HOBO - unknown"]
installation_types = ["weather station", "thaw tube", "cable", "air", "ground surface", "four channel"]
regions = ["inuvik", "norman wells", "fort simpson", "yellowknife", "alert", "alaska highway"]


@app.get("/")
async def root():
    return {"name": "thermal db api"}


@app.get("/sites/site_uid{site_uid}", response_model=schemas.Site)
async def get_site_by_uid(site_uid: int, db: Session = Depends(get_db)):
    site = crud.get_site_by_uid(db=db, site_uid=site_uid)
    if site is None:
        raise HTTPException(status_code=400, detail=f"Site {site_uid} does not exist")
    return site


@app.get("/sites/site_code{site_code}", response_model=schemas.Site)
async def get_site_by_code(site_code: str, db: Session = Depends(get_db)):
    site = crud.get_site_by_code(db=db, site_code=site_code)
    if site is None:
        raise HTTPException(status_code=400, detail=f"Site {site_code} does not exist")
    return site


@app.post("/sites/", response_model=schemas.Site)
async def add_site(site: schemas.SiteBase, db: Session = Depends(get_db)):
    db_site = crud.get_site_by_code(db, site.site_code)
    if db_site:
        raise HTTPException(status_code=400, detail=f"Site {site.site_code} already exists")
    if site.site_name is None:
        raise HTTPException(status_code=400, detail="Site name must be specified")
    if site.site_code is None:
        raise HTTPException(status_code=400, detail="Site code must be specified")
    if site.latitude is None:
        raise HTTPException(status_code=400, detail="Latitude of site must be specified")
    if site.longitude is None:
        raise HTTPException(status_code=400, detail="Longitude of site must be specified")
    if site.region not in regions:
        raise HTTPException(status_code=400, detail=f"The region {site.region} is not in {regions}. "
                                                    f"Contact Ryan if it needs to be added")
    if not -90 <= site.latitude <= 90:
        raise HTTPException(status_code=400, detail="Latitude is invalid")
    if not -180 <= site.latitude <= 180:
        raise HTTPException(status_code=400, detail="Longitude is invalid")
    return crud.add_site(db, site)


@app.post("/installations/", response_model=schemas.Installation)
async def add_installation(installation: schemas.InstallationBase, db: Session = Depends(get_db)):
    db_installation = crud.get_installation_by_code(db, installation.installation_code)
    if db_installation:
        raise HTTPException(status_code=400, detail=f"Installation {installation.installation_code} already exists")
    if installation.installation_name is None:
        raise HTTPException(status_code=400, detail="Installation name must be specified")
    if installation.installation_code is None:
        raise HTTPException(status_code=400, detail="Installation code must be specified")
    if installation.installation_type not in installation_types:
        raise HTTPException(status_code=400, detail=f"Invalid installation type: {installation.installation_type}")
    if installation.site_uid is None:
        raise HTTPException(status_code=400, detail="Installation site UID must be specified")
    if installation.latitude is None:
        raise HTTPException(status_code=400, detail="Latitude of installation must be specified")
    if installation.longitude is None:
        raise HTTPException(status_code=400, detail="Longitude of installation must be specified")
    if not -90 <= installation.latitude <= 90:
        raise HTTPException(status_code=400, detail="Latitude is invalid")
    if not -180 <= installation.latitude <= 180:
        raise HTTPException(status_code=400, detail="longitude is invalid")
    return crud.add_installation(db, installation)


@app.get("/installations/installation_code{installation_code}", response_model=schemas.Installation)
async def get_installation_by_code(installation_code: str, db: Session = Depends(get_db)):
    installation = crud.get_installation_by_code(db=db, installation_code=installation_code)
    if installation is None:
        raise HTTPException(status_code=400, detail=f"Installation {installation_code} does not exist")
    return installation


@app.get("/installations/installation_uid{installation_uid}", response_model=schemas.Installation)
async def get_installation_by_uid(installation_uid: int, db: Session = Depends(get_db)):
    installation = crud.get_installation_by_uid(db=db, installation_uid=installation_uid)
    if installation is None:
        raise HTTPException(status_code=400, detail=f"Installation uid {installation_uid} does not exist")
    return installation


@app.get("/installation_visits/date_and_installation_uid/", response_model=schemas.InstallationVisit)
async def get_installation_visit_by_date_and_uid(installation_uid: int, visit_date: dt.datetime,
                                                 db: Session = Depends(get_db)):
    if not check_tz_aware(visit_date):
        raise HTTPException(status_code=400, detail=f"{visit_date} is not time zone aware.")
    installation_visit = crud.get_installation_visit_by_date_and_code(db=db, visit_date=visit_date,
                                                                      installation_uid=installation_uid)
    if installation_visit is None:
        raise HTTPException(status_code=400, detail=f"There is no recorded visit to installation UID "
                                                    f"{installation_uid} on {visit_date}")
    return installation_visit


@app.post("/installation_visits/", response_model=schemas.InstallationVisit)
async def add_installation_visit(installation_visit: schemas.InstallationVisitBase, db: Session = Depends(get_db)):
    db_installation_visit = \
        crud.get_installation_visit_by_date_and_code(db=db, visit_date=installation_visit.visit_date,
                                                     installation_uid=installation_visit.installation_uid)
    if db_installation_visit:
        raise HTTPException(status_code=400, detail=f"Installation visit already exists")
    if installation_visit.installation_uid is None:
        raise HTTPException(status_code=400, detail="Installation UID must be specified")
    if installation_visit.record_of_activities is None:
        raise HTTPException(status_code=400, detail="Record of activities must be specified")
    if installation_visit.visit_date is None:
        raise HTTPException(status_code=400, detail="Visit date must be specified")
    if not check_tz_aware(installation_visit.visit_date):
        raise HTTPException(status_code=400, detail=f"{installation_visit.visit_date} is not time zone aware.")
    if installation_visit.field_party is None:
        raise HTTPException(status_code=400, detail="Field party must be specified")
    return crud.add_installation_visit(db, installation_visit)


@app.post("/al_probe_measurements/", response_model=schemas.ALProbeMeasurement)
async def add_al_probe_measurement(al_probe_measurement: schemas.ALProbeMeasurementBase, db: Session = Depends(get_db)):
    db_al_probe_measurement = crud.get_al_probe_measurement_by_installation_visit_uid_and_probe_number(
        db=db,
        installation_visit_uid=al_probe_measurement.installation_visit_uid,
        probe_number=al_probe_measurement.probe_number)
    if db_al_probe_measurement:
        raise HTTPException(status_code=400, detail=f"probe measurement {al_probe_measurement.probe_number} for "
                                                    f"installation visit UID"
                                                    f"{al_probe_measurement.installation_visit_uid} already exists")
    if al_probe_measurement.installation_visit_uid is None:
        raise HTTPException(status_code=400, detail="Installation visit uid must be specified")
    if al_probe_measurement.probe_number is None:
        raise HTTPException(status_code=400, detail="Probenumber must be specified")
    if al_probe_measurement.measurement is None:
        raise HTTPException(status_code=400, detail="Measurement must be specified")
    if al_probe_measurement.probe_maxed is None:
        raise HTTPException(status_code=400, detail="Probe maxed must be specified")
    return crud.add_al_probe_measurement(db=db, al_probe_measurement=al_probe_measurement)


@app.get("/al_probe_measurements/installation_visit_uid_and_probe_number/", response_model=schemas.ALProbeMeasurement)
async def get_al_probe_measurement_by_installation_visit_uid_and_probe_number(installation_visit_uid: int,
                                                                              probe_number: int,
                                                                              db: Session = Depends(get_db)):
    db_al_probe_measurement = crud.get_al_probe_measurement_by_installation_visit_uid_and_probe_number(
        db=db,
        installation_visit_uid=installation_visit_uid,
        probe_number=probe_number)

    if db_al_probe_measurement is None:
        raise HTTPException(status_code=400, detail=f"No probe measurement {probe_number} for installation visit UID"
                                                    f"{installation_visit_uid} found")
    return db_al_probe_measurement


@app.get("/loggers/logger_sn{sn}", response_model=schemas.Logger)
async def get_logger_by_sn(sn: str, db: Session = Depends(get_db)):
    db_logger = crud.get_logger_by_sn(db=db, logger_sn=sn)
    if db_logger is None:
        raise HTTPException(status_code=400, detail=f"Logger SN {sn} does not exist")
    return db_logger


@app.get("/loggers/logger_uid{uid}", response_model=schemas.Logger)
async def get_logger_by_uid(uid: int, db: Session = Depends(get_db)):
    db_logger = crud.get_logger_by_uid(db=db, logger_uid=uid)
    if db_logger is None:
        raise HTTPException(status_code=400, detail=f"Logger UID {uid} does not exist")
    return db_logger


@app.get("/loggers/logger_sn_and_type/", response_model=schemas.Logger)
async def get_logger_by_sn_and_type(logger_sn: str, logger_type: str, db: Session = Depends(get_db)):
    db_logger = crud.get_logger_by_sn_and_type(db=db, logger_sn=logger_sn, logger_type=logger_type)
    if db_logger is None:
        raise HTTPException(status_code=400, detail=f"Logger SN {logger_sn} does not exist as a {logger_type}")
    return db_logger


@app.post("/loggers/update_type/", response_model=schemas.Logger)
async def update_logger_type(logger_uid: int, logger_type: str, db: Session = Depends(get_db)):
    if logger_type in logger_type_list:
        db_logger = crud.update_logger_type(db=db, logger_uid=logger_uid, logger_type=logger_type)
    else:
        raise HTTPException(status_code=400, detail=f"Logger type must be in {logger_type_list}")
    return db_logger


@app.post("/loggers/update_battery_year/", response_model=schemas.Logger)
async def update_logger_battery_year(logger_uid: int, battery_year: int, db: Session = Depends(get_db)):
    if battery_year in range(1985, 2100):
        db_logger = crud.update_logger_battery_year(db=db, logger_uid=logger_uid, battery_year=battery_year)
    else:
        raise HTTPException(status_code=400, detail=f"Year must be between 1985 and 2100")
    return db_logger


@app.post("/loggers/", response_model=schemas.Logger)
async def add_logger(logger: schemas.LoggerBase, db: Session = Depends(get_db)):
    if logger.logger_serial_number is None:
        raise HTTPException(status_code=400, detail="Logger SN must be specified")
    if logger.logger_type not in logger_type_list:
        raise HTTPException(status_code=400, detail=f"Logger type must be in {logger_type_list}")
    db_logger = crud.get_logger_by_sn_and_type(db=db, logger_sn=logger.logger_serial_number,
                                               logger_type=logger.logger_type)
    if db_logger is not None:
        raise HTTPException(status_code=400, detail=f"A logger of type {logger.logger_type} with the SN "
                                                    f"{logger.logger_serial_number} already exists")
    return crud.add_logger(db=db, logger=logger)


@app.get("/logger_deployments/most_recent_installation_and_logger_uid/", response_model=schemas.LoggerDeployment)
async def get_most_recent_deployment_by_installation_and_logger_uid(logger_uid: int, installation_uid: int,
                                                                    db: Session = Depends(get_db)):
    db_deployment = crud.get_most_recent_deployment_by_installation_and_logger_uid(db=db, logger_uid=logger_uid,
                                                                                   installation_uid=installation_uid)
    if db_deployment is None:
        raise HTTPException(status_code=400, detail=f"No record of logger uid {logger_uid} being deployed at "
                                                    f"installation uid {installation_uid}")
    return db_deployment


@app.get("/logger_deployments/previous_unclosed_by_installation_and_logger_uid/",
         response_model=list[schemas.LoggerDeployment])
async def get_previous_unclosed_logger_deployment_at_installation(logger_uid: int, installation_uid: int,
                                                                  visit_date: dt.datetime, return_closest: bool,
                                                                  db: Session = Depends(get_db)):
    if not check_tz_aware(visit_date):
        raise HTTPException(status_code=400, detail=f"{visit_date} is not time zone aware.")
    db_deployment = crud.get_previous_unclosed_logger_deployment_at_installation(
        db=db, logger_uid=logger_uid, installation_uid=installation_uid, visit_date=visit_date,
        return_closest=return_closest)
    if db_deployment is None:
        raise HTTPException(status_code=400, detail=f"No record of logger uid {logger_uid} being deployed at "
                                                    f"installation uid {installation_uid}")
    return db_deployment


@app.get("/installation_visits/installation_visit_uid{uid}", response_model=schemas.InstallationVisit)
async def get_installation_visit_by_uid(uid: int, db: Session = Depends(get_db)):
    db_installation_visit = crud.get_installation_visit_by_uid(db=db, uid=uid)
    if db_installation_visit is None:
        raise HTTPException(status_code=400, detail=f"Installation visit UID {uid} does not exist")
    return db_installation_visit


@app.get("/logger_deployments/installation_uid{installation_uid}", response_model=list[schemas.LoggerDeployment])
async def get_all_deployments_at_installation_uid(installation_uid: int, db: Session = Depends(get_db)):
    db_deployments = crud.get_all_deployments_at_installation_uid(db=db, installation_uid=installation_uid)
    if not db_deployments:
        raise HTTPException(status_code=400, detail=f"No logger deployments recoded at installation UID "
                                                    f"{installation_uid}")
    return db_deployments


@app.post("/logger_deployments/", response_model=schemas.LoggerDeployment)
async def add_logger_deployment(logger_deployment: schemas.LoggerDeploymentBase, db: Session = Depends(get_db)):
    if logger_deployment.logger_uid is None:
        raise HTTPException(status_code=400, detail="Logger UID must be specified")
    if logger_deployment.installation_uid is None:
        raise HTTPException(status_code=400, detail="Installation UID must be specified")
    if logger_deployment.deployment_visit_uid is None and logger_deployment.extraction_visit_uid is None:
        raise HTTPException(status_code=400, detail="extraction visit UID or deployment visit UID must be specified")
    if logger_deployment.deployment_visit_uid is None:
        db_logger_deployment = crud.get_logger_deployment_by_extraction_visit_uid(
            db=db,
            extraction_uid=logger_deployment.extraction_visit_uid)
    else:
        db_logger_deployment = crud.get_logger_deployment_by_deployment_visit_uid(
            db=db,
            deployment_uid=logger_deployment.deployment_visit_uid)
    if db_logger_deployment is not None:
        raise HTTPException(status_code=400, detail=f"Logger deployment already exists")
    return crud.add_logger_deployment(db=db, logger_deployment=logger_deployment)


@app.post("/logger_deployments/close_deployment/", response_model=schemas.LoggerDeployment)
async def close_logger_deployment(logger_deployment_uid: int, installation_visit_uid: int,
                                  db: Session = Depends(get_db)):
    db_logger_deployment = crud.get_logger_deployment_by_uid(db=db, uid=logger_deployment_uid)
    if db_logger_deployment is None:
        raise HTTPException(status_code=400, detail=f"Logger deployment UID {logger_deployment_uid} does not exist")
    if db_logger_deployment.extraction_visit_uid is not None:
        raise HTTPException(status_code=400, detail=f"Logger deployment UID {logger_deployment_uid} already closed")
    db_installation_visit = crud.get_installation_visit_by_uid(db=db, uid=installation_visit_uid)
    if db_installation_visit is None:
        raise HTTPException(status_code=400, detail=f"Installation visit UID {logger_deployment_uid} does not exist")
    return crud.close_logger_deployment(db=db, logger_deployment_uid=logger_deployment_uid,
                                        installation_visit_uid=installation_visit_uid)


@app.get("/logger_deployments/extraction_visit_uid/", response_model=schemas.LoggerDeployment)
async def get_logger_deployment_extraction_visit_uid(extraction_uid: int, db: Session = Depends(get_db)):
    db_logger_deployment = crud.get_logger_deployment_by_extraction_visit_uid(db=db, extraction_uid=extraction_uid)
    if db_logger_deployment is None:
        raise HTTPException(status_code=400, detail=f"No deployment record exists where a logger was extracted "
                                                    f"during installation visit uid {extraction_uid}")
    return db_logger_deployment


@app.get("/logger_deployments/deployment_visit_uid/", response_model=schemas.LoggerDeployment)
async def get_logger_deployment_by_deployment_visit_uid(deployment_uid: int, db: Session = Depends(get_db)):
    db_logger_deployment = crud.get_logger_deployment_by_deployment_visit_uid(db=db, deployment_uid=deployment_uid)
    if db_logger_deployment is None:
        raise HTTPException(status_code=400, detail=f"No deployment record exists where a logger was deployed "
                                                    f"during installation visit uid {deployment_uid}")
    return db_logger_deployment


@app.get("/logger_deployments/logger_deployment_uid{uid}", response_model=schemas.LoggerDeployment)
async def get_logger_deployment_by_uid(uid: int, db: Session = Depends(get_db)):
    db_logger_deployment = crud.get_logger_deployment_by_uid(db=db, uid=uid)
    if db_logger_deployment is None:
        raise HTTPException(status_code=400, detail=f"Logger deployment UID {uid} does not exist")
    return db_logger_deployment


@app.post("/logger_downloads/", response_model=schemas.LoggerDownload)
async def add_logger_download(logger_download: schemas.LoggerDownloadBase, db: Session = Depends(get_db)):
    if logger_download.logger_uid is None:
        raise HTTPException(status_code=400, detail=f"Logger UID must be specified")
    if logger_download.logger_deployment_uid is None:
        raise HTTPException(status_code=400, detail=f"Logger deployment UID must be specified")
    if logger_download.download_date is None:
        raise HTTPException(status_code=400, detail=f"Logger download date must be specified")
    if not check_tz_aware(logger_download.download_date):
        raise HTTPException(status_code=400, detail=f"{logger_download.download_date} is not time zone aware.")
    db_logger_download = crud.get_logger_download_by_deployment_uid(
        db=db,
        deployment_uid=logger_download.logger_deployment_uid)
    if db_logger_download is not None:
        raise HTTPException(status_code=400, detail=f"A logger download record is already linked to deployment UID "
                                                    f"{logger_download.logger_deployment_uid}")
    return crud.add_logger_download(db=db, logger_download=logger_download)


@app.get("/logger_downloads/deployment_uid{deployment_uid}", response_model=schemas.LoggerDownload)
async def get_logger_download_by_deployment_uid(deployment_uid: int, db: Session = Depends(get_db)):
    db_logger_download = crud.get_logger_download_by_deployment_uid(db=db, deployment_uid=deployment_uid)
    if db_logger_download is None:
        raise HTTPException(status_code=400, detail=f"no logger download linked to logger deployment UID "
                                                    f"{deployment_uid}")
    return db_logger_download


@app.get("/installation_visits/logger_history/installation_uid{installation_uid}",
         response_model=list[ods_schemas.InstallationLoggerHistory])
async def get_logger_history_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    logger_history = pd.DataFrame(crud.get_logger_history_at_installation(db=db, installation_uid=installation_uid),
                                  columns=["installation_visit_uid", "date_time", "recorded_by", "activity", "notes",
                                           "logger_in_uid", "logger_in", "logger_in_type", "logger_out_uid",
                                           "logger_out", "logger_out_type"])
    logger_history.drop(columns=["logger_in_uid", "logger_out_uid"], inplace=True)
    installation_type = crud.get_installation_by_uid(installation_uid=installation_uid, db=db).installation_type
    if installation_type == "cable":
        for i, r in logger_history.iterrows():
            db_stick_up = crud.get_stick_up_by_installation_visit_uid(
                installation_visit_uid=r["installation_visit_uid"], db=db)
            if db_stick_up is not None:
                logger_history.loc[i, "stick_up"] = db_stick_up.measurement
    logger_history.sort_values(by="date_time", inplace=True)
    logger_history.replace(np.nan, None, inplace=True)
    return logger_history.to_dict("records")


@app.get("/al_probe_measurements/al_probe_history/installation_uid{installation_uid}",
         response_model=list[ods_schemas.ALProbeHistory])
async def get_al_probe_history_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return pd.DataFrame(crud.get_al_probe_history_at_installation(db=db, installation_uid=installation_uid),
                        columns=["probe_number", "probe_depth", "probe_maxed", "date_time"]).to_dict("records")


@app.get("/installations/site_uid{site_uid}",
         response_model=list[schemas.Installation])
async def get_installations_at_site(site_uid: int, db: Session = Depends(get_db)):
    return crud.get_installations_at_site(site_uid=site_uid, db=db)


@app.get("/installations/survey_info/{installation_type}",
         response_model=list[ods_schemas.SurveyInfo], response_model_exclude_unset=True)
async def get_info_for_survey(installation_type, db: Session = Depends(get_db)):
    wire_mapping_cols = [f"sensor{i + 1}" for i in range(8)]
    if installation_type not in ["cable", "air", "ground surface", "thaw tube", "weather station", "four channel"]:
        raise HTTPException(status_code=400, detail=f"{installation_type} is not in ['cable', 'air', 'ground surface', "
                                                    f"'thaw tube', 'weather station', 'four channel']")
    data = pd.DataFrame([obj.__dict__ for obj in
                         crud.get_all_installations_of_type(installation_type=installation_type, db=db)])
    for i, r in data.iterrows():
        installation_visit = crud.get_most_recent_installation_visit_at_installation(
            installation_uid=r["installation_uid"], db=db)
        if installation_visit is not None:
            if r["notes"] is not None and installation_visit.notes is not None:
                data.loc[i, "notes"] = "\n\n".join([r["notes"], installation_visit.notes])
            elif installation_visit.notes is not None:
                data.loc[i, "notes"] = installation_visit.notes
        data["label"] = data["installation_code"] + " - " + data["installation_name"]

        if installation_type not in ["thaw tube", "weather station"]:
            deployed_logger = crud.get_logger_currently_deployed(installation_uid=r["installation_uid"], db=db)
            if deployed_logger is not None:
                data.loc[i, "logger_sn"] = deployed_logger.logger_serial_number
                if installation_type != "cable":
                    data.loc[i, "logger_type"] = deployed_logger.logger_type

        if installation_type == "cable":
            cable = crud.get_cable_by_installation_uid(installation_uid=r["installation_uid"], db=db)
            if cable is not None:
                data.loc[i, "connector"] = cable.connector_type
                mappings = pd.DataFrame(crud.get_cable_sensor_mappings_of_cable(cable_uid=cable.cable_uid, db=db),
                                        columns=["cable_sensor_uid", "mapping_1", "mapping_2", "number_in_chain"])
                if not mappings.empty:
                    if len(mappings.index) <= len(wire_mapping_cols):
                        for i2, r2 in mappings.iterrows():
                            data.loc[i, f"sensor{r2['number_in_chain']}"] = f"{r2['mapping_1']} - {r2['mapping_2']}"
                    else:
                        print(mappings.to_markdown())
                        raise HTTPException(status_code=400,
                                            detail=f"complex case where sensors have moved and more than 8 mappings")
            else:
                data.loc[i, "connector"] = "unknown"
    data.replace(np.nan, None, inplace=True)
    if installation_type not in ["thaw tube", "weather station", "four channel"]:
        if installation_type == "cable":
            return data[["installation_code", "installation_name", "label", "notes", "logger_sn", "connector",
                         *wire_mapping_cols]].to_dict("records")
        else:
            return data[["installation_code", "installation_name", "label", "notes", "logger_sn", "logger_type"]] \
                .to_dict("records")
    else:
        return data[["installation_code", "installation_name", "label", "notes"]].to_dict("records")


@app.get("/installation_visits/dump/", response_model=list[ods_schemas.Dump])
async def get_dump(data: schemas.DumpInputSchema, db: Session = Depends(get_db)):
    year = data.year
    region = data.region
    if year is None and region is None:
        raise ValueError("year or region must be specified")
    if type(region) is str:
        region = [region]
    if year is not None:
        data = pd.DataFrame(crud.get_all_installation_visits_in_year(year=year, db=db),
                            columns=["recorded_by", "visit_date", "record_of_activities", "notes", "installation_name",
                                     "installation_code", "installation_type", "latitude", "longitude",
                                     "logger_deployed_uid", "logger_deployed", "logger_type_deployed",
                                     "logger_deployed_battery_year", "logger_extracted_uid", "logger_extracted",
                                     "logger_type_extracted", "connector_type", "stick_up"])
        data.replace(np.nan, None, inplace=True)
        data.drop(columns=["logger_deployed_uid", "logger_extracted_uid"], inplace=True)
        return data.to_dict("records")
    else:
        full_dump = None
        for r in region:
            data = crud.get_dump_for_region(region=r, db=db)
            if full_dump is None:
                full_dump = data.copy()
            else:
                full_dump = pd.concat([full_dump, data], ignore_index=True)
        full_dump.replace(np.nan, None, inplace=True)
        full_dump.drop(columns=["logger_deployed_uid", "logger_extracted_uid", "region"], inplace=True)
        return full_dump.to_dict("records")


@app.get("/logger_deployments/readable/", response_model=list[ods_schemas.ReadableLoggerDeployments])
async def get_readable_logger_deployments(logger_deployment_uid_list: list[int], db: Session = Depends(get_db)):
    data = pd.DataFrame(
        crud.get_readable_logger_deployments(logger_deployment_uid_list=logger_deployment_uid_list, db=db),
        columns=["logger_deployment_uid", "installation_code", "logger_sn", "deployment_date", "extraction_date",
                 "deployment_roa", "deployment_notes"])
    data.replace(np.nan, None, inplace=True)
    data.sort_values(by="deployment_date", inplace=True)
    return data.to_dict("records")


@app.post("/logger_deployments/update_logger/", response_model=schemas.LoggerDeployment)
async def edit_logger_in_deployment_record(logger_deployment_uid: int, new_logger_uid: int,
                                           db: Session = Depends(get_db)):
    db_logger_deployment = crud.get_logger_deployment_by_uid(uid=logger_deployment_uid, db=db)
    db_new_logger = await get_logger_by_uid(uid=new_logger_uid, db=db)
    db_cur_logger = await get_logger_by_uid(uid=db_logger_deployment.logger_uid, db=db)

    db_logger_download = crud.get_logger_download_by_deployment_uid(deployment_uid=logger_deployment_uid, db=db)
    if db_logger_download is not None:
        # modify download record
        raise HTTPException(status_code=400,
                            detail=f"CODE NOT WRITTEN :(\n logger download record must be modified to reflect update")
        pass

    return crud.edit_logger_in_deployment_record(logger_deployment_uid=logger_deployment_uid,
                                                 new_logger_uid=db_new_logger.logger_uid, db=db)


@app.get("/installation_visits/get_closest/", response_model=Union[schemas.InstallationVisit, None])
async def get_closest_installation_visit(installation_uid: int, date: dt.datetime, max_difference_hours: int = None,
                                         linked_to_deployment: bool = False, db: Session = Depends(get_db)):
    if not check_tz_aware(date):
        raise HTTPException(status_code=400, detail=f"{date} is not time zone aware.")
    return crud.get_closest_installation_visit(installation_uid=installation_uid, date=date,
                                               max_difference_hours=max_difference_hours,
                                               linked_to_deployment=linked_to_deployment, db=db)


@app.get("/installation_visits/all_visits_to_installation/", response_model=list[schemas.InstallationVisit])
def get_all_visits_to_installation(installation_uid: int, db: Session = Depends(get_db)):
    return crud.get_all_visits_to_installation(installation_uid=installation_uid, db=db)


@app.post("/installations/update/", response_model=schemas.Installation)
async def update_installation(uid: int, installation_code: str | None = None, installation_name: str | None = None,
                              installation_type: str | None = None, latitude: float | None = None,
                              longitude: float | None = None, notes: str | None = None, site_uid: int | None = None,
                              db: Session = Depends(get_db)):
    installation_types_plus_none = installation_types + [None]
    if installation_type not in installation_types_plus_none:
        raise HTTPException(status_code=400, detail=f"Invalid installation type: {installation_type}")
    if latitude is not None and not -90 <= latitude <= 90:
        raise HTTPException(status_code=400, detail="Latitude is invalid")
    if longitude is not None and not -180 <= longitude <= 180:
        raise HTTPException(status_code=400, detail="longitude is invalid")
    db_installation = crud.update_installation(db=db, uid=uid, installation_code=installation_code,
                                               installation_name=installation_name, installation_type=installation_type,
                                               latitude=latitude, longitude=longitude, site_uid=site_uid, notes=notes)
    return db_installation


@app.post("/logger_downloads/update/", response_model=schemas.LoggerDownload)
async def update_logger_download(logger_download_uid: int, logger_uid: int | None = None,
                                 logger_deployment_uid: int | None = None, download_date: dt.datetime | None = None,
                                 download_quality: str | None = None, db: Session = Depends(get_db)):
    if crud.get_logger_download_by_uid(logger_download_uid=logger_download_uid, db=db) is None:
        raise HTTPException(status_code=400, detail=f"logger download uid {logger_download_uid} does not exist")
    if logger_deployment_uid is not None \
            and crud.get_logger_deployment_by_uid(uid=logger_deployment_uid, db=db) is None:
        raise HTTPException(status_code=400, detail=f"logger deployment uid {logger_deployment_uid} does not exist")
    if logger_uid is not None \
            and crud.get_logger_by_uid(logger_uid=logger_uid, db=db) is None:
        raise HTTPException(status_code=400, detail=f"logger uid {logger_uid} does not exist")
    if download_date is not None and not check_tz_aware(download_date):
        raise HTTPException(status_code=400, detail=f"{download_date} is not time zone aware.")
    db_logger_download = crud.update_logger_download(logger_download_uid=logger_download_uid,
                                                     logger_uid=logger_uid,
                                                     logger_deployment_uid=logger_deployment_uid,
                                                     download_quality=download_quality,
                                                     db=db)
    return db_logger_download


@app.post("/logger_deployments/delete/", response_model=schemas.LoggerDeployment)
async def delete_logger_deployment(logger_deployment_uid: int, db: Session = Depends(get_db)):
    if crud.get_logger_deployment_by_uid(uid=logger_deployment_uid, db=db) is None:
        raise HTTPException(status_code=400, detail=f"logger deployment uid {logger_deployment_uid} does not exist")
    db_logger_deployment = crud.delete_logger_deployment(logger_deployment_uid=logger_deployment_uid)
    return db_logger_deployment


@app.post("/installation_pairs/", response_model=schemas.InstallationPair)
async def add_installation_pair(installation_pair: schemas.InstallationPairBase, db: Session = Depends(get_db)):
    if installation_pair.installation_uid_1 is None:
        raise HTTPException(status_code=400, detail=f"Installation UID 1 must be specified")
    if installation_pair.installation_uid_2 is None:
        raise HTTPException(status_code=400, detail=f"Installation UID 2 must be specified")
    db_installation_1 = crud.get_installation_by_uid(installation_uid=installation_pair.installation_uid_1, db=db)
    if db_installation_1 is None:
        raise HTTPException(status_code=400, detail=f"Installation UID {installation_pair.installation_uid_1} "
                                                    f"does not exist.")
    db_installation_2 = crud.get_installation_by_uid(installation_uid=installation_pair.installation_uid_2, db=db)
    if db_installation_2 is None:
        raise HTTPException(status_code=400, detail=f"Installation UID {installation_pair.installation_uid_2} "
                                                    f"does not exist.")
    db_installation_pair_1 = crud.get_installation_pair(installation_uid=installation_pair.installation_uid_1, db=db)
    if db_installation_pair_1 is not None:
        raise HTTPException(status_code=400, detail=f"Installation UID {installation_pair.installation_uid_1} "
                                                    f"is already paired.")
    db_installation_pair_2 = crud.get_installation_pair(installation_uid=installation_pair.installation_uid_2, db=db)
    if db_installation_pair_2 is not None:
        raise HTTPException(status_code=400, detail=f"Installation UID {installation_pair.installation_uid_2} "
                                                    f"is already paired.")
    return crud.add_installation_pair(installation_pair=installation_pair, db=db)


@app.get("/installation_pairs/installation_uid{installation_uid}", response_model=schemas.InstallationPair)
async def add_installation_pair(installation_uid: int, db: Session = Depends(get_db)):
    db_installation_pair = crud.get_installation_pair(db=db, installation_uid=installation_uid)
    if db_installation_pair is None:
        raise HTTPException(status_code=400, detail=f"Installation UID {installation_uid} is not paired.")
    return db_installation_pair


