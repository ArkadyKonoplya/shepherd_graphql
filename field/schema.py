import datetime
import os

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphene_gis.scalars import PolygonScalar, PointScalar
from graphene_gis.converter import gis_converter
from darksky.api import DarkSky

from field.models import LocationType as LocType, Location
from task.models import TaskHistory

from task.schema import TaskHistoryType
from weather.schema import convert_weather, WeatherType

darksky_key = os.getenv("darksky_api_key")


class LocationTypeType(DjangoObjectType):
    class Meta:
        model = LocType
        fields = ("id", "name")


class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = (
            "id",
            "name",
            "type",
            "acres",
            "image",
            "geo_center",
            "drawn_area",
            "legal_name",
            "organization",
            "weather",
        )

    weather = graphene.Field(WeatherType)

    def resolve_weather(value_obj, info):
        geo_center = value_obj.geo_center
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

        darksky = DarkSky(darksky_key)
        weather = darksky.get_forecast(
            latitude=geo_center.coords[1], longitude=geo_center.coords[0]
        )
        historical_weather = darksky.get_time_machine_forecast(
            latitude=geo_center.coords[1], longitude=geo_center.coords[0], time=yesterday)

        return convert_weather(weather=weather, historical_weather=historical_weather)


class Query(graphene.ObjectType):
    get_all_location_types = graphene.List(LocationTypeType)
    get_location = graphene.Field(
        LocationType, location_id=graphene.String(required=True)
    )
    get_location_activity_log = graphene.List(TaskHistoryType, location_id=graphene.String(required=True))

    @login_required
    def resolve_get_all_location_types(self, info):
        return LocType.objects.filter(deleted_at=None)

    @login_required
    def resolve_get_location(self, info, location_id):
        return Location.objects.get(id=location_id, deleted_at=None)

    @login_required
    def resolve_get_location_activity_log(self, info, location_id):
        today = datetime.datetime.today()
        min_date = today - datetime.timedelta(days=90)

        return TaskHistory.objects.filter(task_id__task_plan__location_id=location_id, status_date_change__gte=min_date)


schema = graphene.Schema(query=Query)
