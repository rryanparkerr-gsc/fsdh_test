# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-06-28
"""
import numpy as np
import pandas as pd
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import datetime as dt

from app import schemas
from app import crud
from .api import app, get_db, check_tz_aware
from app.output_data_structures import output_schemas as ods_schemas


@app.post("/thaw_tube_bead_colour_years/", response_model=schemas.ThawTubeBeadColourYear)
async def add_thaw_tube_bead_colour_year(bead_colour_year: schemas.ThawTubeBeadColourYearBase,
                                         db: Session = Depends(get_db)):
    db_bead_colour = crud.get_thaw_tube_bead_by_year(db=db, year=bead_colour_year.year)
    if db_bead_colour:
        raise HTTPException(status_code=400, detail=f"There is already a bead colour associated with this year")
    if bead_colour_year.year is None:
        raise HTTPException(status_code=400, detail=f"Year must be specified")
    if bead_colour_year.colour is None:
        raise HTTPException(status_code=400, detail=f"Colour must be specified")
    return crud.add_thaw_tube_bead_colour_year(db, bead_colour_year)


@app.get("/thaw_tube_beads/year{year}", response_model=schemas.ThawTubeBeadColourYear)
async def get_thaw_tube_bead_by_year(year: int, db: Session = Depends(get_db)):
    db_bead_colour = crud.get_thaw_tube_bead_by_year(db=db, year=year)
    if db_bead_colour is None:
        raise HTTPException(status_code=400, detail=f"There is no bead colour associated with {year}")
    return db_bead_colour


@app.get("/thaw_tube_beads/colour{colour}", response_model=schemas.ThawTubeBeadColourYear)
async def get_thaw_tube_bead_by_colour(colour: str, db: Session = Depends(get_db)):
    db_bead_colour = crud.get_thaw_tube_bead_by_colour(db=db, colour=colour)
    if db_bead_colour is None:
        raise HTTPException(status_code=400, detail=f"There is no record of a {colour} thaw tube bead")
    return db_bead_colour


@app.post("/thaw_tubes/", response_model=schemas.ThawTube)
async def add_thaw_tube(thaw_tube: schemas.ThawTubeBase, db: Session = Depends(get_db)):
    db_thaw_tube = crud.get_thaw_tube_by_installation_uid(db, thaw_tube.installation_uid)
    if db_thaw_tube:
        raise HTTPException(status_code=400, detail=f"Thaw tube already associated to installation uid "
                                                    f"{thaw_tube.installation_uid}")
    if thaw_tube.installation_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation UID must be specified")
    if thaw_tube.date_installed is None:
        raise HTTPException(status_code=400, detail=f"Date installed must be specified")
    if not check_tz_aware(thaw_tube.date_installed):
        raise HTTPException(status_code=400, detail=f"{thaw_tube.date_installed} is not time zone aware.")
    return crud.add_thaw_tube(db, thaw_tube)


@app.get("/thaw_tubes/installation_uid{installation_uid}", response_model=schemas.ThawTube)
async def get_thaw_tube_by_installation_uid(installation_uid: int, db: Session = Depends(get_db)):
    db_thaw_tube = crud.get_thaw_tube_by_installation_uid(db=db, installation_uid=installation_uid)
    if db_thaw_tube is None:
        raise HTTPException(status_code=400, detail=f"No thaw tube associated with installation UID "
                                                    f"{installation_uid}")
    return db_thaw_tube


@app.post("/thaw_tube_readings/", response_model=schemas.ThawTubeReading)
async def add_thaw_tube_reading(thaw_tube_reading: schemas.ThawTubeReadingBase, db: Session = Depends(get_db)):
    db_thaw_tube_reading = \
        crud.get_thaw_tube_reading_by_installation_visit_uid(db, thaw_tube_reading.installation_visit_uid)
    if db_thaw_tube_reading:
        raise HTTPException(status_code=400, detail=f"Thaw tube reading already associated to installation visit UID "
                                                    f"{thaw_tube_reading.installation_visit_uid}")
    if thaw_tube_reading.thaw_tube_uid is None:
        raise HTTPException(status_code=400, detail=f"Thaw tube UID must be specified")
    if thaw_tube_reading.installation_visit_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation visit UID must be specified")
    """
    if thaw_tube_reading.scribe_curr is None:
        raise HTTPException(status_code=400, detail=f"scribe_curr must be specified")
    if thaw_tube_reading.scribe_min is None:
        raise HTTPException(status_code=400, detail=f"scribe_min must be specified")
    if thaw_tube_reading.scribe_max is None:
        raise HTTPException(status_code=400, detail=f"scribe_max must be specified")
    if thaw_tube_reading.scribe_height is None:
        raise HTTPException(status_code=400, detail=f"Scriber height must be specified")
    if thaw_tube_reading.tube_height is None:
        raise HTTPException(status_code=400, detail=f"Tube height must be specified")
    if thaw_tube_reading.water_depth is None:
        raise HTTPException(status_code=400, detail=f"Water depth must be specified")
    if thaw_tube_reading.ice_depth is None:
        raise HTTPException(status_code=400, detail=f"Ice depth must be specified")
    """
    if thaw_tube_reading.stopper_on_plug is None:
        raise HTTPException(status_code=400, detail=f"stopper_on_plug must be specified")
    if thaw_tube_reading.new_bead_in is None:
        raise HTTPException(status_code=400, detail=f"new_bead_in must be specified")
    return crud.add_thaw_tube_reading(db, thaw_tube_reading)


@app.get("/thaw_tube_readings/installation_visit_uid{installation_visit_uid}", response_model=schemas.ThawTubeReading)
async def get_thaw_tube_reading_by_installation_visit_uid(installation_visit_uid: int, db: Session = Depends(get_db)):
    db_thaw_tube_reading = \
        crud.get_thaw_tube_reading_by_installation_visit_uid(db, installation_visit_uid)
    if db_thaw_tube_reading is None:
        raise HTTPException(status_code=400, detail=f"No thaw tube reading associated to installation visit UID "
                                                    f"{installation_visit_uid}")
    return db_thaw_tube_reading


@app.post("/thaw_tube_bead_measurements/", response_model=schemas.ThawTubeBeadMeasurement)
async def add_thaw_tube_bead_measurement(bead_measurement: schemas.ThawTubeBeadMeasurementBase,
                                         db: Session = Depends(get_db)):
    db_bead_measurement = crud.get_thaw_tube_bead_measurement_by_reading_uid_and_bead_year(
        db=db,
        thaw_tube_reading_uid=bead_measurement.thaw_tube_reading_uid,
        bead_year=bead_measurement.year)
    if db_bead_measurement:
        raise HTTPException(status_code=400, detail=f"Measurement for {bead_measurement.colour} "
                                                    f"({bead_measurement.year}) already exists for thaw tube reading "
                                                    f"UID {bead_measurement.thaw_tube_reading_uid}")
    if bead_measurement.thaw_tube_reading_uid is None:
        raise HTTPException(status_code=400, detail=f"Thaw tube reading UID must be specified")
    if bead_measurement.thaw_tube_uid is None:
        raise HTTPException(status_code=400, detail=f"Thaw tube UID must be specified")
    if bead_measurement.colour is None:
        raise HTTPException(status_code=400, detail=f"Bead colour must be specified")
    if bead_measurement.year is None:
        raise HTTPException(status_code=400, detail=f"Bead year must be specified")
    if bead_measurement.depth is None:
        raise HTTPException(status_code=400, detail=f"Bead depth must be specified")
    return crud.add_thaw_tube_bead_measurement(db=db, bead_measurement=bead_measurement)


@app.get("/thaw_tube_bead_measurements/reading_uid_and_bead_year/", response_model=schemas.ThawTubeBeadMeasurement)
async def get_thaw_tube_bead_measurement_by_reading_uid_and_bead_year(reading_uid: int, bead_year: int,
                                                                      db: Session = Depends(get_db)):
    db_bead_measurement = crud.get_thaw_tube_bead_measurement_by_reading_uid_and_bead_year(
        db=db,
        thaw_tube_reading_uid=reading_uid,
        bead_year=bead_year)
    if db_bead_measurement is None:
        raise HTTPException(status_code=400, detail=f"No measurement for {bead_year} bead found for thaw tube reading"
                                                    f"UID {reading_uid}")
    return db_bead_measurement


@app.get("/thaw_tube_readings/thaw_tube_uid{thaw_tube_uid}", response_model=list[schemas.ThawTubeReading])
async def get_all_readings_of_thaw_tube_by_thaw_tube_uid(thaw_tube_uid: int, db: Session = Depends(get_db)):
    db_thaw_tube_readings = crud.get_all_readings_of_thaw_tube_by_thaw_tube_uid(db=db, thaw_tube_uid=thaw_tube_uid)
    if db_thaw_tube_readings is None:
        raise HTTPException(status_code=400, detail=f"No thaw tube readings for thaw tube UID {thaw_tube_uid}")
    return db_thaw_tube_readings


@app.get("/thaw_tube_bead_measurements/thaw_tube_reading_uid{thaw_tube_reading_uid}",
         response_model=list[schemas.ThawTubeBeadMeasurement])
async def get_all_thaw_tube_bead_measurements_by_reading_uid(thaw_tube_reading_uid: int, db: Session = Depends(get_db)):
    db_thaw_tube_readings = \
        crud.get_all_thaw_tube_bead_measurements_by_reading_uid(db=db, thaw_tube_reading_uid=thaw_tube_reading_uid)
    if db_thaw_tube_readings is None:
        raise HTTPException(status_code=400, detail=f"No thaw tube readings for thaw tube UID {thaw_tube_reading_uid}")
    return db_thaw_tube_readings


@app.post("/thaw_tube_references/", response_model=schemas.ThawTubeReference)
async def add_thaw_tube_reference(thaw_tube_reference: schemas.ThawTubeReferenceBase, db: Session = Depends(get_db)):
    if thaw_tube_reference.thaw_tube_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation UID must be specified")
    if thaw_tube_reference.date is None:
        raise HTTPException(status_code=400, detail=f"Date must be specified")
    if not check_tz_aware(thaw_tube_reference.date):
        raise HTTPException(status_code=400, detail=f"{thaw_tube_reference.date} is not time zone aware.")
    if thaw_tube_reference.reference_measurement is None:
        raise HTTPException(status_code=400, detail=f"Reference measurement must be specified")
    db_thaw_tube_reference = \
        crud.get_thaw_tube_reference_by_thaw_tube_uid_and_date(db=db,
                                                               thaw_tube_uid=thaw_tube_reference.thaw_tube_uid,
                                                               date=thaw_tube_reference.date)
    if db_thaw_tube_reference:
        raise HTTPException(status_code=400, detail=f"Thaw tube reference already exists for thaw tube UID"
                                                    f"{thaw_tube_reference.thaw_tube_uid} on "
                                                    f"{thaw_tube_reference.date}")
    return crud.add_thaw_tube_reference(db=db, thaw_tube_reference=thaw_tube_reference)


@app.get("/thaw_tube_references/thaw_tube_uid_and_date/", response_model=schemas.ThawTubeReference)
async def get_thaw_tube_reference_by_thaw_tube_uid_and_date(thaw_tube_uid: int, date: dt.datetime,
                                                            db: Session = Depends(get_db)):
    if not check_tz_aware(date):
        raise HTTPException(status_code=400, detail=f"{date} is not time zone aware.")
    db_thaw_tube_reference = \
        crud.get_thaw_tube_reference_by_thaw_tube_uid_and_date(db=db, thaw_tube_uid=thaw_tube_uid, date=date)
    if db_thaw_tube_reference:
        raise HTTPException(status_code=400, detail=f"Thaw tube reference already exists for thaw tube UID "
                                                    f"{thaw_tube_uid} on {date}")
    return db_thaw_tube_reference


@app.get("/installation_visits/thaw_tube_history/installation_uid{installation_uid}",
         response_model=list[ods_schemas.ThawTubeHistory])
def get_thaw_tube_history_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    thaw_tube_uid = crud.get_thaw_tube_by_installation_uid(db=db, installation_uid=installation_uid).thaw_tube_uid
    thaw_tube_references = pd.DataFrame(
        [ele.__dict__ for ele in crud.get_all_thaw_tube_references_for_thaw_tube_uid(
            db=db, thaw_tube_uid=thaw_tube_uid)])
    thaw_tube_references.drop(columns="_sa_instance_state", inplace=True)
    table = pd.DataFrame(crud.get_thaw_tube_readings_at_installation(db=db, installation_uid=installation_uid),
                         columns=["date_time", "recorded_by", "activity", "notes", "tt_read_uid", "tube_height",
                                  "ice_depth", "scribe_min", "scribe_curr", "scribe_max"])
    for i, r in table.iterrows():
        prev_year = r["date_time"].year - 1

        db_prev_year_bead = \
            crud.get_thaw_tube_bead_measurement_by_reading_uid_and_bead_year(thaw_tube_reading_uid=r["tt_read_uid"],
                                                                             bead_year=prev_year, db=db)
        time_diff = [(r["date_time"] - ref_date).total_seconds() for ref_date in thaw_tube_references["date"]]
        ref_index = time_diff.index(min([ele for ele in time_diff if ele > 0]))
        ref_measurement = thaw_tube_references.loc[ref_index, "reference_measurement"]
        if db_prev_year_bead is not None:
            table.loc[i, "previous_year_bead_depth"] = db_prev_year_bead.depth
            table.loc[i, "thaw_penetration"] = db_prev_year_bead.depth - ref_measurement
            table.loc[i, "max_active_layer"] = db_prev_year_bead.depth - (
                        r["tube_height"] - (r["scribe_min"] - r["scribe_curr"]))
            table.loc[i, "surface_change"] = table.loc[i, "thaw_penetration"] - table.loc[i, "max_active_layer"]
    table = table.replace({np.nan: None})
    return table.drop(columns=["tt_read_uid"]).to_dict("records")


@app.get("/thaw_tube_bead_measurements/bead_history/thaw_tube_uid{thaw_tube_uid}",
         response_model=list[ods_schemas.ThawTubeBeadHistory])
def get_thaw_tube_bead_history(thaw_tube_uid: int, db: Session = Depends(get_db)):
    table = pd.DataFrame(crud.get_thaw_tube_bead_history(thaw_tube_uid=thaw_tube_uid, db=db),
                         columns=["bead_year", "bead_colour", "depth", "depth_max", "depth_min",
                                  "installation_visit_uid"])
    for i, r in table.iterrows():
        table.loc[i, "date_time"] = crud.get_installation_visit_by_uid(
            uid=r["installation_visit_uid"], db=db).visit_date
    table = table.replace({np.nan: None})
    return table.drop(columns=["installation_visit_uid"]).to_dict("records")
