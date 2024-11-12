# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-11-01
"""

from sqlalchemy.orm import Session
import datetime as dt

from . import schemas
from . import models


def get_ag_logger_data_by_logger_uid_channel_number_and_measurement_date(logger_uid: int, channel_number: int,
                                                                         date_time: dt.datetime, db: Session):
    return db.query(models.AirGroundTemperatureData).filter(
        (models.AirGroundTemperatureData.logger_uid == logger_uid)
        & (models.AirGroundTemperatureData.channel_number == channel_number)
        & (models.AirGroundTemperatureData.date_time == date_time)).first()


def add_ag_logger_data(ag_logger_data: schemas.AirGroundTemperatureDataBase, db: Session):
    new_ag_logger_data = models.AirGroundTemperatureData(logger_uid=ag_logger_data.logger_uid,
                                                         logger_download_uid=ag_logger_data.logger_download_uid,
                                                         channel_number=ag_logger_data.channel_number,
                                                         installation_uid=ag_logger_data.installation_uid,
                                                         date_time=ag_logger_data.date_time.replace(microsecond=0),
                                                         temperature=ag_logger_data.temperature)
    db.add(new_ag_logger_data)
    db.commit()
    db.refresh(new_ag_logger_data)
    return new_ag_logger_data


def get_ag_logger_data_at_installation(installation_uid: int, db: Session):
    return db.query(models.AirGroundTemperatureData.date_time,
                    models.AirGroundTemperatureData.temperature,
                    models.AirGroundTemperatureData.channel_number,
                    models.Logger.logger_serial_number) \
        .join(models.Logger) \
        .filter(models.AirGroundTemperatureData.installation_uid == installation_uid).all()


def get_ag_data_by_installation_and_measurement_date(installation_uid: int, date_time: dt.datetime, db: Session):
    return db.query(models.AirGroundTemperatureData) \
        .filter((models.AirGroundTemperatureData.installation_uid == installation_uid)
                & (models.AirGroundTemperatureData.date_time == date_time)).first()
