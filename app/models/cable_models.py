# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-07
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes

from database import Base


class Cable(Base):
    __tablename__ = "cable"
    cable_uid = Column(sqltypes.Integer, primary_key=True)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    connector_type = Column(sqltypes.String, nullable=False)
    length = Column(sqltypes.Float, nullable=False)
    num_sensors = Column(sqltypes.Integer, nullable=False)
    borehole_depth = Column(sqltypes.Float)

    def __init__(self, installation_uid, connector_type, length, num_sensors, borehole_depth):
        self.installation_uid = installation_uid
        self.connector_type = connector_type
        self.length = length
        self.num_sensors = num_sensors
        self.borehole_depth = borehole_depth
        return


class CableSensor(Base):
    __tablename__ = "cable_sensor"
    cable_sensor_uid = Column(sqltypes.Integer, primary_key=True)
    cable_uid = Column(sqltypes.Integer, ForeignKey("cable.cable_uid"), nullable=False)
    date_installed = Column(sqltypes.DateTime(timezone=True))
    depth = Column(sqltypes.Float, nullable=False)
    sensor_type = Column(sqltypes.String, nullable=False)
    number_in_chain = Column(sqltypes.Integer, nullable=False)

    def __init__(self, cable_uid, date_installed, depth, sensor_type, number_in_chain):
        self.cable_uid = cable_uid
        self.date_installed = date_installed
        self.depth = depth
        self.sensor_type = sensor_type
        self.number_in_chain = number_in_chain
        return


class CableLoggerData(Base):
    __tablename__ = "cable_logger_data"
    cable_logger_data_uid = Column(sqltypes.Integer, primary_key=True)
    logger_uid = Column(sqltypes.Integer, ForeignKey("logger.logger_uid"), nullable=False)
    logger_download_uid = Column(sqltypes.Integer, ForeignKey("logger_download.logger_download_uid"), nullable=False)
    cable_sensor_uid = Column(sqltypes.Integer, ForeignKey("cable_sensor.cable_sensor_uid"), nullable=False)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    date_time = Column(sqltypes.DateTime(timezone=True), nullable=False)
    temperature = Column(sqltypes.Float, nullable=False)

    def __init__(self, logger_uid, logger_download_uid, cable_sensor_uid, installation_uid, date_time, temperature):
        self.logger_uid = logger_uid
        self.logger_download_uid = logger_download_uid
        self.cable_sensor_uid = cable_sensor_uid
        self.installation_uid = installation_uid
        self.date_time = date_time
        self.temperature = temperature
        return


class CableManualRead(Base):
    __tablename__ = "cable_manual_read"
    cable_manual_read_uid = Column(sqltypes.Integer, primary_key=True)
    cable_sensor_uid = Column(sqltypes.Integer, ForeignKey("cable_sensor.cable_sensor_uid"), nullable=False)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    installation_visit_uid = Column(sqltypes.Integer, ForeignKey("installation_visit.installation_visit_uid"),
                                    nullable=False)
    temperature = Column(sqltypes.Float)
    ol = Column(sqltypes.Boolean)
    drift_up = Column(sqltypes.Boolean)
    drift_down = Column(sqltypes.Boolean)

    def __init__(self, cable_sensor_uid, installation_uid, installation_visit_uid, temperature, ol, drift_up,
                 drift_down):
        self.cable_sensor_uid = cable_sensor_uid
        self.installation_uid = installation_uid
        self.installation_visit_uid = installation_visit_uid
        self.temperature = temperature
        self.ol = ol
        self.drift_up = drift_up
        self.drift_down = drift_down
        return


class StickUp(Base):
    __tablename__ = "stick_up"
    stick_up_uid = Column(sqltypes.Integer, primary_key=True)
    installation_visit_uid = Column(sqltypes.Integer, ForeignKey("installation_visit.installation_visit_uid"),
                                    nullable=False)
    measurement = Column(sqltypes.Float, nullable=False)
    reference = Column(sqltypes.String)

    def __init__(self, installation_visit_uid, measurement, reference):
        self.installation_visit_uid = installation_visit_uid
        self.measurement = measurement
        self.reference = reference
        return


class CableSensorMapping(Base):
    __tablename__ = "cable_sensor_mapping"
    cable_sensor_mapping_uid = Column(sqltypes.Integer, primary_key=True)
    cable_uid = Column(sqltypes.Integer, ForeignKey("cable.cable_uid"), nullable=False)
    cable_sensor_uid = Column(sqltypes.Integer, ForeignKey("cable_sensor.cable_sensor_uid"), nullable=False)
    mapping_1 = Column(sqltypes.String, nullable=False)
    mapping_2 = Column(sqltypes.String)

    def __init__(self, cable_uid, cable_sensor_uid, mapping_1, mapping_2=None):
        self.cable_uid = cable_uid
        self.cable_sensor_uid = cable_sensor_uid
        self.mapping_1 = mapping_1
        self.mapping_2 = mapping_2
        return
