import datetime

import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from equipment.models import Equipment
from farm.models import Farm, FarmUsers, OrganizationRole
from field.models import Location
from user.models import ShepherdUser

from farm.schema import FarmType, FarmUsersType


class FarmCreateMutation(graphene.Mutation):
    class Arguments:
        farm_type = graphene.String(required=True)
        name = graphene.String(required=True)
        code = graphene.String()

    farm = graphene.Field(FarmType)

    @login_required
    def mutate(self, info, farm_type, name, code):
        farm = Farm(type_id=farm_type, name=name, code=code)
        farm.created_by = info.context.user.id
        farm.modified_by = info.context.user.id
        farm.save()

        # Adding default items on farm creation
        equipment = Equipment(name="By Hand", farm=farm)
        equipment.created_by = info.context.user.id
        equipment.modified_by = info.context.user.id
        equipment.created_at = datetime.datetime.now()
        equipment.modified_at = datetime.datetime.now()
        equipment.save()

        return FarmCreateMutation(farm=farm)


class FarmDeleteMutation(graphene.Mutation):
    class Arguments:
        farm_id = graphene.ID()

    farm = graphene.Field(FarmType)

    @login_required
    def mutate(self, info, farm_id):
        farm = Farm.objects.get(pk=farm_id)
        farm.deleted_at = datetime.datetime.now(datetime.timezone.utc)
        farm.deleted_by = info.context.user.id

        return FarmDeleteMutation(farm=farm)


class FarmUserAddMutation(graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)
        farm = graphene.String(required=True)
        role = graphene.String(required=True)

    farm_user = graphene.Field(FarmUsersType)

    @login_required
    def mutate(self, info, user, farm, role):

        farm_count = FarmUsers.objects.filter(user_id=user).count()
        already_member = FarmUsers.objects.filter(user_id=user, farm_id=farm).count()

        if already_member == 0:

            farm_user = FarmUsers(user_id=user, farm_id=farm, role_id=role)
            farm_user.created_by = info.context.user.id
            farm_user.modified_by = info.context.user.id

            if farm_count == 0:
                farm_user.default_farm = True

            farm_user.save()

        else:
            raise GraphQLError("User is already member of this farm.")

        return FarmUserAddMutation(farm_user=farm_user)


class FarmUserRemoveMutation(graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)
        farm = graphene.String(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, user, farm):

        farm_user = FarmUsers.objects.filter(farm=farm, user=user, deleted_at=None)

        owner_role = OrganizationRole.objects.get(name="owner")

        for role in farm_user:
            if role.role.pk != owner_role.pk:
                role.deleted_by = info.context.user.id
                role.deleted_at = datetime.datetime.now(datetime.timezone.utc)
                role.save()
            else:
                raise GraphQLError("Owners are unable to be removed from their farms.")

        return FarmUserRemoveMutation(success=True)


class FarmUserUpdateMutation(graphene.Mutation):
    class Arguments:
        user = graphene.String(required=True)
        farm = graphene.String(required=True)
        role = graphene.String(required=True)
        default_farm = graphene.Boolean()

    farm_user = graphene.Field(FarmUsersType)

    @login_required
    def mutate(self, info, user, farm, role, **kwargs):
        default_farm = kwargs.get("default_farm", None)

        farm_user = FarmUsers.objects.get(farm_id=farm, user_id=user)
        farm_user.role_id = role

        if default_farm:
            farm_user.default_farm = default_farm

            old_default_farm = FarmUsers.objects.get(user_id=user, default_farm=True)
            old_default_farm.default_farm = False
            old_default_farm.modified_by = info.context.user.id
            old_default_farm.save()

        farm_user.save()

        return FarmUserUpdateMutation(farm_user=farm_user)


class Mutation(graphene.ObjectType):
    add_farm = FarmCreateMutation.Field()
    add_farm_user = FarmUserAddMutation.Field()
    remove_farm_user = FarmUserRemoveMutation.Field()
    update_farm_user = FarmUserUpdateMutation.Field()

    remove_farm = FarmDeleteMutation.Field()
