from itertools import chain

import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from activity.models import Activity, ActivityDetail, ActivityDetailRel, CustomActivity, FarmTypeActivityRel, LocationTypeActivityType, BaseActivity


class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity
        fields = ("id", "name", "requires_crop", "sort_order")


class ActivityDetailType(DjangoObjectType):
    class Meta:
        model = ActivityDetail
        fields = ("id", "name")


class ActivityDetailRelType(DjangoObjectType):
    class Meta:
        model = ActivityDetailRel
        fields = ("id", "activity", "activity_detail", "sort_order")


class CustomActivityType(DjangoObjectType):
    class Meta:
        model = CustomActivity
        fields = ("id", "name", "farm")


class FarmTypeActivityRelType(DjangoObjectType):
    class Meta:
        model = FarmTypeActivityRel
        fields = ("id", "farm_type", "activity_type", "sort_order")


class LocationTypeActivityRelType(DjangoObjectType):
    class Meta:
        model = LocationTypeActivityType
        fields = ("id", "location_type", "activity_type")


class FarmActivities(graphene.Union):
    class Meta:
        types = (ActivityType, CustomActivityType)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, Activity):
            return ActivityType
        if isinstance(instance, CustomActivity):
            return CustomActivityType

        return FarmActivities.resolve_type(instance, info)


class Query(graphene.ObjectType):

    get_all_activity_types = graphene.List(ActivityType)
    get_all_activity_details = graphene.List(ActivityDetailType)
    get_activity_details = graphene.List(
        ActivityDetailRelType, activity_id=graphene.String(required=True)
    )
    get_farm_activities = graphene.List(FarmActivities, farm=graphene.String(required=True)
    )

    @login_required
    def resolve_get_all_activity_types(self, info):
        return Activity.objects.filter(deleted_at=None)

    @login_required
    def resolve_get_all_activity_details(self, info):
        return ActivityDetail.objects.filter(deleted_at=None)

    @login_required
    def resolve_get_activity_details(self, info, activity_id):
        return ActivityDetailRel.objects.prefetch_related("activity_detail").filter(
            activity_id=activity_id, deleted_at=None
        )

    @login_required
    def resolve_get_farm_activities(self, info, farm):

        farm_activities = Activity.objects.filter(
            farmtypeactivityrel__farm_type__farm=farm, deleted_at=None
        )

        custom_activities = CustomActivity.objects.filter(farm=farm, deleted_at=None)

        return list(chain(farm_activities, custom_activities))


schema = graphene.Schema(query=Query)
