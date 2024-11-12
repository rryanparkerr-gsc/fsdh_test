# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-07
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes
from sqlalchemy.orm import relationship

from database import Base


class ThawTube(Base):
    __tablename__ = "thaw_tube"
    thaw_tube_uid = Column(sqltypes.Integer, primary_key=True)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    date_installed = Column(sqltypes.DateTime(timezone=True), nullable=False)
    status = Column(sqltypes.String)

    def __init__(self, installation_uid, date_installed, status):
        self.installation_uid = installation_uid
        self.date_installed = date_installed
        self.status = status
        return


class ThawTubeReading(Base):
    __tablename__ = "thaw_tube_reading"
    thaw_tube_reading_uid = Column(sqltypes.Integer, primary_key=True)
    thaw_tube_uid = Column(sqltypes.Integer, ForeignKey("thaw_tube.thaw_tube_uid"), nullable=False)
    installation_visit_uid = Column(sqltypes.Integer, ForeignKey("installation_visit.installation_visit_uid"),
                                    nullable=False)
    scribe_curr = Column(sqltypes.Float)
    scribe_max = Column(sqltypes.Float)
    scribe_min = Column(sqltypes.Float)
    scribe_height = Column(sqltypes.Float)
    tube_height = Column(sqltypes.Float)
    water_depth = Column(sqltypes.Float)
    ice_depth = Column(sqltypes.Float)
    stopper_to_plug = Column(sqltypes.Float)
    stopper_push = Column(sqltypes.Float)
    stopper_on_plug = Column(sqltypes.Boolean)
    new_bead_in = Column(sqltypes.Boolean, nullable=False)

    def __init__(self, thaw_tube_uid, installation_visit_uid, scribe_curr, scribe_max, scribe_min, scribe_height,
                 tube_height, water_depth, ice_depth, stopper_to_plug, stopper_push, stopper_on_plug, new_bead_in):
        self.thaw_tube_uid = thaw_tube_uid
        self.installation_visit_uid = installation_visit_uid
        self.scribe_curr = scribe_curr
        self.scribe_max = scribe_max
        self.scribe_min = scribe_min
        self.scribe_height = scribe_height
        self.tube_height = tube_height
        self.water_depth = water_depth
        self.ice_depth = ice_depth
        self.stopper_to_plug = stopper_to_plug
        self.stopper_push = stopper_push
        self.stopper_on_plug = stopper_on_plug
        self.new_bead_in = new_bead_in
        return


class ThawTubeBeadMeasurement(Base):
    __tablename__ = "thaw_tube_bead_measurement"
    thaw_tube_bead_measurement_uid = Column(sqltypes.Integer, primary_key=True)
    thaw_tube_reading_uid = Column(sqltypes.Integer, ForeignKey("thaw_tube_reading.thaw_tube_reading_uid"),
                                   nullable=False)
    thaw_tube_uid = Column(sqltypes.Integer, ForeignKey("thaw_tube.thaw_tube_uid"), nullable=False)
    colour = Column(sqltypes.String, nullable=False)
    year = Column(sqltypes.Integer, nullable=False)
    depth = Column(sqltypes.Float, nullable=False)
    depth_min = Column(sqltypes.Float)
    depth_max = Column(sqltypes.Float)

    def __init__(self, thaw_tube_reading_uid, thaw_tube_uid, colour, year, depth, depth_min, depth_max):
        self.thaw_tube_reading_uid = thaw_tube_reading_uid
        self.thaw_tube_uid = thaw_tube_uid
        self.colour = colour
        self.year = year
        self.depth = depth
        self.depth_min = depth_min
        self.depth_max = depth_max
        return


class ThawTubeBeadColourYear(Base):
    __tablename__ = "thaw_tube_bead_colour_years"
    bcy_uid = Column(sqltypes.Integer, primary_key=True)
    year = Column(sqltypes.Integer, nullable=False)
    colour = Column(sqltypes.String, nullable=False)

    def __init__(self, year, colour):
        self.year = year
        self.colour = colour
        return


class ThawTubeReference(Base):
    __tablename__ = "thaw_tube_reference"
    thaw_tube_reference_uid = Column(sqltypes.Integer, primary_key=True)
    thaw_tube_uid = Column(sqltypes.Integer, ForeignKey("thaw_tube.thaw_tube_uid"), nullable=False)
    date = Column(sqltypes.DateTime(timezone=True), nullable=False)
    reference_measurement = Column(sqltypes.Float, nullable=False)

    def __init__(self, thaw_tube_uid, date, reference_measurement):
        self.thaw_tube_uid = thaw_tube_uid
        self.date = date
        self.reference_measurement = reference_measurement
        return
