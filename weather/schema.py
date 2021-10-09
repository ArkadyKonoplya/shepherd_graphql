import datetime
import json
import os

import graphene
from graphql_jwt.decorators import login_required

from darksky.api import DarkSky

darksky_key = os.getenv("darksky_api_key")


class CurrentWeatherType(graphene.ObjectType):

    time = graphene.DateTime()
    summary = graphene.String()
    icon = graphene.String()
    nearest_storm_distance = graphene.Int()
    nearest_storm_bearing = graphene.Int()
    precip_intensity = graphene.Float()
    precip_intensity_error = graphene.Float()
    precip_probability = graphene.Float()
    precip_type = graphene.String()
    precip_accumulation = graphene.Float()
    temperature = graphene.Float()
    apparent_temperature = graphene.Float()
    dew_point = graphene.Float()
    humidity = graphene.Float()
    pressure = graphene.Float()
    wind_speed = graphene.Float()
    wind_gust = graphene.Float()
    wind_bearing = graphene.Int()
    cloud_cover = graphene.Float()
    uv_index = graphene.Float()
    visibility = graphene.Float()
    ozone = graphene.Float()


class MinuteWeatherItemType(graphene.ObjectType):

    time = graphene.DateTime()
    precip_intensity = graphene.Float()
    precip_intensity_error = graphene.Float()
    precip_probability = graphene.Float()
    precip_type = graphene.String()


class HourWeatherItemType(graphene.ObjectType):

    time = graphene.DateTime()
    summary = graphene.String()
    icon = graphene.String()
    precip_intensity = graphene.Float()
    precip_probability = graphene.Float()
    precip_type = graphene.String()
    precip_accumulation = graphene.Float()
    temperature = graphene.Float()
    apparent_temperature = graphene.Float()
    dew_point = graphene.Float()
    humidity = graphene.Float()
    pressure = graphene.Float()
    wind_speed = graphene.Float()
    wind_gust = graphene.Float()
    wind_bearing = graphene.Int()
    cloud_cover = graphene.Float()
    uv_index = graphene.Int()
    visibility = graphene.Float()
    ozone = graphene.Float()


class DayWeatherItemType(graphene.ObjectType):

    time = graphene.DateTime()
    summary = graphene.String()
    icon = graphene.String()
    sunrise_time = graphene.DateTime()
    sunset_time = graphene.DateTime()
    moon_phase = graphene.Float()
    precip_intensity = graphene.Float()
    precip_intensity_max = graphene.Float()
    precip_intensity_max_time = graphene.DateTime()
    precip_probability = graphene.Float()
    precip_type = graphene.String()
    precip_accumulation = graphene.Float()
    temperature_high = graphene.Float()
    temperature_high_time = graphene.DateTime()
    temperature_low = graphene.Float()
    temperature_low_time = graphene.DateTime()
    dew_point = graphene.Float()
    humidity = graphene.Float()
    pressure = graphene.Float()
    wind_speed = graphene.Float()
    wind_gust = graphene.Float()
    wind_gust_time = graphene.DateTime()
    wind_bearing = graphene.Int()
    cloud_cover = graphene.Float()
    uv_index = graphene.Int()
    uv_index_time = graphene.DateTime()
    visibility = graphene.Int()
    ozone = graphene.Float()
    temperature_min = graphene.Float()
    temperature_min_time = graphene.DateTime()
    temperature_max = graphene.Float()
    temperature_max_time = graphene.DateTime()
    apparent_temperature_min = graphene.Float()
    apparent_temperature_min_time = graphene.DateTime()
    apparent_temperature_max = graphene.Float()
    apparent_temperature_max_time = graphene.DateTime()


class AlertWeatherItemType(graphene.ObjectType):

    title = graphene.String()
    regions = graphene.List(graphene.String)
    severity = graphene.String()
    time = graphene.DateTime()
    expires = graphene.DateTime()
    description = graphene.String()
    uri = graphene.String()


class HistoricalWeatherType(graphene.ObjectType):

    daily_potential_precip = graphene.Float()

    def resolve_daily_potential_precip(self, info):
        return self.daily_potential_precip


class WeatherType(graphene.ObjectType):

    currently = graphene.Field(CurrentWeatherType)
    minutely = graphene.List(MinuteWeatherItemType)
    hourly = graphene.List(HourWeatherItemType)
    daily = graphene.List(DayWeatherItemType)
    alerts = graphene.List(AlertWeatherItemType)
    historical = graphene.List(HistoricalWeatherType)

    def resolve_currently(self, info):
        return self.currently

    def resolve_minutely(self, info):
        return self.minutely

    def resolve_hourly(self, info):
        return self.hourly

    def resolve_daily(self, info):
        return self.daily

    def resolve_alerts(self, info):
        return self.alerts

    def resolve_historical(self, info):
        return self.historical


