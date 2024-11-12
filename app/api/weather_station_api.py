from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import datetime as dt

import schemas
import crud
from .api import app, get_db, check_tz_aware


@app.post("/weather_stations/", response_model=schemas.WeatherStation)
async def add_weather_station(weather_station: schemas.WeatherStationBase, db: Session = Depends(get_db)):
    if weather_station.installation_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation UID must be specified")
    if weather_station.logger_serial_number is None:
        raise HTTPException(status_code=400, detail=f"Logger SN must be specified")
    if weather_station.date_installed is None:
        raise HTTPException(status_code=400, detail=f"Date installed must be specified")
    if not check_tz_aware(weather_station.date_installed):
        raise HTTPException(status_code=400, detail=f"{weather_station.date_installed} is not time zone aware.")
    if weather_station.battery_year is None:
        raise HTTPException(status_code=400, detail=f"Battery year must be specified")
    db_weather_station = crud.get_weather_station_by_installation_uid(db, weather_station.installation_uid)
    if db_weather_station:
        raise HTTPException(status_code=400, detail=f"Weather station associated to installation uid "
                                                    f"{weather_station.installation_uid}")
    return crud.add_weather_station(db, weather_station)


@app.get("/weather_stations/installation_uid{installation_uid}", response_model=schemas.WeatherStation)
async def get_weather_station_by_installation_uid(installation_uid: int, db: Session = Depends(get_db)):
    weather_station = crud.get_weather_station_by_installation_uid(db=db, installation_uid=installation_uid)
    if weather_station is None:
        raise HTTPException(status_code=400, detail=f"No weather station associated with installation UID "
                                                    f"{installation_uid}")
    return weather_station


@app.get("/weather_station_downloads/installation_visit_uid{installation_visit_uid}",
         response_model=schemas.WeatherStationDownload)
async def get_weather_station_download_by_visit_uid(installation_visit_uid: int, db: Session = Depends(get_db)):
    weather_station = crud.get_weather_station_download_by_visit_uid(db=db,
                                                                     installation_visit_uid=installation_visit_uid)
    if weather_station is None:
        raise HTTPException(status_code=400, detail=f"No weather station download associated with installation visit "
                                                    f"UID {installation_visit_uid}")
    return weather_station


@app.post("/weather_station_downloads/", response_model=schemas.WeatherStationDownload)
async def add_weather_station_download(weather_station_download: schemas.WeatherStationDownloadBase,
                                       db: Session = Depends(get_db)):
    if weather_station_download.installation_visit_uid is None:
        raise HTTPException(status_code=400, detail=f"Installation visit UID must be specified")
    if weather_station_download.weather_station_uid is None:
        raise HTTPException(status_code=400, detail=f"Weather station UID must be specified")
    if weather_station_download.download_date is None:
        raise HTTPException(status_code=400, detail=f"Download date must be specified")
    if not check_tz_aware(weather_station_download.download_date):
        raise HTTPException(status_code=400, detail=f"{weather_station_download.download_date} is not time zone aware.")
    db_weather_station_download = crud.get_weather_station_download_by_visit_uid(
        db=db, installation_visit_uid=weather_station_download.installation_visit_uid)
    if db_weather_station_download:
        HTTPException(status_code=400, detail=f"A Weather station download is already associated to installation visit"
                                              f"uid {weather_station_download.installation_visit_uid}")
    return crud.add_weather_station_download(db=db, weather_station_download=weather_station_download)


