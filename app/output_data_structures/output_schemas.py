# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-11-03
"""


import datetime as dt

from app.schemas.base_model import BaseModelConfig


class CableLoggerDataOutput(BaseModelConfig):
    date_time: dt.datetime
    temperature: float
    logger_sn: str
    sensor_number: int
    sensor_depth: float


class CableManualReadOutput(BaseModelConfig):
    date_time: dt.datetime
    resistance: int
    ol: bool
    drift_up: bool
    drift_down: bool
    sensor_number: int
    depth: float
    sensor_type: str


class AGLoggerDataOutput(BaseModelConfig):
    date_time: dt.datetime
    temperature: float
    logger_sn: str
    sensor_number: int


class MultiSensorTimeSeriesAverageData(BaseModelConfig):
    date: dt.datetime
    sensor_1_temp: float
    sensor_1_depth: float
    sensor_2_temp: float | None
    sensor_2_depth: float | None
    sensor_3_temp: float | None
    sensor_3_depth: float | None
    sensor_4_temp: float | None
    sensor_4_depth: float | None
    sensor_5_temp: float | None
    sensor_5_depth: float | None
    sensor_6_temp: float | None
    sensor_6_depth: float | None
    sensor_7_temp: float | None
    sensor_7_depth: float | None
    sensor_8_temp: float | None
    sensor_8_depth: float | None
    sensor_9_temp: float | None
    sensor_9_depth: float | None
    sensor_10_temp: float | None
    sensor_10_depth: float | None
    sensor_11_temp: float | None
    sensor_11_depth: float | None
    sensor_12_temp: float | None
    sensor_12_depth: float | None
    sensor_13_temp: float | None
    sensor_13_depth: float | None
    sensor_14_temp: float | None
    sensor_14_depth: float | None
    sensor_15_temp: float | None
    sensor_15_depth: float | None


class SingleSensorTimeSeriesAverageData(BaseModelConfig):
    date: dt.datetime
    temperature: float


class InstallationLoggerHistory(BaseModelConfig):
    date_time: dt.datetime
    recorded_by: str
    activity: str
    logger_in: str | None
    logger_in_type: str | None
    logger_out: str | None
    logger_out_type: str | None
    notes: str | None
    stick_up: float | None


class ThawTubeHistory(BaseModelConfig):
    date_time: dt.datetime
    recorded_by: str
    activity: str
    notes: str | None
    tube_height: float | None
    ice_depth: float | None
    scribe_min: float | None
    scribe_curr: float | None
    scribe_max: float | None
    previous_year_bead_depth: float | None
    thaw_penetration: float | None
    max_active_layer: float | None
    surface_change: float | None


class ThawTubeBeadHistory(BaseModelConfig):
    bead_year: int
    bead_colour: str
    depth: float
    depth_max: float | None
    depth_min: float | None
    date_time: dt.datetime


class ALProbeHistory(BaseModelConfig):
    date_time: dt.datetime
    probe_depth: float
    probe_maxed: bool
    probe_number: int


class SurveyInfo(BaseModelConfig):
    installation_code: str
    installation_name: str
    label: str
    logger_sn: str | None
    logger_type: str | None
    connector: str | None
    notes: str | None
    sensor1: str | None
    sensor2: str | None
    sensor3: str | None
    sensor4: str | None
    sensor5: str | None
    sensor6: str | None
    sensor7: str | None
    sensor8: str | None


class Dump(BaseModelConfig):
    recorded_by: str
    visit_date: dt.datetime
    record_of_activities: str
    notes: str | None
    installation_name: str
    installation_code: str
    installation_type: str
    latitude: float
    longitude: float
    logger_deployed: str | None
    logger_type_deployed: str | None
    logger_deployed_battery_year: int | None
    logger_extracted: str | None
    logger_type_extracted: str | None
    connector_type: str | None
    stick_up: float | None


class ReadableLoggerDeployments(BaseModelConfig):
    logger_deployment_uid: int
    installation_code: str
    logger_sn: str
    deployment_date: dt.datetime | None
    extraction_date: dt.datetime | None
    deployment_notes: str | None
