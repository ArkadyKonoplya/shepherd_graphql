import datetime

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from django.db.models import Q
from graphql import GraphQLError

from task.models import (
    Message,
    Task,
    TaskStatus,
    TaskDetails,
    TaskEquipment,
    TaskHistory,
)


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = (
            "id",
            "recipient",
            "farm",
            "sender",
            "task",
            "message_year",
            "is_archived",
            "is_deleted",
            "message",
            "message_location",
        )


class TaskDetailsType(DjangoObjectType):
    class Meta:
        model = TaskDetails
        fields = ("id", "activity_detail", "detail_value", "detail_set_num")


class TaskHistoryType(DjangoObjectType):
    class Meta:
        model = TaskHistory
        fields = (
            "id",
            "update_user",
            "assigned_user",
            "status_date_change",
            "status_change_location",
            "task_status",
            "task_id",
        )

    def resolve_status_date_change(value_obj, info):
        return value_obj.status_date_change.replace(microsecond=0)


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = (
            "id",
            "task_creator",
            "task_activity",
            "task_start_date",
            "task_end_date",
            "task_status",
            "task_notes",
            "task_assignee",
            "equipment",
            "task_plan",
            "task_details",
            "history",
        )

    task_details = graphene.List(TaskDetailsType)
    history = graphene.List(TaskHistoryType)

    def resolve_task_details(value_obj, info):
        return value_obj.detail_tasks.all()

    def resolve_history(value_obj, info):
        return value_obj.task_history.all()


class TaskAssigneeInput(graphene.InputObjectType):

    assignee = graphene.String()


class TaskDetailsInput(graphene.InputObjectType):

    activity_detail = graphene.String()
    detail_value = graphene.String()


class TaskDetailsSetInput(graphene.InputObjectType):

    set_num = graphene.Int()
    task_details = graphene.List(TaskDetailsInput)


class TaskEquipmentType(DjangoObjectType):
    class Meta:
        model = TaskEquipment
        fields = ("id", "task", "equipment")


class TaskEquipmentInput(graphene.InputObjectType):

    equipment = graphene.String()


class TaskStatusType(DjangoObjectType):
    class Meta:
        model = TaskStatus
        fields = ("id", "name")


class TaskCount(graphene.ObjectType):
    count_type = graphene.String()
    count = graphene.Int()


