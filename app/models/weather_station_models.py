# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-07
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import sqltypes

from database import Base


class WeatherStation(Base):
    __tablename__ = "weather_station"
    weather_station_uid = Column(sqltypes.Integer, primary_key=True)
    installation_uid = Column(sqltypes.Integer, ForeignKey("installation.installation_uid"), nullable=False)
    logger_serial_number = Column(sqltypes.String, nullable=False)
    date_installed = Column(sqltypes.DateTime(timezone=True), nullable=False)
    battery_year = Column(sqltypes.SmallInteger,  nullable=False)
    at_status = Column(sqltypes.String)
    anemo_status = Column(sqltypes.String)
    snow_status = Column(sqltypes.String)

    def __init__(self, installation_uid, logger_serial_number, date_installed, battery_year, at_status, anemo_status,
                 snow_status):
        self.installation_uid = installation_uid
        self.logger_serial_number = logger_serial_number
        self.date_installed = date_installed
        self.battery_year = battery_year
        self.at_status = at_status
        self.anemo_status = anemo_status
        self.snow_status = snow_status
        return


class WeatherStationDownload(Base):
    __tablename__ = "weather_station_download"
    weather_station_download_uid = Column(sqltypes.Integer, primary_key=True)
    installation_visit_uid = Column(sqltypes.Integer, ForeignKey("installation_visit.installation_visit_uid"),
                                    nullable=False)
    weather_station_uid = Column(sqltypes.Integer, ForeignKey("weather_station.weather_station_uid"), nullable=False)
    download_date = Column(sqltypes.DateTime(timezone=True), nullable=False)
    download_quality = Column(sqltypes.String)
    clock_reset = Column(sqltypes.Boolean)
    public_tbl_good = Column(sqltypes.Boolean)
    status_tbl_good = Column(sqltypes.Boolean)
    daily_tbl_good = Column(sqltypes.Boolean)
    hourly_tbl_good = Column(sqltypes.Boolean)
    notes = Column(sqltypes.String)

    def __init__(self, installation_visit_uid, weather_station_uid, download_date, download_quality, clock_reset,
                 public_tbl_good, status_tbl_good, daily_tbl_good, hourly_tbl_good, notes):
        self.installation_visit_uid = installation_visit_uid
        self.weather_station_uid = weather_station_uid
        self.download_date = download_date
        self.download_quality = download_quality
        self.clock_reset = clock_reset
        self.public_tbl_good = public_tbl_good
        self.status_tbl_good = status_tbl_good
        self.hourly_tbl_good = hourly_tbl_good
        self.daily_tbl_good = daily_tbl_good
        self.notes = notes
        return


class WeatherStationDailyData(Base):
    __tablename__ = "weather_station_daily_data"
    weather_station_daily_data_uid = Column(sqltypes.Integer, primary_key=True)
    weather_station_uid = Column(sqltypes.Integer, ForeignKey("weather_station.weather_station_uid"), nullable=False)
    weather_station_download_uid = Column(sqltypes.Integer,
                                          ForeignKey("weather_station_download.weather_station_download_uid"),
                                          nullable=False)
    date_time = Column(sqltypes.DateTime(timezone=True), nullable=False)
    internal_temp_min = Column(sqltypes.Float)
    internal_temp_max = Column(sqltypes.Float)
    air_temp_avg = Column(sqltypes.Float)
    air_temp_max = Column(sqltypes.Float)
    time_air_temp_max = Column(sqltypes.DateTime(timezone=True))
    air_temp_min = Column(sqltypes.Float)
    time_air_temp_min = Column(sqltypes.DateTime(timezone=True))
    wind_speed_avg = Column(sqltypes.Float)
    wind_speed_max = Column(sqltypes.Float)
    time_wind_speed_max = Column(sqltypes.DateTime(timezone=True))
    snow_depth = Column(sqltypes.Float)

    def __init__(self, weather_station_uid, weather_station_download_uid, date_time, internal_temp_min,
                 internal_temp_max, air_temp_avg, air_temp_max, time_air_temp_max, air_temp_min, time_air_temp_min,
                 wind_speed_avg, wind_speed_max, time_wind_speed_max, snow_depth):
        self.weather_station_uid = weather_station_uid
        self.weather_station_download_uid = weather_station_download_uid
        self.date_time = date_time
        self.internal_temp_min = internal_temp_min
        self.internal_temp_max = internal_temp_max
        self.air_temp_avg = air_temp_avg
        self.air_temp_max = air_temp_max
        self.time_air_temp_max = time_air_temp_max
        self.air_temp_min = air_temp_min
        self.time_air_temp_min = time_air_temp_min
        self.wind_speed_avg = wind_speed_avg
        self.wind_speed_max = wind_speed_max
        self.time_wind_speed_max = time_wind_speed_max
        self.snow_depth = snow_depth
        return


class WeatherStationHourlyData(Base):
    __tablename__ = "weather_station_hourly_data"
    weather_station_hourly_data_uid = Column(sqltypes.Integer, primary_key=True)
    weather_station_uid = Column(sqltypes.Integer, ForeignKey("weather_station.weather_station_uid"), nullable=False)
    weather_station_download_uid = Column(sqltypes.Integer,
                                          ForeignKey("weather_station_download.weather_station_download_uid"),
                                          nullable=False)
    date_time = Column(sqltypes.DateTime(timezone=True), nullable=False)
    internal_temp_avg = Column(sqltypes.Float)
    air_temp_avg = Column(sqltypes.Float)
    wind_speed_avg = Column(sqltypes.Float)
    wind_speed_std = Column(sqltypes.Float)
    snow_depth = Column(sqltypes.Float)

    def __init__(self, weather_station_uid, weather_station_download_uid, date_time, internal_temp_avg=None,
                 air_temp_avg=None, wind_speed_avg=None, wind_speed_std=None, snow_depth=None):
        self.weather_station_uid = weather_station_uid
        self.weather_station_download_uid = weather_station_download_uid
        self.date_time = date_time
        self.internal_temp_avg = internal_temp_avg
        self.air_temp_avg = air_temp_avg
        self.wind_speed_avg = wind_speed_avg
        self.wind_speed_std = wind_speed_std
        self.snow_depth = snow_depth
        return
