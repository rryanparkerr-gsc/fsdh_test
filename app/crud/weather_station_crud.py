# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-06-20
"""

from sqlalchemy.orm import Session
import datetime as dt

from app import schemas
from app import models


def get_weather_station_by_installation_uid(db: Session, installation_uid: int):
    return db.query(models.WeatherStation).filter(models.WeatherStation.installation_uid == installation_uid).first()


def add_weather_station(db: Session, weather_station: schemas.WeatherStationBase):
    new_weather_station = models.WeatherStation(installation_uid=weather_station.installation_uid,
                                                logger_serial_number=weather_station.logger_serial_number,
                                                date_installed=weather_station.date_installed.replace(microsecond=0),
                                                battery_year=weather_station.battery_year,
                                                at_status=weather_station.at_status,
                                                anemo_status=weather_station.anemo_status,
                                                snow_status=weather_station.snow_status)
    db.add(new_weather_station)
    db.commit()
    db.refresh(new_weather_station)
    return new_weather_station


def get_weather_station_download_by_visit_uid(db: Session, installation_visit_uid: int):
    return db.query(models.WeatherStationDownload) \
        .filter(models.WeatherStationDownload.installation_visit_uid == installation_visit_uid).first()


def add_weather_station_download(db: Session, weather_station_download: schemas.WeatherStationDownloadBase):
    new_weather_station_download = models.WeatherStationDownload(
        installation_visit_uid=weather_station_download.installation_visit_uid,
        weather_station_uid=weather_station_download.weather_station_uid,
        download_date=weather_station_download.download_date.replace(microsecond=0),
        download_quality=weather_station_download.download_quality,
        clock_reset=weather_station_download.clock_reset,
        public_tbl_good=weather_station_download.public_tbl_good,
        status_tbl_good=weather_station_download.status_tbl_good,
        daily_tbl_good=weather_station_download.daily_tbl_good,
        hourly_tbl_good=weather_station_download.hourly_tbl_good,
        notes=weather_station_download.notes)
    db.add(new_weather_station_download)
    db.commit()
    db.refresh(new_weather_station_download)
    return new_weather_station_download


def add_hourly_weather_station_data(db: Session, hourly_data: schemas.WeatherStationHourlyDataBase):
    new_data = models.WeatherStationHourlyData(
        weather_station_uid=hourly_data.weather_station_uid,
        weather_station_download_uid=hourly_data.weather_station_download_uid,
        date_time=hourly_data.date_time.replace(microsecond=0),
        internal_temp_avg=hourly_data.internal_temp_avg,
        air_temp_avg=hourly_data.air_temp_avg,
        wind_speed_avg=hourly_data.wind_speed_avg,
        wind_speed_std=hourly_data.wind_speed_std,
        snow_depth=hourly_data.snow_depth)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


def get_weather_station_hourly_data_by_station_uid_and_time(db: Session, weather_station_uid: int,
                                                            timestamp: dt.datetime):
    return db.query(models.WeatherStationHourlyData)\
        .filter((models.WeatherStationHourlyData.date_time == timestamp)
                & (models.WeatherStationHourlyData.weather_station_uid == weather_station_uid)).first()


def add_daily_weather_station_data(db: Session, daily_data: schemas.WeatherStationDailyDataBase):
    new_data = models.WeatherStationDailyData(
        weather_station_uid=daily_data.weather_station_uid,
        weather_station_download_uid=daily_data.weather_station_download_uid,
        date_time=daily_data.date_time.replace(microsecond=0),
        internal_temp_min=daily_data.internal_temp_min,
        internal_temp_max=daily_data.internal_temp_max,
        air_temp_avg=daily_data.air_temp_avg,
        air_temp_max=daily_data.air_temp_max,
        time_air_temp_max=daily_data.time_air_temp_max,
        air_temp_min=daily_data.air_temp_min,
        time_air_temp_min=daily_data.time_air_temp_min,
        wind_speed_avg=daily_data.wind_speed_avg,
        wind_speed_max=daily_data.wind_speed_max,
        time_wind_speed_max=daily_data.time_wind_speed_max,
        snow_depth=daily_data.snow_depth)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


def get_weather_station_daily_data_by_station_uid_and_time(db: Session, weather_station_uid: int,
                                                           timestamp: dt.datetime):
    return db.query(models.WeatherStationDailyData)\
        .filter((models.WeatherStationDailyData.date_time == timestamp)
                & (models.WeatherStationDailyData.weather_station_uid == weather_station_uid)).first()


def update_ws_sensor_status(db: Session, uid: int, air_temp: str, anemo: str, snow: str):
    weather_station = db.query(models.WeatherStation).filter(models.WeatherStation.weather_station_uid == uid).first()
    weather_station.at_status = air_temp
    weather_station.anemo_status = anemo
    weather_station.snow_status = snow
    db.commit()
    return weather_station
