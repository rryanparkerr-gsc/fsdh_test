# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-10
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes

from database import Base


class AirGroundTemperatureData(Base):
    __tablename__ = "air_ground_temperature_data"
    ag_temperature_data_uid = Column(sqltypes.Integer, primary_key=True)
    logger_uid = Column(sqltypes.Integer, ForeignKey("logger.logger_uid"), nullable=False)
    logger_download_uid = Column(sqltypes.Integer, ForeignKey("logger_download.logger_download_uid"), nullable=False)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    date_time = Column(sqltypes.DateTime(timezone=True), nullable=False)
    channel_number = Column(sqltypes.Integer, nullable=False)
    temperature = Column(sqltypes.Float, nullable=False)

    def __init__(self, logger_uid, logger_download_uid, installation_uid, date_time, channel_number, temperature):
        self.logger_uid = logger_uid
        self.logger_download_uid = logger_download_uid
        self.installation_uid = installation_uid
        self.date_time = date_time
        self.channel_number = channel_number
        self.temperature = temperature
        return


class TemperaturePressureData(Base):
    __tablename__ = "temperature_pressure_data"
    temperature_pressure_data_uid = Column(sqltypes.Integer, primary_key=True)
    logger_uid = Column(sqltypes.Integer, ForeignKey("logger.logger_uid"), nullable=False)
    logger_download_uid = Column(sqltypes.Integer, ForeignKey("logger_download.logger_download_uid"), nullable=False)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    date_time = Column(sqltypes.DateTime(timezone=True), nullable=False)
    temperature = Column(sqltypes.Float, nullable=False)
    pressure = Column(sqltypes.Float, nullable=False)

    def __init__(self, logger_uid, logger_download_uid, installation_uid, date_time, temperature, pressure):
        self.logger_uid = logger_uid
        self.logger_download_uid = logger_download_uid
        self.installation_uid = installation_uid
        self.date_time = date_time
        self.temperature = temperature
        self.pressure = pressure
        return

"""
class GroundSurfaceTemperatureData(Base):
    __tablename__ = "ground_surface_temperature_data"
    ground_surface_temperature_data_uid = Column(sqltypes.Integer, primary_key=True)
    logger_uid = Column(sqltypes.Integer, ForeignKey("logger.logger_uid"), nullable=False)
    logger_download_uid = Column(sqltypes.Integer, ForeignKey("logger_download.logger_download_uid"), nullable=False)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    date_time = Column(sqltypes.DateTime(timezone=True), nullable=False)
    temperature = Column(sqltypes.Float, nullable=False)

    def __init__(self, logger_uid, logger_download_uid, installation_uid, date_time, temperature):
        self.logger_uid = logger_uid
        self.logger_download_uid = logger_download_uid
        self.installation_uid = installation_uid
        self.date_time = date_time
        self.temperature = temperature
        return
"""
