# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-07
"""

import datetime as dt

from .base_model import BaseModelConfig


class SiteBase(BaseModelConfig):
    site_name: str
    site_code: str
    latitude: float
    longitude: float
    region: str
    approach: str | None = None
    notes: str | None = None


class Site(SiteBase):
    site_uid: int


class InstallationBase(BaseModelConfig):
    site_uid: int
    installation_code: str
    installation_name: str
    installation_type: str
    latitude: float
    longitude: float
    notes: str | None
    status: str | None


class Installation(InstallationBase):
    installation_uid: int


class InstallationVisitBase(BaseModelConfig):
    installation_uid: int
    record_of_activities: str
    visit_date: dt.datetime
    field_party: str
    notes: str | None


class InstallationVisit(InstallationVisitBase):
    installation_visit_uid: int


class ALProbeMeasurementBase(BaseModelConfig):
    installation_visit_uid: int
    probe_number: int
    measurement: float
    probe_maxed: bool


class ALProbeMeasurement(ALProbeMeasurementBase):
    al_probe_measurement_uid: int


class LoggerDeploymentBase(BaseModelConfig):
    installation_uid: int
    logger_uid: int
    deployment_visit_uid: int | None
    extraction_visit_uid: int | None


class LoggerDeployment(LoggerDeploymentBase):
    logger_deployment_uid: int


class LoggerBase(BaseModelConfig):
    logger_serial_number: str
    logger_type: str
    battery_year: int | None
    asset_tag: str | None


class Logger(LoggerBase):
    logger_uid: int


class LoggerDownloadBase(BaseModelConfig):
    logger_uid: int
    logger_deployment_uid: int
    download_date: dt.datetime
    download_quality: str


class LoggerDownload(LoggerDownloadBase):
    logger_download_uid: int


class InstallationPairBase(BaseModelConfig):
    installation_uid_1: int
    installation_uid_2: int


class InstallationPair(InstallationPairBase):
    installation_pair_uid: int


class DumpInputSchema(BaseModelConfig):
    year: int | None
    region: str | list[str] | None
