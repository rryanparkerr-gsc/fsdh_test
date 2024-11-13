# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-10
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes

from app.database import Base


class FourChannelSensor(Base):
    __tablename__ = "four_channel_sensor"
    four_channel_sensor_uid = Column(sqltypes.Integer, primary_key=True)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    date_installed = Column(sqltypes.DateTime(timezone=True), nullable=False)
    depth = Column(sqltypes.Float, nullable=False)
    channel_number = Column(sqltypes.Integer, nullable=False)

    def __init__(self, installation_uid, date_installed, depth, channel_number):
        self.installation_uid = installation_uid
        self.date_installed = date_installed
        self.depth = depth
        self.channel_number = channel_number
        return


class FourChannelData(Base):
    __tablename__ = "four_channel_data"
    four_channel_data_uid = Column(sqltypes.Integer, primary_key=True)
    logger_uid = Column(sqltypes.Integer, ForeignKey("logger.logger_uid"), nullable=False)
    logger_download_uid = Column(sqltypes.Integer, ForeignKey("logger_download.logger_download_uid"), nullable=False)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    four_channel_sensor_uid = Column(sqltypes.Integer, ForeignKey("four_channel_sensor.four_channel_sensor_uid"),
                                     nullable=False)
    date_time = Column(sqltypes.DateTime(timezone=True), nullable=False)
    temperature = Column(sqltypes.Float, nullable=False)

    def __init__(self, logger_uid, logger_download_uid, installation_uid, four_channel_sensor_uid, date_time,
                 temperature):
        self.logger_uid = logger_uid
        self.logger_download_uid = logger_download_uid
        self.installation_uid = installation_uid
        self.four_channel_sensor_uid = four_channel_sensor_uid
        self.date_time = date_time
        self.temperature = temperature
        return
