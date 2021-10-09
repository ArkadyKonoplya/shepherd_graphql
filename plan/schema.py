import datetime

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql import GraphQLError

from plan.models import Plan
from task.models import TaskHistory

from task.schema import TaskType, TaskHistoryType


class PlanType(DjangoObjectType):
    class Meta:
        model = Plan
        fields = ("id", "crop", "location", "planner", "plan_year", "tasks")

    tasks = graphene.List(TaskType)

    def resolve_tasks(value_obj, info):
        return value_obj.plan_tasks.exclude(task_status__name="deleted")


class PlanInput(graphene.InputObjectType):
    plan = graphene.String()


class Query(graphene.ObjectType):
    get_farm_plans = graphene.List(PlanType, farm_id=graphene.String(required=True))
    get_location_plans = graphene.List(
        PlanType, location=graphene.String(required=True)
    )
    get_plan_tasks = graphene.List(TaskType, plan_id=graphene.String(required=True))
    get_farm_plan = graphene.Field(PlanType, farm_id=graphene.String(required=True), plan_id=graphene.String(required=True))
    get_plan_activity_log = graphene.List(TaskHistoryType, plan_id=graphene.String(required=True))

    @login_required
    def resolve_get_location_plans(self, info, location):
        today = datetime.datetime.today()
        return (
            Plan.objects.select_related("location", "crop")
                .filter(location_id=location)
                .filter(plan_year__gte=today.year, deleted_at=None)
        )

    @login_required
    def resolve_get_farm_plans(self, info, farm_id):
        today = datetime.datetime.today()
        farm_plans = (
            Plan.objects.select_related("location", "crop")
                .filter(
                plan_year__gte=today.year,
                deleted_at=None,
                location__farm__member_farms__user_id=info.context.user.id,
            ).filter(location__organization__id=farm_id)
        )

        if farm_plans is None:
            raise (
                GraphQLError(
                    f"No user farms have plans for the current or future years."
                )
            )

        else:

            return farm_plans

    @login_required
    def resolve_get_farm_plan(self, info, farm_id, plan_id):
        return Plan.objects.select_related("location", "crop").get(deleted_at=None, location__organization__id=farm_id, id=plan_id)

    @login_required
    def resolve_get_plan_activity_log(self, info, plan_id):
        min_date = datetime.datetime.today() - datetime.timedelta(days=90)
        return TaskHistory.objects.select_related("task_id", "task_id__task_activity").filter(task_id__task_plan_id=plan_id, modified_at__gte=min_date)


schema = graphene.Schema(query=Query)
