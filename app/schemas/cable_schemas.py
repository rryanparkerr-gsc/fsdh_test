# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-07
"""

import datetime as dt

from .base_model import BaseModelConfig


class CableBase(BaseModelConfig):
    installation_uid: int
    connector_type: str
    length: float
    num_sensors: int
    borehole_depth: float | None


class Cable(CableBase):
    cable_uid: int


class CableSensorBase(BaseModelConfig):
    cable_uid: int
    date_installed: dt.datetime
    depth: float
    sensor_type: str
    number_in_chain: int


class CableSensor(CableSensorBase):
    cable_sensor_uid: int


class CableLoggerDataBase(BaseModelConfig):
    logger_uid: int
    logger_download_uid: int
    cable_sensor_uid: int
    installation_uid: int
    date_time: dt.datetime
    temperature: float


class CableLoggerData(CableLoggerDataBase):
    cable_logger_data_uid: int


class CableManualReadBase(BaseModelConfig):
    cable_sensor_uid: int
    installation_uid: int
    installation_visit_uid: int
    ol: bool | None
    drift_up: bool | None
    drift_down: bool | None


class CableManualReadInput(CableManualReadBase):
    temperature: float | None
    resistance: int | None


class CableManualRead(CableManualReadBase):
    cable_manual_read_uid: int
    temperature: float


class StickUpBase(BaseModelConfig):
    installation_visit_uid: int
    measurement: float
    reference: str | None


class StickUp(StickUpBase):
    stick_up_uid: int


class CableSensorMappingBase(BaseModelConfig):
    cable_uid: int
    cable_sensor_uid: int
    mapping_1: str
    mapping_2: str | None


class CableSensorMapping(CableSensorMappingBase):
    cable_sensor_mapping_uid: int
