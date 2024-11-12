# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-07
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes

from database import Base


class Site(Base):
    __tablename__ = "site"
    site_uid = Column(sqltypes.Integer, primary_key=True)
    site_name = Column(sqltypes.String, nullable=False)
    site_code = Column(sqltypes.String, nullable=False)
    latitude = Column(sqltypes.Float, nullable=False)
    longitude = Column(sqltypes.Float, nullable=False)
    region = Column(sqltypes.String, nullable=False)
    approach = Column(sqltypes.String)
    notes = Column(sqltypes.String)

    def __init__(self, name, code, latitude, longitude, region, approach, notes):
        self.site_name = name
        self.site_code = code
        if -90 <= latitude <= 90:
            self.latitude = latitude
        else:
            raise ValueError("Latitude value is invalid")
        if -180 <= longitude <= 180:
            self.longitude = longitude
        else:
            raise ValueError("Longitude value is invalid")
        self.region = region
        self.approach = approach
        self.notes = notes
        return


class Installation(Base):
    __tablename__ = "installation"
    installation_uid = Column(sqltypes.Integer, primary_key=True)
    installation_code = Column(sqltypes.String, nullable=False)
    installation_name = Column(sqltypes.String, nullable=False)
    installation_type = Column(sqltypes.String, nullable=False)
    latitude = Column(sqltypes.Float)
    longitude = Column(sqltypes.Float)
    site_uid = Column(sqltypes.Integer, ForeignKey("site.site_uid"),  nullable=False)
    notes = Column(sqltypes.String)
    status = Column(sqltypes.String)

    def __init__(self, installation_code, site_uid, installation_name, installation_type, latitude, longitude, notes,
                 status):
        self.installation_code = installation_code
        self.installation_name = installation_name
        self.installation_type = installation_type
        self.site_uid = site_uid
        self.latitude = latitude
        self.longitude = longitude
        self.notes = notes
        self.status = status
        return


class InstallationVisit(Base):
    __tablename__ = "installation_visit"
    installation_visit_uid = Column(sqltypes.Integer, primary_key=True)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"),  nullable=False)
    record_of_activities = Column(sqltypes.String,  nullable=False)
    visit_date = Column(sqltypes.DateTime(timezone=True), nullable=False)
    field_party = Column(sqltypes.String,  nullable=False)
    notes = Column(sqltypes.String)

    def __init__(self, installation_uid, roa, visit_dt, party, notes):
        self.installation_uid = installation_uid
        self.record_of_activities = roa
        self.visit_date = visit_dt
        self.field_party = party
        self.notes = notes
        return


class ALProbeMeasurement(Base):
    __tablename__ = "active_layer_probe_measurement"
    al_probe_measurement_uid = Column(sqltypes.Integer, primary_key=True)
    installation_visit_uid = Column(sqltypes.Integer, ForeignKey("installation_visit.installation_visit_uid"),
                                    nullable=False)
    probe_number = Column(sqltypes.Integer, nullable=False)
    measurement = Column(sqltypes.Float, nullable=False)
    probe_maxed = Column(sqltypes.Boolean, nullable=False)

    def __init__(self, installation_visit_uid, probe_number, measurement, probe_maxed):
        self.installation_visit_uid = installation_visit_uid
        self.probe_number = probe_number
        self.measurement = measurement
        self.probe_maxed = probe_maxed
        return


class LoggerDeployment(Base):
    __tablename__ = "logger_deployment"
    logger_deployment_uid = Column(sqltypes.Integer, primary_key=True)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"),  nullable=False)
    logger_uid = Column(sqltypes.Integer, ForeignKey("logger.logger_uid"),  nullable=False)
    deployment_visit_uid = Column(sqltypes.Integer, ForeignKey("installation_visit.installation_visit_uid"))
    extraction_visit_uid = Column(sqltypes.Integer, ForeignKey("installation_visit.installation_visit_uid"))

    def __init__(self, installation_uid, logger_uid, deployment_visit_uid, extraction_visit_uid):
        self.installation_uid = installation_uid
        self.logger_uid = logger_uid
        self.deployment_visit_uid = deployment_visit_uid
        self.extraction_visit_uid = extraction_visit_uid
        return


class Logger(Base):
    __tablename__ = "logger"
    logger_uid = Column(sqltypes.Integer, primary_key=True)
    logger_serial_number = Column(sqltypes.String,  nullable=False)
    logger_type = Column(sqltypes.String,  nullable=False)
    battery_year = Column(sqltypes.Integer)
    asset_tag = Column(sqltypes.String)

    def __init__(self, logger_serial_number, logger_type, battery_year, asset_tag):
        self.logger_serial_number = logger_serial_number
        self.logger_type = logger_type
        self.battery_year = battery_year
        self.asset_tag = asset_tag
        return


class LoggerDownload(Base):
    __tablename__ = "logger_download"
    logger_download_uid = Column(sqltypes.Integer, primary_key=True)
    logger_uid = Column(sqltypes.Integer, ForeignKey("logger.logger_uid"), nullable=False)
    logger_deployment_uid = Column(sqltypes.Integer, ForeignKey("logger_deployment.logger_deployment_uid"),
                                   nullable=False)
    download_date = Column(sqltypes.DateTime(timezone=True), nullable=False)
    download_quality = Column(sqltypes.String,  nullable=False)

    def __init__(self, logger_uid, logger_deployment_uid, download_date, download_quality):
        self.logger_uid = logger_uid
        self.logger_deployment_uid = logger_deployment_uid
        self.download_date = download_date
        self.download_quality = download_quality
        return


class InstallationPair(Base):
    __tablename__ = "installation_pair"
    installation_pair_uid = Column(sqltypes.Integer, primary_key=True)
    installation_uid_1 = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"),  nullable=False)
    installation_uid_2 = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)

    def __init__(self, installation_uid_1, installation_uid_2):
        self.installation_uid_1 = installation_uid_1
        self.installation_uid_2 = installation_uid_2
        return



