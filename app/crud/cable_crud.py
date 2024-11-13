# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-12
"""

from sqlalchemy.orm import Session
import datetime as dt
import pytz

from app import schemas
from app import models


def get_cable_by_installation_uid(db: Session, installation_uid: int):
    return db.query(models.Cable).filter(models.Cable.installation_uid == installation_uid).first()


def add_cable(db: Session, cable: schemas.CableBase):
    new_cable = models.Cable(installation_uid=cable.installation_uid,
                             connector_type=cable.connector_type,
                             length=cable.length,
                             borehole_depth=cable.borehole_depth,
                             num_sensors=cable.num_sensors)
    db.add(new_cable)
    db.commit()
    db.refresh(new_cable)
    return new_cable


def get_cable_sensor_by_uid(db: Session, cable_sensor_uid: int):
    return db.query(models.CableSensor).filter(models.CableSensor.cable_sensor_uid == cable_sensor_uid).first()


def get_cable_sensor_by_cable_uid_sensor_number_and_date_installed(db: Session, sensor_number: int, cable_uid: int,
                                                                   date_installed: dt.datetime):
    return db.query(models.CableSensor).filter((models.CableSensor.cable_uid == cable_uid)
                                               & (models.CableSensor.number_in_chain == sensor_number)
                                               & (models.CableSensor.date_installed == date_installed)).first()


def add_cable_sensor(db: Session, cable_sensor: schemas.CableSensorBase):
    new_cable_sensor = models.CableSensor(cable_uid=cable_sensor.cable_uid,
                                          date_installed=cable_sensor.date_installed.replace(microsecond=0),
                                          depth=cable_sensor.depth,
                                          sensor_type=cable_sensor.sensor_type,
                                          number_in_chain=cable_sensor.number_in_chain)
    db.add(new_cable_sensor)
    db.commit()
    db.refresh(new_cable_sensor)
    return new_cable_sensor


def update_cable(db: Session, uid: int | None, connector_type: str | None, length: float | None,
                 borehole_depth: float | None, num_sensors: int | None):
    cable = db.query(models.Cable).filter(models.Cable.cable_uid == uid).first()
    if connector_type is not None:
        cable.connector_type = connector_type
    if length is not None:
        cable.length = length
    if borehole_depth is not None:
        cable.borehole_depth = borehole_depth
    if num_sensors is not None:
        cable.num_sensors = num_sensors
    db.commit()
    db.refresh(cable)
    return cable


def update_cable_sensor(cable_sensor_uid: int, db: Session, date_installed: dt.datetime | None,
                        depth: float | None, sensor_type: str | None, number_in_chain: int | None):
    cable_sensor = get_cable_sensor_by_uid(db=db, cable_sensor_uid=cable_sensor_uid)
    if date_installed is not None:
        cable_sensor.date_installed = date_installed
    if depth is not None:
        cable_sensor.depth = depth
    if sensor_type is not None:
        cable_sensor.sensor_type = sensor_type
    if number_in_chain is not None:
        cable_sensor.date_installed = number_in_chain
    db.commit()
    db.refresh(cable_sensor)
    return cable_sensor


def get_cable_manual_read_by_sensor_and_installation_visit_uids(sensor_uid: int, installation_visit_uid: int,
                                                                db: Session):
    return db.query(models.CableManualRead) \
        .filter((models.CableManualRead.cable_sensor_uid == sensor_uid)
                & (models.CableManualRead.installation_visit_uid == installation_visit_uid)).first()


def add_cable_manual_read(cable_manual_read: schemas.CableManualReadInput, db: Session):
    new_cable_manual_read = models.CableManualRead(cable_sensor_uid=cable_manual_read.cable_sensor_uid,
                                                   installation_uid=cable_manual_read.installation_uid,
                                                   installation_visit_uid=cable_manual_read.installation_visit_uid,
                                                   temperature=cable_manual_read.temperature,
                                                   ol=cable_manual_read.ol,
                                                   drift_down=cable_manual_read.drift_down,
                                                   drift_up=cable_manual_read.drift_up)
    db.add(new_cable_manual_read)
    db.commit()
    db.refresh(new_cable_manual_read)
    return new_cable_manual_read


def get_cable_sensor_by_cable_uid_sensor_number_and_date_visited(cable_uid: int, sensor_number: int,
                                                                 date_visited: dt.datetime, db: Session):
    sensor_records = db.query(models.CableSensor).filter((models.CableSensor.cable_uid == cable_uid)
                                                         & (models.CableSensor.number_in_chain == sensor_number)).all()
    if sensor_records:
        time_gaps = {}
        for record in sensor_records:
            if record.date_installed is None:
                time_gaps[date_visited - dt.datetime(1900, 1, 1, tzinfo=pytz.utc)] = record.cable_sensor_uid
            else:
                time_gaps[date_visited - record.date_installed] = record.cable_sensor_uid
        positive_diffs = [k for k in time_gaps.keys() if k >= dt.timedelta(0)]
        if positive_diffs:
            sensor_uid = int(time_gaps[min(positive_diffs)])
            db_cable_sensor = db.query(models.CableSensor).filter(models.CableSensor.cable_sensor_uid == sensor_uid).first()
            return db_cable_sensor
        else:
            return None
    else:
        return None


def get_all_cable_sensor_records_for_cable_uid_and_sensor_number(cable_uid: int, sensor_number: int, db: Session):
    return db.query(models.CableSensor).filter((models.CableSensor.cable_uid == cable_uid)
                                               & (models.CableSensor.number_in_chain == sensor_number)).all()


def get_cable_logger_data_by_logger_uid_sensor_uid_and_measurement_date(logger_uid: int, sensor_uid: int,
                                                                        date_time: dt.datetime, db: Session):
    return db.query(models.CableLoggerData).filter((models.CableLoggerData.logger_uid == logger_uid)
                                                   & (models.CableLoggerData.cable_sensor_uid == sensor_uid)
                                                   & (models.CableLoggerData.date_time == date_time)).first()


def add_cable_logger_data(cable_logger_data: schemas.CableLoggerDataBase, db: Session):
    new_cable_logger_data = models.CableLoggerData(logger_uid=cable_logger_data.logger_uid,
                                                   logger_download_uid=cable_logger_data.logger_download_uid,
                                                   cable_sensor_uid=cable_logger_data.cable_sensor_uid,
                                                   installation_uid=cable_logger_data.installation_uid,
                                                   date_time=cable_logger_data.date_time.replace(microsecond=0),
                                                   temperature=cable_logger_data.temperature)
    db.add(new_cable_logger_data)
    db.commit()
    db.refresh(new_cable_logger_data)
    return new_cable_logger_data


def get_cable_logger_data_at_installation(installation_uid: int, db: Session):
    return db.query(models.CableLoggerData.date_time,
                    models.CableLoggerData.temperature,
                    models.Logger.logger_serial_number,
                    models.CableSensor.number_in_chain,
                    models.CableSensor.depth) \
        .join(models.CableSensor) \
        .join(models.Logger) \
        .filter(models.CableLoggerData.installation_uid == installation_uid).all()


def get_cable_manual_read_data_at_installation(installation_uid: int, db: Session):
    return db.query(models.CableManualRead.resistance,
                    models.CableManualRead.ol,
                    models.CableManualRead.drift_up,
                    models.CableManualRead.drift_down,
                    models.CableSensor.number_in_chain,
                    models.CableSensor.depth,
                    models.CableSensor.sensor_type,
                    models.InstallationVisit.visit_date) \
        .join(models.CableSensor) \
        .join(models.InstallationVisit) \
        .filter(models.CableManualRead.installation_uid == installation_uid).all()


def get_cable_data_by_sensor_uid_and_measurement_date(sensor_uid: int, date_time: dt.datetime, db: Session):
    return db.query(models.CableLoggerData).filter((models.CableLoggerData.cable_sensor_uid == sensor_uid)
                                                   & (models.CableLoggerData.date_time == date_time)).first()


def get_stick_up_by_installation_visit_uid(installation_visit_uid: int, db: Session):
    return db.query(models.StickUp).filter(models.StickUp.installation_visit_uid == installation_visit_uid).first()


def add_stick_up(stick_up: schemas.StickUpBase, db: Session):
    new_stick_up = models.StickUp(installation_visit_uid=stick_up.installation_visit_uid,
                                  measurement=stick_up.measurement,
                                  reference=stick_up.reference)
    db.add(new_stick_up)
    db.commit()
    db.refresh(new_stick_up)
    return new_stick_up


def get_all_cable_sensors(cable_uid: int, db: Session):
    return db.query(models.CableSensor).filter(models.CableSensor.cable_uid == cable_uid).all()


def get_cable_sensor_mapping_by_cable_sensor_uid(cable_sensor_uid: int, db: Session):
    return db.query(models.CableSensorMapping) \
        .filter(models.CableSensorMapping.cable_sensor_uid == cable_sensor_uid).first()


def add_cable_sensor_mapping(cable_sensor_mapping: schemas.CableSensorMappingBase, db: Session):
    new_cable_sensor_mapping = models.CableSensorMapping(cable_uid=cable_sensor_mapping.cable_uid,
                                                         cable_sensor_uid=cable_sensor_mapping.cable_sensor_uid,
                                                         mapping_1=cable_sensor_mapping.mapping_1,
                                                         mapping_2=cable_sensor_mapping.mapping_2)
    db.add(new_cable_sensor_mapping)
    db.commit()
    db.refresh(new_cable_sensor_mapping)
    return new_cable_sensor_mapping


def get_cable_sensor_mappings_of_cable(cable_uid: int, db: Session):
    return db.query(models.CableSensorMapping.cable_sensor_uid,
                    models.CableSensorMapping.mapping_1,
                    models.CableSensorMapping.mapping_2,
                    models.CableSensor.number_in_chain)\
        .join(models.CableSensor)\
        .filter(models.CableSensorMapping.cable_uid == cable_uid).all()
