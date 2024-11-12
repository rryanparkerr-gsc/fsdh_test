# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-12
"""

from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np
import pandas as pd
import asyncio

import schemas
import crud
from .api import app, get_db, check_tz_aware
import output_data_structures.data_structures as ods
import output_data_structures.output_schemas as ods_schemas

connector_types = ["seacon", "impulse", "16 pin", "bendix", "24 pin", "unknown"]
sensor_types = ["YSI44033", "YSI44032", "fenwall", "aitkins", "unknown"]


@app.get("/cables/installation_uid{installation_uid}", response_model=schemas.Cable)
async def get_cable_by_installation_uid(installation_uid: int, db: Session = Depends(get_db)):
    db_cable = crud.get_cable_by_installation_uid(db=db, installation_uid=installation_uid)
    if db_cable is None:
        raise HTTPException(status_code=400, detail=f"No cable associated with installation UID {installation_uid}")
    return db_cable


@app.post("/cables/", response_model=schemas.Cable)
async def add_cable(cable: schemas.CableBase, db: Session = Depends(get_db)):
    db_cable = crud.get_cable_by_installation_uid(db=db, installation_uid=cable.installation_uid)
    if db_cable:
        raise HTTPException(status_code=400, detail=f"Cable already associated to installation uid "
                                                    f"{cable.installation_uid}")
    if cable.installation_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation UID must be specified")
    if cable.connector_type not in connector_types:
        raise HTTPException(status_code=400, detail=f"Connector type must be specified")
    """if cable.length is None:
        raise HTTPException(status_code=400, detail=f"Cable length must be specified")"""
    if cable.num_sensors is None:
        raise HTTPException(status_code=400, detail=f"number of sensors must be specified")
    return crud.add_cable(db=db, cable=cable)


@app.post("/cable_sensors/", response_model=schemas.CableSensor)
async def add_cable_sensor(cable_sensor: schemas.CableSensorBase, db: Session = Depends(get_db)):
    db_cable_sensor = \
        crud.get_cable_sensor_by_cable_uid_sensor_number_and_date_installed(db=db,
                                                                            cable_uid=cable_sensor.cable_uid,
                                                                            date_installed=cable_sensor.date_installed,
                                                                            sensor_number=cable_sensor.number_in_chain)
    if db_cable_sensor:
        raise HTTPException(status_code=400, detail=f"Cable sensor already exists for sensor"
                                                    f"{cable_sensor.number_in_chain} in cable UID "
                                                    f"{cable_sensor.cable_uid} installed on"
                                                    f"{cable_sensor.date_installed}")
    if cable_sensor.cable_uid is None:
        raise HTTPException(status_code=400, detail=f"Cable UID must be specified")
    if cable_sensor.date_installed is None:
        raise HTTPException(status_code=400, detail=f"date installed must be specified")
    if not check_tz_aware(cable_sensor.date_installed):
        raise HTTPException(status_code=400, detail=f"{cable_sensor.date_installed} is not time zone aware.")
    if cable_sensor.sensor_type not in sensor_types:
        raise HTTPException(status_code=400, detail=f"sensor type must be in {sensor_types}")
    if cable_sensor.number_in_chain is None:
        raise HTTPException(status_code=400, detail=f"Sensor number must be specified")
    if cable_sensor.depth is None:
        raise HTTPException(status_code=400, detail=f"Sensor depth must be specified")
    return crud.add_cable_sensor(db=db, cable_sensor=cable_sensor)


@app.get("/cable_sensors/cable_sensor_uid{cable_sensor_uid}/", response_model=schemas.CableSensor)
async def get_cable_sensor_by_uid(cable_sensor_uid: int, db: Session = Depends(get_db)):
    db_cable = crud.get_cable_sensor_by_uid(db=db, cable_sensor_uid=cable_sensor_uid)
    if db_cable is None:
        raise HTTPException(status_code=400, detail=f"Cable sensor UID {cable_sensor_uid} does not exist")
    return db_cable


@app.get("/cable_sensors/cable_uid_sensor_number_and_date_installed/", response_model=schemas.CableSensor)
async def get_cable_sensor_by_cable_uid_sensor_number_and_date_installed(sensor_number: int, cable_uid: int,
                                                                         date_installed: dt.datetime,
                                                                         db: Session = Depends(get_db)):
    if date_installed.tzinfo is None or date_installed.tzinfo.utcoffset(date_installed) is None:
        raise HTTPException(status_code=400, detail=f"date_installed must be timezone aware.")
    db_cable_sensor = \
        crud.get_cable_sensor_by_cable_uid_sensor_number_and_date_installed(db=db,
                                                                            cable_uid=cable_uid,
                                                                            date_installed=date_installed,
                                                                            sensor_number=sensor_number)
    if db_cable_sensor is None:
        raise HTTPException(status_code=400, detail=f"Cable sensor does not exist for sensor"
                                                    f"{sensor_number} in cable UID "
                                                    f"{cable_uid} installed on"
                                                    f"{date_installed}")
    return db_cable_sensor


@app.post("/cables/update/", response_model=schemas.Cable)
async def update_cable(uid: int, connector_type: str | None = None, length: float | None = None,
                       borehole_depth: float | None = None, num_sensors: int | None = None,
                       db: Session = Depends(get_db)):
    db_cable = crud.update_cable(db=db, uid=uid, connector_type=connector_type, length=length,
                                 borehole_depth=borehole_depth, num_sensors=num_sensors)
    return db_cable


@app.post("/cable_sensors/update/", response_model=schemas.CableSensor)
async def update_cable_sensor(cable_sensor_uid: int, date_installed: dt.datetime | None = None,
                              depth: float | None = None, sensor_type: str | None = None,
                              number_in_chain: int | None = None, db: Session = Depends(get_db)):
    if date_installed is not None and not check_tz_aware(date_installed):
        raise HTTPException(status_code=400, detail=f"{date_installed} is not time zone aware.")
    db_cable_sensor = crud.update_cable_sensor(db=db, cable_sensor_uid=cable_sensor_uid, date_installed=date_installed,
                                               depth=depth, sensor_type=sensor_type, number_in_chain=number_in_chain)
    return db_cable_sensor


@app.post("/cable_manual_reads/", response_model=schemas.CableManualRead)
async def add_cable_manual_read(cable_manual_read: schemas.CableManualReadInput, db: Session = Depends(get_db)):
    if cable_manual_read.cable_sensor_uid is None:
        raise HTTPException(status_code=400, detail=f"Cable sensor UID is not specified")
    if cable_manual_read.installation_visit_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation visit UID is not specified")
    if cable_manual_read.installation_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation UID is not specified")
    if (cable_manual_read.resistance is None and cable_manual_read.temperature is None) \
            or (cable_manual_read.resistance is not None and cable_manual_read.temperature is not None):
        raise HTTPException(status_code=400, detail=f"Either temperature or resistance must be specified but not both")
    db_cable_manual_read = crud.get_cable_manual_read_by_sensor_and_installation_visit_uids(
        db=db,
        sensor_uid=cable_manual_read.cable_sensor_uid,
        installation_visit_uid=cable_manual_read.installation_visit_uid)
    if db_cable_manual_read is not None:
        raise HTTPException(status_code=400, detail=f"Cable manual read from installation visit UID "
                                                    f"{cable_manual_read.installation_visit_uid} already exists for "
                                                    f"cable sensor UID {cable_manual_read.cable_sensor_uid}")

    if cable_manual_read.resistance is not None:
        db_cable_sensor = crud.get_cable_sensor_by_uid(cable_sensor_uid=cable_manual_read.cable_sensor_uid, db=db)
        if db_cable_sensor.sensor_type == "aitkins":
            a = -6.53968443
            b = 5164.37176
            c = 318
            cable_manual_read.temperature = b / (np.log(cable_manual_read.resistance) - a) - c
        elif db_cable_sensor.sensor_type == "fenwal":
            a = 0.001382913
            b = 0.000240465
            c = 0.0000000891485
            cable_manual_read.temperature = 1 / (a + (b * np.log(cable_manual_read.resistance))
                                                 + (c * (np.log(cable_manual_read.resistance)) ^ 3)) - 273.16
        elif db_cable_sensor.sensor_type == "YSI44033":
            a = -7.46641674
            b = 5248.119347
            c = 320.6
            cable_manual_read.temperature = b / (np.log(cable_manual_read.resistance) - a) - c
        elif db_cable_sensor.sensor_type == "YSI44032":
            a = -5.53848562
            b = 5844.563551
            c = 343.8
            cable_manual_read.temperature = b / (np.log(cable_manual_read.resistance) - a) - c
        else:
            raise HTTPException(status_code=400,
                                detail=f"Sensor type {db_cable_sensor.sensor_type} does not have a formula for "
                                       f"converting resistance to temperature")
    return crud.add_cable_manual_read(cable_manual_read=cable_manual_read, db=db)


@app.get("/cable_manual_reads/sensor_and_installation_visit_uids/", response_model=schemas.CableManualRead)
async def get_cable_manual_read_by_sensor_and_installation_visit_uids(sensor_uid: int, installation_visit_uid: int,
                                                                      db: Session = Depends(get_db)):
    db_cable_manual_read = \
        crud.get_cable_manual_read_by_sensor_and_installation_visit_uids(sensor_uid=sensor_uid,
                                                                         installation_visit_uid=installation_visit_uid,
                                                                         db=db)
    if db_cable_manual_read is None:
        raise HTTPException(status_code=400, detail=f"Cable manual read from installation visit UID "
                                                    f"{installation_visit_uid} does not exist for "
                                                    f"cable sensor UID {sensor_uid}")
    return db_cable_manual_read


@app.get("/cable_sensors/cable_uid_sensor_number_and_date_visited/", response_model=schemas.CableSensor)
async def get_cable_sensor_by_cable_uid_sensor_number_and_date_visited(cable_uid: int, sensor_number: int,
                                                                       date_visited: dt.datetime,
                                                                       db: Session = Depends(get_db)):
    if not check_tz_aware(date_visited):
        raise HTTPException(status_code=400, detail=f"{date_visited} is not time zone aware.")
    db_cable_sensor = crud.get_cable_sensor_by_cable_uid_sensor_number_and_date_visited(
        cable_uid=cable_uid,
        sensor_number=sensor_number,
        date_visited=date_visited,
        db=db)
    if db_cable_sensor is None:
        raise HTTPException(status_code=400, detail=f"Sensor {sensor_number} does not exist in cable UID {cable_uid}")
    return db_cable_sensor


@app.get("/cable_sensors/cable_uid_and_sensor_number/", response_model=list[schemas.CableSensor])
async def get_all_cable_sensor_records_for_cable_uid_and_sensor_number(cable_uid: int, sensor_number: int,
                                                                       db: Session = Depends(get_db)):
    db_cable_sensor = crud.get_all_cable_sensor_records_for_cable_uid_and_sensor_number(
        cable_uid=cable_uid,
        sensor_number=sensor_number,
        db=db)
    if db_cable_sensor is None:
        raise HTTPException(status_code=400, detail=f"Sensor {sensor_number} does not exist in cable UID {cable_uid}")
    return db_cable_sensor


@app.post("/cable_logger_data/", response_model=schemas.CableLoggerData | None)
async def add_cable_logger_data(cable_logger_data: schemas.CableLoggerDataBase, db: Session = Depends(get_db),
                                silence_duplicate_warnings: bool = False, return_data: bool = True):
    if cable_logger_data.logger_uid is None:
        raise HTTPException(status_code=400, detail=f"Logger UID is not specified")
    if cable_logger_data.logger_download_uid is None:
        raise HTTPException(status_code=400, detail=f"Logger download UID is not specified")
    if cable_logger_data.cable_sensor_uid is None:
        raise HTTPException(status_code=400, detail=f"Cable sensor UID is not specified")
    if cable_logger_data.installation_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation UID is not specified")
    if cable_logger_data.date_time is None:
        raise HTTPException(status_code=400, detail=f"Measurement date/time is not specified")
    if not check_tz_aware(cable_logger_data.date_time):
        raise HTTPException(status_code=400, detail=f"{cable_logger_data.date_time} is not time zone aware.")
    if cable_logger_data.temperature is None:
        raise HTTPException(status_code=400, detail=f"Temperature measurement is not specified")
    db_cable_logger_data = \
        crud.get_cable_logger_data_by_logger_uid_sensor_uid_and_measurement_date(
            logger_uid=cable_logger_data.logger_uid, sensor_uid=cable_logger_data.cable_sensor_uid,
            date_time=cable_logger_data.date_time, db=db)
    if db_cable_logger_data is not None:
        if silence_duplicate_warnings:
            return
        else:
            raise HTTPException(status_code=400, detail=f"Data already exists for logger UID "
                                                        f"{cable_logger_data.logger_uid} and cable sensor UID "
                                                        f"{cable_logger_data.cable_sensor_uid} for "
                                                        f"{cable_logger_data.date_time}")

    db_cable_data = crud.get_cable_data_by_sensor_uid_and_measurement_date(
        sensor_uid=cable_logger_data.cable_sensor_uid, date_time=cable_logger_data.date_time, db=db)
    if db_cable_data is not None:
        if silence_duplicate_warnings:
            return
        else:
            raise HTTPException(status_code=400, detail=f"Data already exists for installation UID "
                                                        f"{cable_logger_data.installation_uid} at "
                                                        f"{cable_logger_data.date_time}")
    if return_data:
        return crud.add_cable_logger_data(cable_logger_data=cable_logger_data, db=db)
    else:
        return None


@app.post("/cable_logger_data/bulk/", response_model=list[schemas.CableLoggerData | None] | None)
async def add_bulk_cable_logger_data(bulk_cable_logger_data: list[schemas.CableLoggerDataBase],
                                     db: Session = Depends(get_db), return_data: bool = True):
    output = await asyncio.gather(*[add_cable_logger_data(cable_logger_data=cable_logger_data,
                                                          db=db,
                                                          silence_duplicate_warnings=True,
                                                          return_data=return_data)
                                    for cable_logger_data in bulk_cable_logger_data])
    if return_data:
        return output
    else:
        return None


@app.get("/cable_logger_data/installation_uid{installation_uid}/all/",
         response_model=list[ods_schemas.CableLoggerDataOutput])
async def get_cable_logger_data_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    db_cable_logger_data = crud.get_cable_logger_data_at_installation(db=db, installation_uid=installation_uid)
    if not db_cable_logger_data:
        raise HTTPException(status_code=400, detail=f"No cable logger data associated with installation UID"
                                                    f"{installation_uid}")
    cable_logger_data = [ods.CableLoggerDataOutput(date_time=row.date_time,
                                                   temperature=row.temperature,
                                                   logger_sn=row.logger_serial_number,
                                                   sensor_number=row.number_in_chain,
                                                   sensor_depth=row.depth)
                         for row in db_cable_logger_data]
    return cable_logger_data


@app.get("/cable_logger_data/installation_uid/timeseries_mean/",
         response_model=list[ods_schemas.MultiSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_cable_timeseries_mean_at_installation(installation_uid: int, frequency: str = "D",
                                                    db: Session = Depends(get_db)):
    if frequency not in ["D", "W", "M", "Q", "Y"]:
        raise HTTPException(status_code=400, detail=f"Frequency {frequency} not in [D, W, M, Q, Y]")
    db_cable_logger_data = crud.get_cable_logger_data_at_installation(db=db, installation_uid=installation_uid)
    if not db_cable_logger_data:
        raise HTTPException(status_code=400, detail=f"No cable logger data associated with installation UID"
                                                    f"{installation_uid}")
    cable_logger_data = [ods.CableLoggerDataOutput(date_time=row.date_time,
                                                   temperature=row.temperature,
                                                   logger_sn=row.logger_serial_number,
                                                   sensor_number=row.number_in_chain,
                                                   sensor_depth=row.depth).__dict__
                         for row in db_cable_logger_data]
    cable_logger_data = pd.DataFrame(cable_logger_data)
    cable_logger_data["date_time"] = pd.to_datetime(cable_logger_data["date_time"], utc=True)
    daily_means = None
    for sensor in cable_logger_data["sensor_number"].unique():
        subset = cable_logger_data.loc[cable_logger_data["sensor_number"] == sensor]
        subset_daily_means = subset[["date_time", "temperature", "sensor_depth"]] \
            .groupby(pd.Grouper(key="date_time", freq=frequency, origin="epoch")).mean()
        subset_daily_means.rename(columns={"temperature": f"sensor_{sensor}_temp",
                                           "sensor_depth": f"sensor_{sensor}_depth"}, inplace=True)
        if daily_means is None:
            daily_means = subset_daily_means
        else:
            daily_means = daily_means.join(subset_daily_means, how="outer")
    daily_means.reset_index(inplace=True)
    daily_means.rename(columns={"date_time": "date"}, inplace=True)
    return daily_means.to_dict("records")


@app.get("/cable_logger_data/installation_uid{installation_uid}/daily_mean/",
         response_model=list[ods_schemas.MultiSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_cable_daily_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_cable_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="D", db=db)


@app.get("/cable_logger_data/installation_uid{installation_uid}/weekly_mean/",
         response_model=list[ods_schemas.MultiSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_cable_weekly_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_cable_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="W", db=db)


@app.get("/cable_logger_data/installation_uid{installation_uid}monthly_mean/",
         response_model=list[ods_schemas.MultiSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_cable_monthly_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_cable_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="M", db=db)


@app.get("/cable_logger_data/installation_uid{installation_uid}/quarterly_mean/",
         response_model=list[ods_schemas.MultiSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_cable_quarterly_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_cable_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="Q", db=db)


@app.get("/cable_logger_data/installation_uid{installation_uid}/yearly_mean/",
         response_model=list[ods_schemas.MultiSensorTimeSeriesAverageData], response_model_exclude_defaults=True)
async def get_cable_yearly_mean_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    return await get_cable_timeseries_mean_at_installation(installation_uid=installation_uid, frequency="Y", db=db)


@app.get("/cable_manual_reads/installation_uid{installation_uid}/all/",
         response_model=list[ods_schemas.CableManualReadOutput])
async def get_cable_manual_read_data_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    db_cable_manual_reads = crud.get_cable_manual_read_data_at_installation(db=db, installation_uid=installation_uid)
    if not db_cable_manual_reads:
        raise HTTPException(status_code=400, detail=f"No manual cable readings associated with installation UID"
                                                    f"{installation_uid}")
    cable_manual_reads = [ods.CableManualReadOutput(date_time=row.visit_date,
                                                    resistance=row.resistance,
                                                    ol=row.ol,
                                                    drift_up=row.drift_up,
                                                    drift_down=row.drift_down,
                                                    sensor_number=row.number_in_chain,
                                                    depth=row.depth,
                                                    sensor_type=row.sensor_type)
                          for row in db_cable_manual_reads]
    return cable_manual_reads


@app.get("/stick_ups/installation_visit_uid{installation_visit_uid}/", response_model=schemas.StickUp)
async def get_stick_up_by_installation_visit_uid(installation_visit_uid: int, db: Session = Depends(get_db)):
    db_stick_up = crud.get_stick_up_by_installation_visit_uid(installation_visit_uid=installation_visit_uid, db=db)
    if db_stick_up is None:
        raise HTTPException(status_code=400, detail=f"No stick up recorded during installation visit "
                                                    f"{installation_visit_uid}.")
    return db_stick_up


@app.post("/stick_ups/", response_model=schemas.StickUp)
async def add_stick_up(stick_up: schemas.StickUpBase, db: Session = Depends(get_db)):
    if stick_up.installation_visit_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation visit UID is not specified")
    if stick_up.measurement is None:
        raise HTTPException(status_code=400, detail=f"Stick up measurement is not specified")
    db_stick_up = crud.get_stick_up_by_installation_visit_uid(installation_visit_uid=stick_up.installation_visit_uid,
                                                              db=db)
    if db_stick_up is not None:
        raise HTTPException(status_code=400, detail=f"Stick up record already exists for installation visit "
                                                    f"{stick_up.installation_visit_uid}.")
    return crud.add_stick_up(stick_up=stick_up, db=db)


@app.get("/cable_sensors/installation_uid{installation_uid}/", response_model=list[schemas.CableSensor])
async def get_all_cable_sensors_at_installation(installation_uid: int, db: Session = Depends(get_db)):
    db_cable = await get_cable_by_installation_uid(db=db, installation_uid=installation_uid)
    db_sensors = crud.get_all_cable_sensors(cable_uid=db_cable.cable_uid, db=db)
    if not db_sensors:
        raise HTTPException(status_code=400, detail=f"No cable sensor records exist for cable UID "
                                                    f"{db_cable.cable_uid}.")
    return db_sensors


@app.post("/cable_sensor_mappings/", response_model=schemas.CableSensorMapping)
async def add_cable_sensor_mapping(cable_sensor_mapping: schemas.CableSensorMappingBase, db: Session = Depends(get_db)):
    if cable_sensor_mapping.cable_uid is None:
        raise HTTPException(status_code=400, detail=f"Cable UID is not specified")
    if cable_sensor_mapping.cable_sensor_uid is None:
        raise HTTPException(status_code=400, detail=f"Cable sensor UID is not specified")
    if cable_sensor_mapping.mapping_1 is None:
        raise HTTPException(status_code=400, detail=f"Mapping 1 is not specified")

    db_cable_sensor_mapping = crud.get_cable_sensor_mapping_by_cable_sensor_uid(
        cable_sensor_uid=cable_sensor_mapping.cable_sensor_uid, db=db)
    if db_cable_sensor_mapping is not None:
        raise HTTPException(status_code=400, detail=f"Stick up record already exists for installation visit "
                                                    f"{cable_sensor_mapping.cable_sensor_uid}.")
    return crud.add_cable_sensor_mapping(cable_sensor_mapping=cable_sensor_mapping, db=db)


@app.get("/cable_sensors/cable_uid{cable_uid}/", response_model=list[schemas.CableSensor])
async def get_all_cable_sensors_for_cable(cable_uid: int, db: Session = Depends(get_db)):
    db_sensors = crud.get_all_cable_sensors(cable_uid=cable_uid, db=db)
    if not db_sensors:
        raise HTTPException(status_code=400, detail=f"No cable sensor records exist for cable UID {cable_uid}.")
    return db_sensors
