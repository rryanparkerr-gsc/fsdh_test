# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-10
"""

import datetime as dt

from .base_model import BaseModelConfig


class FourChannelSensorBase(BaseModelConfig):
    installation_uid: int
    date_installed: dt.datetime
    depth: float
    channel_number: int


class FourChannelSensor(FourChannelSensorBase):
    four_channel_sensor_uid: int


class FourChannelDataBase(BaseModelConfig):
    logger_uid: int
    logger_download_uid: int
    installation_uid: int
    four_channel_sensor_uid: int
    date_time: dt.datetime
    temperature: float


class FourChannelData(FourChannelDataBase):
    four_channel_data_uid: int
