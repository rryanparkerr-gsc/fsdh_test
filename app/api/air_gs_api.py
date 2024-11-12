# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-11-01
"""

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

import schemas
import crud
from .api import app, get_db, check_tz_aware
import output_data_structures.data_structures as ods
import output_data_structures.output_schemas as ods_schemas


@app.post("/air_ground_logger_data/", response_model=schemas.AirGroundTemperatureData)
async def add_air_ground_logger_data(air_ground_logger_data: schemas.AirGroundTemperatureDataBase,
                                     db: Session = Depends(get_db)):
    if air_ground_logger_data.logger_uid is None:
        raise HTTPException(status_code=400, detail=f"Logger UID is not specified")
    if air_ground_logger_data.logger_download_uid is None:
        raise HTTPException(status_code=400, detail=f"Logger download UID is not specified")
    if air_ground_logger_data.channel_number is None:
        raise HTTPException(status_code=400, detail=f"Channel number is not specified")
    if air_ground_logger_data.installation_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation UID is not specified")
    if air_ground_logger_data.date_time is None:
        raise HTTPException(status_code=400, detail=f"Measurement date/time is not specified")
    if not check_tz_aware(air_ground_logger_data.date_time):
        raise HTTPException(status_code=400, detail=f"{air_ground_logger_data.date_time} is not time zone aware.")
    if air_ground_logger_data.temperature is None:
        raise HTTPException(status_code=400, detail=f"Temperature measurement is not specified")

    db_cable_logger_data = \
        crud.get_ag_logger_data_by_logger_uid_channel_number_and_measurement_date(
            logger_uid=air_ground_logger_data.logger_uid, channel_number=air_ground_logger_data.channel_number,
            date_time=air_ground_logger_data.date_time, db=db)
    if db_cable_logger_data is not None:
        raise HTTPException(status_code=400, detail=f"Data already exists for logger UID "
                                                    f"{air_ground_logger_data.logger_uid}, channel number "
                                                    f"{air_ground_logger_data.channel_number} for "
                                                    f"{air_ground_logger_data.date_time}")
    db_installation_data = crud.get_ag_data_by_installation_and_measurement_date(
        installation_uid=air_ground_logger_data.installation_uid, date_time=air_ground_logger_data.date_time, db=db)
    if db_installation_data is not None:
        raise HTTPException(status_code=400, detail=f"Data already exists for installation UID "
                                                    f"{air_ground_logger_data.installation_uid} at "
                                                    f"{air_ground_logger_data.date_time}")
    return crud.add_ag_logger_data(ag_logger_data=air_ground_logger_data, db=db)


@app.get("/air_ground_logger_data/installation_uid{installation_uid}/all/",
         response_model=list[ods_schemas.AGLoggerDataOutput])
async def get_air_ground_logger_data_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    db_ag_logger_data = crud.get_ag_logger_data_at_installation(db=db, installation_uid=installation_uid)
    if not db_ag_logger_data:
        raise HTTPException(status_code=400, detail=f"No air/ground logger data associated with installation UID"
                                                    f"{installation_uid}")
    ag_logger_data = [ods.AGLoggerDataOutput(date_time=row.date_time,
                                             temperature=row.temperature,
                                             logger_sn=row.logger_serial_number,
                                             sensor_number=row.channel_number)
                      for row in db_ag_logger_data]
    return ag_logger_data


@app.get("/air_ground_logger_data/installation_uid/timeseries_mean/",
         response_model=list[ods_schemas.SingleSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_air_ground_timeseries_mean_at_installation(installation_uid: int, frequency: str = "D",
                                                         db: Session = Depends(get_db)):
    if frequency not in ["D", "W", "M", "Q", "Y"]:
        raise HTTPException(status_code=400, detail=f"Frequency {frequency} not in [D, W, M, Q, Y]")
    db_ag_logger_data = crud.get_ag_logger_data_at_installation(db=db, installation_uid=installation_uid)
    if not db_ag_logger_data:
        raise HTTPException(status_code=400, detail=f"No air/ground logger data associated with installation UID "
                                                    f"{installation_uid}")
    ag_logger_data = [ods.AGLoggerDataOutput(date_time=row.date_time,
                                             temperature=row.temperature,
                                             logger_sn=row.logger_serial_number,
                                             sensor_number=row.channel_number).__dict__
                      for row in db_ag_logger_data]
    ag_logger_data = pd.DataFrame(ag_logger_data)
    ag_logger_data["date_time"] = pd.to_datetime(ag_logger_data["date_time"], utc=True)
    daily_means = ag_logger_data[["date_time", "temperature"]]\
        .groupby(pd.Grouper(key="date_time", freq=frequency, origin="epoch")).mean()
    daily_means.reset_index(inplace=True)
    daily_means.rename(columns={"date_time": "date"}, inplace=True)
    return daily_means.to_dict("records")


@app.get("/air_ground_logger_data/installation_uid{installation_uid}/daily_mean/",
         response_model=list[ods_schemas.SingleSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_air_ground_daily_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_air_ground_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="D", db=db)


@app.get("/air_ground_logger_data/installation_uid{installation_uid}/weekly_mean/",
         response_model=list[ods_schemas.SingleSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_air_ground_weekly_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_air_ground_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="W", db=db)


@app.get("/air_ground_logger_data/installation_uid{installation_uid}monthly_mean/",
         response_model=list[ods_schemas.SingleSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_air_ground_monthly_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_air_ground_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="M", db=db)


@app.get("/air_ground_logger_data/installation_uid{installation_uid}/quarterly_mean/",
         response_model=list[ods_schemas.SingleSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_air_ground_quarterly_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_air_ground_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="Q", db=db)


@app.get("/air_ground_logger_data/installation_uid{installation_uid}/yearly_mean/",
         response_model=list[ods_schemas.SingleSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_air_ground_yearly_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_air_ground_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="Y", db=db)
