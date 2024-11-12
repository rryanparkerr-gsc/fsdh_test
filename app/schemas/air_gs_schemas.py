# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-10
"""

import datetime as dt

from .base_model import BaseModelConfig


class AirGroundTemperatureDataBase(BaseModelConfig):
    logger_uid: int
    logger_download_uid: int
    installation_uid: int
    date_time: dt.datetime
    channel_number: int
    temperature: float


class AirGroundTemperatureData(AirGroundTemperatureDataBase):
    ag_temperature_data_uid: int


class TemperaturePressureDataBase(BaseModelConfig):
    logger_uid: int
    logger_download_uid: int
    installation_uid: int
    date_time: dt.datetime
    temperature: float
    pressure: float


class TemperaturePressureData(TemperaturePressureDataBase):
    temperature_pressure_data_uid: int

"""
class GroundSurfaceTemperatureDataBase(BaseModelConfig):
    logger_uid: int
    logger_download_uid: int
    installation_uid: int
    date_time: dt.datetime
    temperature: float


class GroundSurfaceTemperatureData(GroundSurfaceTemperatureDataBase):
    ground_surface_temperature_data_uid: int
"""