def list_converter(item_type, item):
    """
    Take dark sky object and turn it into a json array.
    :param item_type:
    :param item:
    :return:
    """
    valid_item_types = [
        "currently",
        "minutely",
        "hourly",
        "daily",
        "alerts",
        "historical",
    ]

    if item_type not in valid_item_types:
        raise Exception(
            f"Invalid item type provided.  Valid types are: {valid_item_types}"
        )

    if item_type == "currently":
        weather_data = CurrentWeatherType(
            time=item.time,
            summary=item.summary,
            icon=item.icon,
            nearest_storm_distance=item.nearest_storm_distance,
            nearest_storm_bearing=item.nearest_storm_bearing,
            precip_intensity=item.precip_intensity,
            precip_intensity_error=item.precip_intensity_error,
            precip_probability=item.precip_probability,
            precip_type=item.precip_type,
            precip_accumulation=item.precipAccumulation,
            temperature=item.temperature,
            apparent_temperature=item.apparent_temperature,
            dew_point=item.dew_point,
            humidity=item.humidity,
            pressure=item.pressure,
            wind_speed=item.wind_speed,
            wind_gust=item.wind_gust,
            wind_bearing=item.wind_bearing,
            cloud_cover=item.cloud_cover,
            uv_index=item.uv_index,
            visibility=item.visibility,
            ozone=item.ozone,
        )

    elif item_type == "daily":
        weather_data = []

        for day in item.data:
            day_data = DayWeatherItemType(
                time=day.time,
                summary=day.summary,
                icon=day.icon,
                sunrise_time=day.sunrise_time,
                sunset_time=day.sunset_time,
                moon_phase=day.moon_phase,
                precip_intensity=day.precip_intensity,
                precip_intensity_max=day.precip_intensity_max,
                precip_intensity_max_time=day.precip_intensity_max_time,
                precip_probability=day.precip_probability,
                precip_type=day.precip_type,
                precip_accumulation=day.precipAccumulation,
                temperature_high=day.temperature_high,
                temperature_high_time=day.temperature_high_time,
                temperature_low=day.temperature_low,
                temperature_low_time=day.temperature_low_time,
                dew_point=day.dew_point,
                humidity=day.humidity,
                pressure=day.pressure,
                wind_speed=day.wind_speed,
                wind_gust=day.wind_gust,
                wind_gust_time=day.wind_gust_time,
                wind_bearing=day.wind_bearing,
                cloud_cover=day.cloud_cover,
                uv_index=day.uv_index,
                uv_index_time=day.uv_index_time,
                visibility=day.visibility,
                ozone=day.ozone,
                temperature_min=day.temperature_min,
                temperature_min_time=day.temperature_min_time,
                temperature_max=day.temperature_max,
                temperature_max_time=day.temperature_max_time,
                apparent_temperature_min=day.apparent_temperature_min,
                apparent_temperature_min_time=day.apparent_temperature_min_time,
                apparent_temperature_max=day.apparent_temperature_max,
                apparent_temperature_max_time=day.apparent_temperature_max_time,
            )
            weather_data.append(day_data)

    elif item_type == "hourly":
        weather_data = []

        for hour in item.data:
            hour_data = HourWeatherItemType(
                time=hour.time,
                summary=hour.summary,
                icon=hour.icon,
                precip_intensity=hour.precip_intensity,
                precip_probability=hour.precip_probability,
                precip_type=hour.precip_type,
                precip_accumulation=hour.precipAccumulation,
                temperature=hour.temperature,
                apparent_temperature=hour.apparent_temperature,
                dew_point=hour.dew_point,
                humidity=hour.humidity,
                pressure=hour.pressure,
                wind_speed=hour.wind_speed,
                wind_gust=hour.wind_gust,
                wind_bearing=hour.wind_bearing,
                cloud_cover=hour.cloud_cover,
                uv_index=hour.uv_index,
                visibility=hour.visibility,
                ozone=hour.ozone,
            )
            weather_data.append(hour_data)

    elif item_type == "minutely":
        weather_data = []
        for minute in item.data:
            minute_data = MinuteWeatherItemType(
                time=minute.time,
                precip_intensity=minute.precip_intensity,
                precip_intensity_error=minute.precip_intensity_error,
                precip_probability=minute.precip_probability,
                precip_type=minute.precip_type,
            )

            weather_data.append(minute_data)

    elif item_type == "alerts":
        weather_data = []
        for alert in item:
            alert_data = AlertWeatherItemType(
                title=alert.title,
                regions=alert.regions,
                severity=alert.severity,
                time=alert.time,
                expires=alert.expires,
                description=alert.description,
                uri=alert.uri,
            )

            weather_data.append(alert_data)

    elif item_type == "historical":
        weather_data = []
        for day in item.daily.data:
            daily_potential_precip = round(day.precip_intensity * day.precip_probability, 2)

            historical_weather = HistoricalWeatherType(
                daily_potential_precip=daily_potential_precip
            )

            weather_data.append(historical_weather)

    return weather_data


def convert_weather(weather, **kwargs):
    """
    Given the darksky weather object, convert into Graphene objects.
    :param weather: dark sky weather data for location
    :param historical_weather: dark sky time machine weather data for same location
    :return:
    """

    historical_weather = kwargs.get("historical_weather", None)

    currently = list_converter(item_type="currently", item=weather.currently)
    minutely = list_converter(item_type="minutely", item=weather.minutely)
    hourly = list_converter(item_type="hourly", item=weather.hourly)
    daily = list_converter(item_type="daily", item=weather.daily)
    alerts = list_converter(item_type="alerts", item=weather.alerts)
    if historical_weather:
        historical_weather = list_converter(
            item_type="historical", item=historical_weather
        )

    return WeatherType(
        currently=currently,
        minutely=minutely,
        hourly=hourly,
        daily=daily,
        alerts=alerts,
        historical=historical_weather,
    )


class Query(graphene.ObjectType):
    get_weather = graphene.Field(
        WeatherType,
        latitude=graphene.Float(required=True),
        longitude=graphene.Float(required=True),
    )

    @login_required
    def resolve_get_weather(self, info, latitude, longitude):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

        darksky = DarkSky(darksky_key)
        weather = darksky.get_forecast(latitude=latitude, longitude=longitude)
        historical_weather = darksky.get_time_machine_forecast(
            latitude=latitude, longitude=longitude, time=yesterday
        )

        return convert_weather(weather=weather, historical_weather=historical_weather)
