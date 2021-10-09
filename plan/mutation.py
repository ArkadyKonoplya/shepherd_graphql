import datetime

import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from plan.schema import PlanInput, PlanType

from crop.models import Crop
from farm.models import FarmUsers
from field.models import Location
from plan.models import Plan
from user.models import ShepherdUser


class PlanAddMutation(graphene.Mutation):

    plan = graphene.Field(PlanType)

    class Arguments:
        crop = graphene.String(required=True)
        location = graphene.String(required=True)
        plan_year = graphene.String(required=True)

    @login_required
    def mutate(self, info, crop, location, plan_year):
        crop = Crop.objects.get(id=crop)
        location = Location.objects.get(id=location)
        planner = ShepherdUser.objects.get(id=info.context.user.id)

        new_plan = Plan()
        new_plan.crop = crop
        new_plan.location = location
        new_plan.plan_year = plan_year
        new_plan.planner = planner
        new_plan.created_by = info.context.user.id
        new_plan.modified_by = info.context.user.id
        new_plan.save()

        return PlanAddMutation(plan=new_plan)


class PlanDeleteMutation(graphene.Mutation):

    success = graphene.Boolean()

    class Arguments:
        plan = graphene.String(required=True)

    @login_required
    def mutate(self, info, plan):

        plan = Plan.objects.get(id=plan)

        try:
            user_allowed = FarmUsers.objects.filter(
                user_id=info.context.user.id,
                role__name__in=("manager", "owner"),
                farm__location=plan.location,
            )

        except FarmUsers.DoesNotExist:
            user_allowed = None

        if user_allowed:
            plan.deleted_at = datetime.datetime.now(datetime.timezone.utc)
            plan.deleted_by = info.context.user.id
            plan.save()

        return PlanDeleteMutation(success=True)


class Mutation(graphene.ObjectType):
    add_plan = PlanAddMutation.Field()
    delete_plan = PlanDeleteMutation.Field()