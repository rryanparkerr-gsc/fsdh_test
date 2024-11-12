# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-07
"""

import datetime as dt

from .base_model import BaseModelConfig


class WeatherStationBase(BaseModelConfig):
    installation_uid: int
    logger_serial_number: str
    date_installed: dt.datetime
    battery_year: int
    at_status: str | None = None
    anemo_status: str | None = None
    snow_status: str | None = None


class WeatherStation(WeatherStationBase):
    weather_station_uid: int


class WeatherStationDownloadBase(BaseModelConfig):
    installation_visit_uid: int
    weather_station_uid: int
    download_date: dt.datetime
    download_quality: str
    clock_reset: bool
    public_tbl_good: bool
    status_tbl_good: bool
    hourly_tbl_good: bool
    daily_tbl_good: bool
    notes: str


class WeatherStationDownload(WeatherStationDownloadBase):
    weather_station_download_uid: int


class WeatherStationHourlyDataBase(BaseModelConfig):
    weather_station_uid: int
    weather_station_download_uid: int
    date_time: dt.datetime
    internal_temp_avg: float
    air_temp_avg: float
    wind_speed_avg: float
    wind_speed_std: float
    snow_depth: float


class WeatherStationHourlyData(WeatherStationHourlyDataBase):
    weather_station_hourly_data_uid: int


class WeatherStationDailyDataBase(BaseModelConfig):
    weather_station_uid: int
    weather_station_download_uid: int
    date_time: dt.datetime
    internal_temp_min: float
    internal_temp_max: float
    air_temp_avg: float
    air_temp_max: float
    time_air_temp_max: dt.datetime
    air_temp_min: float
    time_air_temp_min: dt.datetime
    wind_speed_avg: float
    wind_speed_max: float
    time_wind_speed_max: dt.datetime
    snow_depth: float


class WeatherStationDailyData(WeatherStationDailyDataBase):
    weather_station_daily_data_uid: int