class Query(graphene.ObjectType):
    get_messages = graphene.List(MessageType, recipient=graphene.String(required=True))
    get_farm_tasks = graphene.List(TaskType, farm_id=graphene.String(required=True))
    get_inbox_tasks = graphene.List(TaskType, farm_id=graphene.String(required=True))
    get_available_tasks = graphene.List(
        TaskType, farm_id=graphene.String(required=True)
    )
    get_worker_tasks = graphene.List(TaskType)
    get_worker_activity_log = graphene.List(
        TaskHistoryType, worker_id=graphene.String(required=True))
    get_equipment_activity_log = graphene.List(TaskHistoryType, equipment_id=graphene.String(required=True))
    get_farm_activity_log = graphene.List(TaskHistoryType, farm_id=graphene.String(required=True))

    get_task = graphene.List(TaskType, task_id=graphene.String(required=True))
    get_task_details = graphene.List(
        TaskDetailsType, task_id=graphene.String(required=True)
    )
    get_today_tasks = graphene.List(TaskType, farm_id=graphene.String(required=True))
    get_all_task_status = graphene.List(TaskStatusType)
    get_behind_schedule_tasks = graphene.List(
        TaskType, farm_id=graphene.String(required=True)
    )
    get_in_progress_tasks = graphene.List(
        TaskType, farm_id=graphene.String(required=True)
    )
    get_completed_tasks = graphene.List(TaskType, farm_id=graphene.String(required=True))

    get_farm_task_counts = graphene.List(TaskCount, farm_id=graphene.String(required=True))

    @login_required
    def resolve_get_messages(self, info, recipient):
        return (
            Message.objects.prefetch_related("sender", "task")
            .filter(recipient__username=recipient)
            .filter(is_archived=False)
            .filter(is_deleted=False, deleted_at=None)
        )

    @login_required
    def resolve_get_farm_tasks(self, info, farm_id):
        return (
            Task.objects.select_related("task_plan", "task_activity", "task_status")
            .filter(
                task_plan__location__location_farms__farm=farm_id,
                deleted_at=None,
                task_plan__location__location_farms__farm__member_farms__user_id=info.context.user.id,
            )
            .exclude(task_status__name="deleted")
        )

    @login_required
    def resolve_get_inbox_tasks(self, info, farm_id):

        farm_tasks = (
            Task.objects.select_related("task_plan", "task_activity", "task_status")
            .filter(Q(task_assignee_id=info.context.user.id) | Q(task_assignee_id=None))
            .filter(task_plan__location__location_farms__farm=farm_id)
            .filter(task_status__name__in=("available", "assigned", "accepted"))
            .filter(is_draft=False, deleted_at=None)
        )

        return farm_tasks

    @login_required
    def resolve_get_today_tasks(self, info, farm_id):
        return (
            Task.objects.select_related("task_plan", "task_activity", "task_status")
            .filter(task_assignee=info.context.user.id)
            .filter(task_plan__location__location_farms__farm=farm_id)
            .filter(task_status__name="accepted")
            .filter(is_draft=False, deleted_at=None)
        )

    @login_required
    def resolve_get_plan_tasks(self, info, plan_id):
        return Task.objects.filter(task_plan__id=plan_id, deleted_at=None).exclude(
            task_status__name="deleted"
        )

    @login_required
    def resolve_get_worker_tasks(self, info):
        return (
            Task.objects.select_related("task_plan", "task_activity", "task_status")
            .filter(task_assignee=info.context.user.id)
            .filter(task_status__name__in=("assigned", "accepted"))
            .filter(is_draft=False, deleted_at=None)
        )

    @login_required
    def resolve_get_available_tasks(self, info, farm_id):
        return (
            Task.objects.select_related("task_plan", "task_activity", "task_status")
            .filter(task_status__name="available")
            .filter(is_draft=False)
            .filter(
                task_plan__location__location_farms__farm=farm_id,
                deleted_at=None,
                task_plan__location__location_farms__farm__member_farms__user_id=info.context.user.id,
            )
        )

    @login_required
    def resolve_get_task(self, info, task_id):
        return Task.objects.prefetch_related("equipment__task_set__equipment").filter(
            id=task_id,
            deleted_at=None,
            task_plan__location__location_farms__farm__member_farms__user_id=info.context.user.id,
        )

    @login_required
    def resolve_get_task_details(self, info, task_id):
        return TaskDetails.objects.prefetch_related("activity_detail").filter(
            task_id=task_id,
            deleted_at=None,
            task__task_plan__location__location_farms__farm__member_farms__user_id=info.context.user.id,
        )

    @login_required
    def resolve_get_all_task_status(self, info):
        return TaskStatus.objects.filter(deleted_at=None)

    @login_required
    def resolve_get_worker_activity_log(self, info, worker_id):
        today = datetime.datetime.today()
        min_date = today - datetime.timedelta(days=90)
        return TaskHistory.objects.filter(
            Q(update_user_id=worker_id) | Q(assigned_user=worker_id), status_date_change__gte=min_date
        )

    @login_required
    def resolve_get_behind_schedule_tasks(self, info, farm_id):
        today = datetime.datetime.today()

        return Task.objects.filter(
            task_status__name__in=("accepted", "assigned", "available", "declined"),
            task_end_date__lt=today,
        )

    @login_required
    def resolve_get_in_progress_tasks(self, info, farm_id):
        today = datetime.datetime.today()

        return Task.objects.filter(
            task_status__name__in=("accepted", "assigned", "available", "declined"),
            task_end_date__gte=today,
        )

    @login_required
    def resolve_get_completed_tasks(self, info, farm_id):
        min_date = datetime.datetime.today() - datetime.timedelta(days=90)

        return Task.objects.filter(
            task_status__name="completed", modified_at__gte=min_date
        )

    @login_required
    def resolve_get_farm_task_counts(self, info, farm_id):
        today = datetime.datetime.today()
        min_date = today - datetime.timedelta(days=90)
        task_list = Task.objects.filter(deleted_at=None, modified_at__gte=min_date, task_plan__location__farm=farm_id)

        # Get count of behind schedule tasks

        behind_count = task_list.filter(
            task_status__name__in=("accepted", "assigned", "available", "declined"),
            task_end_date__lt=today,
        ).count()

        behind_schedule = TaskCount(count_type="behind_schedule", count=behind_count)

        # Get count of in progress tasks

        in_progress_count = task_list.filter(
            task_status__name__in=("accepted", "assigned", "available", "declined"),
            task_end_date__gte=today,
        ).count()

        in_progress = TaskCount(count_type="in_progress", count=in_progress_count)

        # Get count of completed tasks

        completed_count = task_list.filter(task_status__name="completed").count()

        completed = TaskCount(count_type="completed", count=completed_count)

        return [behind_schedule, in_progress, completed]

    @login_required
    def resolve_get_equipment_activity_log(self, info, equipment_id):
        today = datetime.datetime.today()
        min_date = today - datetime.timedelta(days=90)

        return TaskHistory.objects.filter(task_id__equipment_task__equipment_id=equipment_id, status_date_change__gte=min_date)

    @login_required
    def resolve_get_farm_activity_log(self, info, farm_id):
        today = datetime.datetime.today()
        min_date = today - datetime.timedelta(days=90)

        return TaskHistory.objects.filter(task_id__task_assignee__farm_members__farm_id=farm_id, status_date_change__gte=min_date)


schema = graphene.Schema(query=Query)
