import datetime

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from fcm_django.models import FCMDevice

from user.models import (
    ShepherdUser,
    UserPointActivity,
    PointActivityType as PointActivity,
    PointLevels,
)
from farm.models import FarmUsers
from farm.schema import FarmUsersType


class ShepherdUserType(DjangoObjectType):
    class Meta:
        model = ShepherdUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "current_points",
            "lifetime_points",
            "onboard_complete",
            "timezone",
            "farms",
        )

    farms = graphene.List(FarmUsersType)

    def resolve_farms(value_obj, info):
        return value_obj.farm_members.all()


class FcmDeviceType(DjangoObjectType):
    class Meta:
        model = FCMDevice
        fields = ("registration_id", "name", "active", "user", "device_id", "type")


class UserPointActivityType(DjangoObjectType):
    class Meta:
        model = UserPointActivity
        fields = (
            "id",
            "user",
            "point_activity",
            "points_earned_spent",
            "activity_date",
        )


class PointActivityType(DjangoObjectType):
    class Meta:
        model = PointActivity
        fields = (
            "id",
            "point_activity_name",
            "point_activity_description",
            "default_point_value",
            "max_times_earnable",
            "available_from_date",
            "available_to_date",
        )


class PointLevelType(DjangoObjectType):
    class Meta:
        model = PointLevels
        fields = ("id", "point_level_name", "points_required")


class Query(graphene.ObjectType):
    check_unique_email = graphene.Boolean(email=graphene.String(required=True))
    check_unique_username = graphene.Boolean(username=graphene.String(required=True))
    get_user_by_username = graphene.List(
        ShepherdUserType, username=graphene.String(required=True)
    )
    get_user_by_email = graphene.List(
        ShepherdUserType, email=graphene.String(required=True)
    )
    get_farm_users = graphene.List(FarmUsersType, farm=graphene.String(required=True))
    get_worker_profile = graphene.List(
        ShepherdUserType, user_id=graphene.String(required=True)
    )
    get_point_activities = graphene.List(PointActivityType)
    get_point_levels = graphene.List(PointLevelType)

    def resolve_check_unique_email(self, info, email):
        email_count = ShepherdUser.objects.filter(email=email, deleted_at=None).count()

        if email_count >= 1:
            return False
        else:
            return True

    def resolve_check_unique_username(self, info, username):
        username_count = ShepherdUser.objects.filter(
            username=username, deleted_at=None
        ).count()

        if username_count >= 1:
            return False
        else:
            return True

    @login_required
    def resolve_get_user_by_email(self, info, email):
        return ShepherdUser.objects.filter(email=email, deleted_at=None)

    @login_required
    def resolve_get_user_by_username(self, info, username):
        return ShepherdUser.objects.filter(username=username, deleted_at=None)

    @login_required
    def resolve_get_farm_users(self, info, farm):
        return FarmUsers.objects.select_related("user", "role").filter(
            farm=farm, deleted_at=None
        )

    @login_required
    def resolve_get_worker_profile(self, info, user_id):
        return ShepherdUser.objects.filter(id=user_id, deleted_at=None)

    def resolve_get_point_activities(self, info):
        return PointActivity.objects.filter(
            available_to_date__gte=datetime.datetime.now(tz=datetime.timezone.utc),
            deleted_at=None,
        )

    def resolve_get_point_levels(self, info):
        return PointLevels.objects.filter(deleted_at=None)


schema = graphene.Schema(query=Query)
