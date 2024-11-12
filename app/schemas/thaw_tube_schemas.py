# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-07
"""

import datetime as dt

from .base_model import BaseModelConfig


class ThawTubeBase(BaseModelConfig):
    installation_uid: int
    date_installed: dt.datetime
    status: str | None


class ThawTube(ThawTubeBase):
    thaw_tube_uid: int


class ThawTubeReadingBase(BaseModelConfig):
    thaw_tube_uid: int
    installation_visit_uid: int
    scribe_curr: float | None
    scribe_max: float | None
    scribe_min: float | None
    scribe_height: float | None
    tube_height: float | None
    water_depth: float | None
    ice_depth: float | None
    stopper_to_plug: float | None
    stopper_push: float | None
    stopper_on_plug: bool
    new_bead_in: bool


class ThawTubeReading(ThawTubeReadingBase):
    thaw_tube_reading_uid: int


class ThawTubeBeadMeasurementBase(BaseModelConfig):
    thaw_tube_reading_uid: int
    thaw_tube_uid: int
    colour: str
    year: int
    depth: float
    depth_min: float | None
    depth_max: float | None


class ThawTubeBeadMeasurement(ThawTubeBeadMeasurementBase):
    thaw_tube_bead_measurement_uid: int


class ThawTubeBeadColourYearBase(BaseModelConfig):
    year: int
    colour: str


class ThawTubeBeadColourYear(ThawTubeBeadColourYearBase):
    bcy_uid: int


class ThawTubeReferenceBase(BaseModelConfig):
    thaw_tube_uid: int
    date: dt.datetime
    reference_measurement: float


class ThawTubeReference(ThawTubeReferenceBase):
    thaw_tube_reference_uid: int
