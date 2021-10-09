import datetime

import graphene
from graphql_jwt.decorators import login_required

from activity.schema import CustomActivityType

from activity.models import CustomActivity
from farm.models import Farm


class CustomActivityAddMutation(graphene.Mutation):

    custom_activity = graphene.Field(CustomActivityType)

    class Arguments:
        name = graphene.String(required=True)
        requires_crop = graphene.Boolean(required=True)

    @login_required
    def mutate(self, info, name, requires_crop):

        farm = Farm.objects.get(member_farms__default_farm=True, member_farms__user_id=info.context.user.id)

        new_custom_activity = CustomActivity(
            farm=farm,
            name=name,
            requires_crop=requires_crop,
            created_by=info.context.user.id,
            modified_by=info.context.user.id
        )

        new_custom_activity.save()

        return CustomActivityAddMutation(custom_activity=new_custom_activity)


class CustomActivityUpdateMutation(graphene.Mutation):

    success = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        requires_crop = graphene.Boolean(required=True)

    @login_required
    def mutate(self, info, id, name, requires_crop):
        custom_activity = CustomActivity.objects.get(id=id)

        farm = Farm.objects.get(member_farms__default_farm=True, member_farms__user_id=info.context.user.id)

        if custom_activity.farm.id == farm.id:
            custom_activity.name = name
            custom_activity.requires_crop = requires_crop
            custom_activity.modified_by = info.context.user.id

            custom_activity.save()

        return CustomActivityUpdateMutation(success=True)


class CustomActivityDeleteMutation(graphene.Mutation):

    success = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)

    @login_required
    def mutate(self, info, id):
        custom_activity = CustomActivity.objects.get(id=id)

        farm = Farm.objects.get(member_farms__default_farm=True, member_farms__user_id=info.context.user.id)

        if custom_activity.farm.id == farm.id:

            custom_activity.deleted_by = info.context.user.id
            custom_activity.deleted_at = datetime.datetime.now(datetime.timezone.utc)
            custom_activity.save()

            return CustomActivityDeleteMutation(success=True)


class Mutation(graphene.ObjectType):
    add_custom_activity = CustomActivityAddMutation.Field()
    update_custom_activity = CustomActivityUpdateMutation.Field()
    delete_custom_activity = CustomActivityDeleteMutation.Field()