@app.post("/weather_station_hourly_data/", response_model=schemas.WeatherStationHourlyData)
async def add_hourly_weather_station_data(hourly_data: schemas.WeatherStationHourlyDataBase,
                                          db: Session = Depends(get_db)):
    if hourly_data.weather_station_uid is None:
        raise HTTPException(status_code=400, detail=f"Weather station UID must be specified")
    if hourly_data.weather_station_download_uid is None:
        raise HTTPException(status_code=400, detail=f"Weather station download UID must be specified")
    if hourly_data.date_time is None:
        raise HTTPException(status_code=400, detail=f"Date/time must be specified")
    if not check_tz_aware(hourly_data.date_time):
        raise HTTPException(status_code=400, detail=f"{hourly_data.date_time} is not time zone aware.")
    db_hourly_data = crud.get_weather_station_hourly_data_by_station_uid_and_time(
        db=db, timestamp=hourly_data.date_time, weather_station_uid=hourly_data.weather_station_uid)
    if db_hourly_data:
        raise HTTPException(status_code=400, detail=f"This data is already in the database")
    return crud.add_hourly_weather_station_data(db=db, hourly_data=hourly_data)


@app.get("/weather_station_hourly_data/station_uid_and_time/", response_model=schemas.WeatherStationHourlyData)
async def get_weather_station_hourly_data_by_station_uid_and_time(weather_station_uid: int, timestamp: dt.datetime,
                                                                  db: Session = Depends(get_db)):
    if not check_tz_aware(timestamp):
        raise HTTPException(status_code=400, detail=f"{timestamp} is not time zone aware.")
    db_hourly_data =\
        crud.get_weather_station_hourly_data_by_station_uid_and_time(
            db=db, timestamp=timestamp, weather_station_uid=weather_station_uid)
    if db_hourly_data is None:
        raise HTTPException(status_code=400, detail=f"There is no data for {timestamp} associated to weather_station "
                                                    f"UID {weather_station_uid}")
    return db_hourly_data


@app.post("/weather_station_daily_data/", response_model=schemas.WeatherStationDailyData)
async def add_daily_weather_station_data(daily_data: schemas.WeatherStationDailyDataBase,
                                         db: Session = Depends(get_db)):
    if daily_data.weather_station_uid is None:
        raise HTTPException(status_code=400, detail=f"Weather station UID must be specified")
    if daily_data.weather_station_download_uid is None:
        raise HTTPException(status_code=400, detail=f"Weather station download UID must be specified")
    if daily_data.date_time is None:
        raise HTTPException(status_code=400, detail=f"Date/time must be specified")
    if not check_tz_aware(daily_data.date_time):
        raise HTTPException(status_code=400, detail=f"{daily_data.date_time} is not time zone aware.")
    db_daily_data = crud.get_weather_station_daily_data_by_station_uid_and_time(
        db=db, timestamp=daily_data.date_time, weather_station_uid=daily_data.weather_station_uid)
    if db_daily_data:
        raise HTTPException(status_code=400, detail=f"This data is already in the database")
    return crud.add_daily_weather_station_data(db=db, daily_data=daily_data)


@app.get("/weather_station_daily_data/station_uid_and_time/", response_model=schemas.WeatherStationDailyData)
async def get_weather_station_hourly_data_by_station_uid_and_time(weather_station_uid: int, timestamp: dt.datetime,
                                                                  db: Session = Depends(get_db)):
    if not check_tz_aware(timestamp):
        raise HTTPException(status_code=400, detail=f"{timestamp} is not time zone aware.")
    db_daily_data =\
        crud.get_weather_station_daily_data_by_station_uid_and_time(
            db=db, timestamp=timestamp, weather_station_uid=weather_station_uid)
    if db_daily_data is None:
        raise HTTPException(status_code=400, detail=f"There is no data for {timestamp} associated to weather_station "
                                                    f"UID {weather_station_uid}")
    return db_daily_data


@app.post("/weather_stations/update_status", response_model=schemas.WeatherStation)
async def update_ws_sensor_status(uid: int, air_temp_stat: str, snow_stat: str, anemo_stat: str,
                                  db: Session = Depends(get_db)):
    for ele in [air_temp_stat, snow_stat, anemo_stat]:
        if ele not in ["active", "need_repair"]:
            raise HTTPException(status_code=400, detail=f"Invalid status: {ele} is not in ['active', 'need_repair']")
    db_weather_station = crud.update_ws_sensor_status(db=db, uid=uid, air_temp=air_temp_stat, anemo=anemo_stat,
                                                      snow=snow_stat)
    return db_weather_station
