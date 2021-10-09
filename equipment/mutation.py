import datetime

import graphene
from graphql_jwt.decorators import login_required

from equipment.models import Equipment, EquipmentModel
from farm.models import Farm
from equipment.schema import EquipmentType


class EquipmentAddMutation(graphene.Mutation):

    equipment = graphene.Field(EquipmentType)

    class Arguments:
        make_model = graphene.String()
        name = graphene.String(required=True)
        farm = graphene.String(required=True)
        serial_num = graphene.String()
        equipment_type = graphene.String()

    @login_required
    def mutate(self, info, name, farm, **kwargs):
        serial_num = kwargs.get("serial_num", None)
        make_model = kwargs.get("make_model", None)
        equipment_type = kwargs.get("equipment_type", None)

        farm = Farm.objects.get(id=farm)

        new_equipment = Equipment()
        if make_model is not None:
            new_equipment.make_model_id = make_model

        new_equipment.name = name
        new_equipment.farm = farm
        new_equipment.created_by = info.context.user.id
        new_equipment.modified_by = info.context.user.id

        if serial_num is not None:
            new_equipment.serial_num = serial_num

        if equipment_type is not None:
            new_equipment.equipment_type_id = equipment_type

        new_equipment.save()

        return EquipmentAddMutation(equipment=new_equipment)


class EquipmentDeleteMutation(graphene.Mutation):

    success = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)

    @login_required
    def mutate(self, info, id):
        equipment_item = Equipment.objects.get(pk=id)
        equipment_item.deleted_by = info.context.user.id
        equipment_item.deleted_at = datetime.datetime.now(datetime.timezone.utc)
        equipment_item.save()

        return EquipmentDeleteMutation(success=True)


class EquipmentUpdateMutation(graphene.Mutation):

    success = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)
        make_model = graphene.String()
        name = graphene.String(required=True)
        farm = graphene.String(required=True)
        serial_num = graphene.String()
        equipment_type = graphene.String()

    @login_required
    def mutate(self, info, id, name, farm, **kwargs):
        serial_num = kwargs.get("serial_num", None)
        make_model = kwargs.get("make_model", None)
        equipment_type = kwargs.get("equipment_type", None)

        farm = Farm.objects.get(id=farm)

        equipment_item = Equipment.objects.get(pk=id)

        equipment_item.farm = farm
        if serial_num is not None:
            equipment_item.serial_num = serial_num

        equipment_item.name = name

        if make_model is not None:
            equipment_item.make_model_id = make_model

        if equipment_type is not None:
            equipment_item.equipment_type_id = equipment_type


        equipment_item.save()

        return EquipmentUpdateMutation(success=True)


class Mutation(graphene.ObjectType):
    add_equipment = EquipmentAddMutation.Field()
    delete_equipment = EquipmentDeleteMutation.Field()
    update_equipment = EquipmentUpdateMutation.Field()
