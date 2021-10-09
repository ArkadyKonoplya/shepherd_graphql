import datetime

import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from equipment.models import Equipment
from farm.models import (
    Farm,
    FarmUsers,
    OrganizationType,
    OrganizationLocationRel,
    OrganizationRole,
    OrganizationTypeLocationTypeRel,
    OrganizationRel,
)
from inventory.models import Inventory


class FarmType(DjangoObjectType):
    class Meta:
        model = Farm
        fields = ("id", "type", "name", "code")


class FarmCountType(graphene.ObjectType):

    field_count = graphene.Int()
    worker_count = graphene.Int()
    equipment_count = graphene.Int()
    inventory_count = graphene.Int()


class FarmUsersType(DjangoObjectType):
    class Meta:
        model = FarmUsers
        fields = ("id", "user", "farm", "role", "default_farm")


class OrganizationLocationRelType(DjangoObjectType):
    class Meta:
        model = OrganizationLocationRel
        fields = ("id", "farm", "location")


class OrganizationTypeType(DjangoObjectType):
    class Meta:
        model = OrganizationType
        fields = ("id", "name")


class OrganizationTypeLocationTypeRelType(DjangoObjectType):
    class Meta:
        model = OrganizationLocationRel
        fields = ("id", "farm", "location")


class OrganizationRelType(DjangoObjectType):
    class Meta:
        model = OrganizationRel
        fields = ("id", "parent_farm", "child_farm")


class OrganizationRoleType(DjangoObjectType):
    class Meta:
        model = OrganizationRole
        fields = ("id", "name")


class OrganizationTypeType(DjangoObjectType):
    class Meta:
        model = OrganizationType
        fields = ("id", "name")


class OrganizationTypeLocationTypeRelType(DjangoObjectType):
    class Meta:
        model = OrganizationTypeLocationTypeRel
        fields = ("id", "farm_type", "location_type")


class Query(graphene.ObjectType):
    check_valid_farm_code = graphene.Field(
        FarmType, code=graphene.String(required=True)
    )
    get_farm = graphene.Field(
        FarmType,
        farm=graphene.String(required=True),
        username=graphene.String(required=True),
    )
    get_farm_counts = graphene.Field(FarmCountType, farm=graphene.String(required=True))
    get_farm_locations = graphene.List(
        OrganizationLocationRelType, farm=graphene.String(required=True)
    )
    get_farm_roles = graphene.List(OrganizationRoleType)
    get_farm_types = graphene.List(OrganizationTypeType)
    get_user_farms = graphene.List(FarmType)

    def resolve_check_valid_farm_code(self, info, code):

        try:
            return Farm.objects.get(code=code, deleted_at=None)

        except Farm.DoesNotExist:
            raise (
                GraphQLError(
                    f"The farm with code {code} doesn't exist. Please check your code and try again."
                )
            )

    @login_required
    def resolve_get_farm(self, info, farm, username):
        return Farm.objects.get(
            pk=farm, member_farms__user__username=username, deleted_at=None
        )

    @login_required
    def resolve_get_farm_counts(self, info, farm):
        field_count = OrganizationLocationRel.objects.filter(
            farm__id=farm, deleted_at=None
        ).count()
        worker_count = FarmUsers.objects.filter(farm__id=farm, deleted_at=None).count()
        equipment_count = Equipment.objects.filter(
            farm__id=farm, deleted_at=None
        ).count()
        inventory_count = Inventory.objects.filter(
            farm_id_id=farm, deleted_at=None
        ).count()

        return FarmCountType(
            field_count=field_count,
            worker_count=worker_count,
            equipment_count=equipment_count,
            inventory_count=inventory_count,
        )

    @login_required
    def resolve_get_farm_locations(self, info, farm):
        return OrganizationLocationRel.objects.select_related(
            "location", "location__type"
        ).filter(
            farm_id=farm,
            deleted_at=None,
            farm__member_farms__user_id=info.context.user.id,
        )

    def resolve_get_farm_roles(self, info):
        return OrganizationRole.objects.filter(deleted_at=None)

    def resolve_get_farm_types(self, info):
        return OrganizationType.objects.filter(deleted_at=None)

    def resolve_get_user_farms(self, info):
        return FarmUsers.objects.filter(user_id=info.context.user.id, deleted_at=None)


schema = graphene.Schema(query=Query)
