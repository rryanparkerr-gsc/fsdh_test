# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-06-28
"""

from sqlalchemy.orm import Session, aliased
import datetime as dt

from app import schemas
from app import models


def add_thaw_tube_bead_colour_year(db: Session, bead_colour_year: schemas.ThawTubeBeadColourYearBase):
    new_bead_colour_year = models.ThawTubeBeadColourYear(year=bead_colour_year.year, colour=bead_colour_year.colour)
    db.add(new_bead_colour_year)
    db.commit()
    db.refresh(new_bead_colour_year)
    return new_bead_colour_year


def get_thaw_tube_bead_by_year(db: Session, year: int):
    return db.query(models.ThawTubeBeadColourYear).filter(models.ThawTubeBeadColourYear.year == year).first()


def get_thaw_tube_bead_by_colour(db: Session, colour: str):
    return db.query(models.ThawTubeBeadColourYear).filter(models.ThawTubeBeadColourYear.colour == colour).first()


def get_thaw_tube_by_installation_uid(db: Session, installation_uid: int):
    return db.query(models.ThawTube).filter(models.ThawTube.installation_uid == installation_uid).first()


def add_thaw_tube(db: Session, thaw_tube: schemas.ThawTubeBase):
    new_thaw_tube = models.ThawTube(installation_uid=thaw_tube.installation_uid,
                                    date_installed=thaw_tube.date_installed.replace(microsecond=0),
                                    status=thaw_tube.status)
    db.add(new_thaw_tube)
    db.commit()
    db.refresh(new_thaw_tube)
    return new_thaw_tube


def get_thaw_tube_reading_by_installation_visit_uid(db: Session, installation_visit_uid: int):
    return db.query(models.ThawTubeReading) \
        .filter(models.ThawTubeReading.installation_visit_uid == installation_visit_uid).first()


def add_thaw_tube_reading(db: Session, thaw_tube_reading: schemas.ThawTubeReadingBase):
    new_thaw_tube_reading = models.ThawTubeReading(thaw_tube_uid=thaw_tube_reading.thaw_tube_uid,
                                                   installation_visit_uid=thaw_tube_reading.installation_visit_uid,
                                                   scribe_curr=thaw_tube_reading.scribe_curr,
                                                   scribe_max=thaw_tube_reading.scribe_max,
                                                   scribe_min=thaw_tube_reading.scribe_min,
                                                   scribe_height=thaw_tube_reading.scribe_height,
                                                   tube_height=thaw_tube_reading.tube_height,
                                                   water_depth=thaw_tube_reading.water_depth,
                                                   ice_depth=thaw_tube_reading.ice_depth,
                                                   stopper_to_plug=thaw_tube_reading.stopper_to_plug,
                                                   stopper_push=thaw_tube_reading.stopper_push,
                                                   stopper_on_plug=thaw_tube_reading.stopper_on_plug,
                                                   new_bead_in=thaw_tube_reading.new_bead_in)
    db.add(new_thaw_tube_reading)
    db.commit()
    db.refresh(new_thaw_tube_reading)
    return new_thaw_tube_reading


def add_thaw_tube_bead_measurement(db: Session, bead_measurement: schemas.ThawTubeBeadMeasurementBase):
    new_bead_measurement = models.ThawTubeBeadMeasurement(thaw_tube_reading_uid=bead_measurement.thaw_tube_reading_uid,
                                                          thaw_tube_uid=bead_measurement.thaw_tube_uid,
                                                          colour=bead_measurement.colour,
                                                          year=bead_measurement.year,
                                                          depth=bead_measurement.depth,
                                                          depth_min=bead_measurement.depth_min,
                                                          depth_max=bead_measurement.depth_max)
    db.add(new_bead_measurement)
    db.commit()
    db.refresh(new_bead_measurement)
    return new_bead_measurement


def get_thaw_tube_bead_measurement_by_reading_uid_and_bead_year(db: Session, thaw_tube_reading_uid: int,
                                                                bead_year: int):
    return db.query(models.ThawTubeBeadMeasurement)\
        .filter((models.ThawTubeBeadMeasurement.thaw_tube_reading_uid == thaw_tube_reading_uid)
                & (models.ThawTubeBeadMeasurement.year == bead_year)).first()


def get_all_readings_of_thaw_tube_by_thaw_tube_uid(db: Session, thaw_tube_uid: int):
    return db.query(models.ThawTubeReading).filter(models.ThawTubeReading.thaw_tube_uid == thaw_tube_uid).all()


def get_all_thaw_tube_bead_measurements_by_reading_uid(db: Session, thaw_tube_reading_uid: int):
    return db.query(models.ThawTubeBeadMeasurement)\
        .filter(models.ThawTubeBeadMeasurement.thaw_tube_reading_uid == thaw_tube_reading_uid).all()


def get_thaw_tube_reference_by_thaw_tube_uid_and_date(db: Session, thaw_tube_uid: int, date: dt.datetime):
    return db.query(models.ThawTubeReference)\
        .filter((models.ThawTubeReference.date == date)
                & (models.ThawTubeReference.thaw_tube_uid == thaw_tube_uid)).first()


def get_all_thaw_tube_references_for_thaw_tube_uid(db: Session, thaw_tube_uid: int):
    return db.query(models.ThawTubeReference)\
        .filter(models.ThawTubeReference.thaw_tube_uid == thaw_tube_uid).all()


def add_thaw_tube_reference(db: Session, thaw_tube_reference: schemas.ThawTubeReferenceBase):
    new_reference = models.ThawTubeReference(thaw_tube_uid=thaw_tube_reference.thaw_tube_uid,
                                             date=thaw_tube_reference.date.replace(microsecond=0),
                                             reference_measurement=thaw_tube_reference.reference_measurement)
    db.add(new_reference)
    db.commit()
    db.refresh(new_reference)
    return new_reference


def get_thaw_tube_readings_at_installation(db: Session, installation_uid: int):
    return db.query(models.InstallationVisit.visit_date,
                    models.InstallationVisit.field_party,
                    models.InstallationVisit.record_of_activities,
                    models.InstallationVisit.notes,
                    models.ThawTubeReading.thaw_tube_reading_uid,
                    models.ThawTubeReading.tube_height,
                    models.ThawTubeReading.ice_depth,
                    models.ThawTubeReading.scribe_min,
                    models.ThawTubeReading.scribe_curr,
                    models.ThawTubeReading.scribe_max)\
        .join(models.ThawTubeReading)\
        .filter(models.InstallationVisit.installation_uid == installation_uid).all()


def get_thaw_tube_bead_history(db: Session, thaw_tube_uid: int):
    return db.query(models.ThawTubeBeadMeasurement.year,
                    models.ThawTubeBeadMeasurement.colour,
                    models.ThawTubeBeadMeasurement.depth,
                    models.ThawTubeBeadMeasurement.depth_max,
                    models.ThawTubeBeadMeasurement.depth_min,
                    models.ThawTubeReading.installation_visit_uid) \
        .join(models.ThawTubeReading) \
        .filter(models.ThawTubeBeadMeasurement.thaw_tube_uid == thaw_tube_uid).all()
