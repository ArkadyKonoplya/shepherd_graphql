import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from equipment.models import (
    Equipment,
    EquipmentModel,
    EquipmentMake,
    EquipmentType as EQType,
    EquipmentUser,
)


class EquipmentType(DjangoObjectType):
    class Meta:
        model = Equipment
        fields = ("id", "make_model", "name", "farm", "serial_num", "equipment_type")


class EquipmentInput(graphene.InputObjectType):
    equipment = graphene.String()


class EquipmentMakeType(DjangoObjectType):
    class Meta:
        model = EquipmentMake
        interfaces = (relay.Node,)
        fields = ("id", "name")

    id = graphene.ID(source="id", required=True)


class EquipmentMakeConnection(relay.Connection):
    search = graphene.String()

    class Meta:
        node = EquipmentMakeType


class EquipmentModelType(DjangoObjectType):
    class Meta:
        model = EquipmentModel
        interfaces = (relay.Node,)
        fields = ("id", "make", "name", "equipment_type")

    id = graphene.ID(source="id", required=True)


class EquipmentModelConnection(relay.Connection):
    search = graphene.String()
    make_id = graphene.String()

    class Meta:
        node = EquipmentModelType


class EquipmentTypeType(DjangoObjectType):
    class Meta:
        model = EQType
        fields = ("id", "name")


class EquipmentUserType(DjangoObjectType):
    class Meta:
        model = EquipmentUser
        fields = ("id", "equipment", "user")


class Query(graphene.ObjectType):
    get_all_farm_equipment = graphene.List(
        EquipmentType, farm=graphene.String(required=True)
    )
    get_farm_equipment = graphene.Field(EquipmentType, farm=graphene.String(required=True), equipment_id=graphene.String(required=True))
    get_all_equipment_makes = relay.ConnectionField(EquipmentMakeConnection)
    get_all_equipment_models = relay.ConnectionField(EquipmentModelConnection)
    get_all_equipment_types = graphene.List(EquipmentTypeType)
    find_equipment_make = relay.ConnectionField(EquipmentMakeConnection, search=graphene.String())
    find_equipment_model = relay.ConnectionField(EquipmentModelConnection, search=graphene.String(), make_id=graphene.String(required=True), equipment_type=graphene.String())

    @login_required
    def resolve_get_all_farm_equipment(self, info, farm):
        return Equipment.objects.filter(
            farm=farm, deleted_at=None, farm__member_farms__user_id=info.context.user.id
        )

    @login_required
    def resolve_get_farm_equipment(self, info, farm, equipment_id):
        return Equipment.objects.get(
            farm=farm, id=equipment_id, deleted_at=None, farm__member_farms__user_id=info.context.user.id
        )

    @login_required
    def resolve_get_all_equipment_makes(self, info, **kwargs):
        return EquipmentMake.objects.filter(deleted_at=None)

    @login_required
    def resolve_get_all_equipment_models(self, info, **kwargs):
        return EquipmentModel.objects.filter(deleted_at=None)

    @login_required
    def resolve_get_all_equipment_types(self, info):
        return EQType.objects.filter(deleted_at=None)

    @login_required
    def resolve_find_equipment_make(self, info, **kwargs):
        search = kwargs.get("search", None)
        if search:
            return EquipmentMake.objects.filter(name__contains=search, deleted_at=None)
        else:
            return EquipmentMake.objects.filter(deleted_at=None)

    @login_required
    def resolve_find_equipment_model(self, info, make_id, **kwargs):
        search = kwargs.get("search", None)
        equipment_type = kwargs.get("equipment_type", None)
        equipment_models = EquipmentModel.objects.filter(make_id=make_id, deleted_at=None)

        if search:
            equipment_models = equipment_models.filter(name__contains=search)

        if equipment_type:
            equipment_models = equipment_models.filter(equipment_type__id=equipment_type)

        return equipment_models


schema = graphene.Schema(query=Query)
