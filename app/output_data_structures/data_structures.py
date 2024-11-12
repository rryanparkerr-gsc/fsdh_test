# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-11-03
"""


import datetime as dt


class CableLoggerDataOutput:
    date_time: dt.datetime
    temperature: float
    logger_sn: str
    sensor_number: int
    sensor_depth: float

    def __init__(self, date_time, temperature, logger_sn, sensor_number, sensor_depth):
        self.date_time = date_time
        self.temperature = temperature
        self.logger_sn = logger_sn
        self.sensor_number = sensor_number
        self.sensor_depth = sensor_depth
        return


class CableManualReadOutput:
    date_time: dt.datetime
    resistance: int
    ol: bool
    drift_up: bool
    drift_down: bool
    sensor_number: int
    depth: float
    sensor_type: str

    def __init__(self, date_time, resistance, ol, drift_up, drift_down, sensor_number, depth, sensor_type):
        self.date_time = date_time
        self.sensor_number = sensor_number
        self.depth = depth
        self.resistance = resistance
        self.ol = ol
        self.drift_up = drift_up
        self.drift_down = drift_down
        self.sensor_type = sensor_type
        return


class AGLoggerDataOutput:
    date_time: dt.datetime
    temperature: float
    logger_sn: str
    sensor_number: int

    def __init__(self, date_time, temperature, logger_sn, sensor_number):
        self.date_time = date_time
        self.temperature = temperature
        self.logger_sn = logger_sn
        self.sensor_number = sensor_number
        return


class SurveyInfoBase:
    installation_code: str
    installation_name: str
    label: str
    notes: str | None

    def __init__(self, installation_code, installation_name, label, notes):
        self.installation_code = installation_code
        self.installation_name = installation_name
        self.label = label
        self.notes = notes


class SurveyInfoCable(SurveyInfoBase):
    sensor1: str | None
    sensor2: str | None
    sensor3: str | None
    sensor4: str | None
    sensor5: str | None
    sensor6: str | None
    sensor7: str | None
    sensor8: str | None

    def __init__(self, installation_code, installation_name, label, notes, sensor1, sensor2, sensor3, sensor4, sensor5,
                 sensor6, sensor7, sensor8):
        super().__init__(installation_code, installation_name, label, notes)
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.sensor3 = sensor3
        self.sensor4 = sensor4
        self.sensor5 = sensor5
        self.sensor6 = sensor6
        self.sensor7 = sensor7
        self.sensor8 = sensor8

