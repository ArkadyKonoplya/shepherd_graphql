import datetime
import os

import graphene
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
from fcm_django.models import FCMDevice

from crop.models import Crop
from farm.models import FarmUsers
from field.models import Location
from plan.models import Plan
from plan.schema import PlanType
from task.models import Task, TaskDetails, TaskEquipment, TaskStatus, TaskHistory
from task.schema import (
    TaskType,
    TaskDetailsSetInput,
    TaskEquipmentInput,
)
from user.models import ShepherdUser


class TaskCreateMutation(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        task_creator = graphene.String(required=True)
        task_activity = graphene.String(required=True)
        task_start_date = graphene.DateTime(required=True)
        task_end_date = graphene.DateTime(required=True)
        task_status = graphene.String()
        task_notes = graphene.String()
        task_plan = graphene.String(required=True)
        task_details = graphene.List(TaskDetailsSetInput)
        task_equipment = graphene.List(TaskEquipmentInput)
        task_assignee = graphene.String()
        update_location = graphene.String()

    @login_required
    def mutate(
        self,
        info,
        task_creator,
        task_activity,
        task_start_date,
        task_end_date,
        task_plan,
        **kwargs,
    ):

        available_status = TaskStatus.objects.get(name="available")

        task_assignee = kwargs.get("task_assignee", None)
        task_status = kwargs.get("task_status", None)
        task_notes = kwargs.get("task_notes", None)
        task_details = kwargs.get("task_details", None)
        task_equipment = kwargs.get("task_equipment", None)
        update_location = kwargs.get("update_location", None)

        task = Task()
        task.task_creator_id = task_creator
        task.task_activity_id = task_activity
        task.task_start_date = task_start_date
        task.task_end_date = task_end_date
        if task_status is not None:
            task.task_status_id = task_status
        else:
            task.task_status_id = available_status.id
        if task_notes is not None:
            task.task_notes = task_notes
        if task_assignee is not None and task_assignee != "":
            task.task_assignee_id = task_assignee
        task.task_plan_id = task_plan
        task.created_by = info.context.user.id
        task.modified_by = info.context.user.id

        task.save()

        update_task_history(info=info, task=task, update_location=update_location)

        if task_details is not None:
            for num in task_details:
                for detail in num.task_details:
                    task_detail = TaskDetails()
                    task_detail.detail_set_num = num.set_num
                    task_detail.task = task
                    task_detail.activity_detail_id = detail["activity_detail"]
                    task_detail.detail_value = detail["detail_value"]
                    task_detail.created_by = info.context.user.id
                    task_detail.modified_by = info.context.user.id
                    task_detail.save()

        if task_equipment is not None:
            for equipment in task_equipment:
                task_equipment = TaskEquipment()
                task_equipment.task = task
                task_equipment.equipment_id = equipment["equipment"]
                task_equipment.created_by = info.context.user.id
                task_equipment.modified_by = info.context.user.id
                task_equipment.save()

        create_notification(action="create", task=task, info=info)

        return TaskCreateMutation(task=task)


class TaskStatusUpdateMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        task = graphene.String(required=True)
        status = graphene.String(required=True)
        task_notes = graphene.String()
        assignee = graphene.String()
        update_location = graphene.String()
        reset_notes = graphene.Boolean()

    @login_required
    def mutate(self, info, task, status, **kwargs):

        notes = kwargs.get("task_notes", None)
        assignee = kwargs.get("assignee", None)
        update_location = kwargs.get("update_location", None)
        reset_notes = kwargs.get("reset_notes", None)

        accepted_status = TaskStatus.objects.get(name="accepted")
        deleted_status = TaskStatus.objects.get(name="deleted")
        no_assignee_status = TaskStatus.objects.filter(
            name__in=("available", "declined")
        )
        task = Task.objects.get(pk=task)

        if assignee is not None and assignee != "":
            assignee = ShepherdUser.objects.get(id=assignee)

        # Task can't be accepted by more than one worker.  This just ensures that.

        if status == str(accepted_status.id) and task.task_assignee is not None and task.task_assignee.id != assignee.id:
            raise GraphQLError(
                f"Task is already assigned to {task.task_assignee.first_name} {task.task_assignee.last_name}."
            )

        if status == str(deleted_status.id):
            task.deleted_at = datetime.datetime.now()
            task.deleted_by = info.context.user.id

        # Certain statuses should remove assignee because the task shouldn't be assigned.
        if status in no_assignee_status:
            task.task_assignee = None

        # assignee should only be assigned on statuses that allow it.
        if assignee is not None and assignee != "" and status not in no_assignee_status:
            task.task_assignee = assignee

        task.task_status_id = status

        if task.task_notes is not None and notes is not None:
            task.task_notes = task.task_notes + notes
        elif notes is not None:
            task.task_notes = notes

        if reset_notes:
            task.task_notes = None

        task.save()

        update_task_history(info=info, task=task, update_location=update_location)
        create_notification(action="update", task=task, info=info)

        return TaskStatusUpdateMutation(success=True)


class TaskUpdateMutation(graphene.Mutation):
    class Arguments:
        task_creator = graphene.String(required=True)
        task_activity = graphene.String(required=True)
        task_start_date = graphene.DateTime(required=True)
        task_end_date = graphene.DateTime(required=True)
        task_status = graphene.String()
        task_notes = graphene.String()
        id = graphene.String(required=True)
        task_plan = graphene.String(required=True)
        update_location = graphene.String()
        task_details = graphene.List(TaskDetailsSetInput)
        task_equipment = graphene.List(TaskEquipmentInput)
        task_assignee = graphene.String()
        reset_notes = graphene.Boolean()

    task = graphene.Field(TaskType)

    @login_required
    def mutate(
        self,
        info,
        task_creator,
        task_activity,
        task_start_date,
        task_end_date,
        id,
        task_plan,
        **kwargs,
    ):
        task_assignee = kwargs.get("task_assignee", None)
        task_status = kwargs.get("task_status", None)
        task_notes = kwargs.get("task_notes", None)
        task_details = kwargs.get("task_details", None)
        task_equipment = kwargs.get("task_equipment", None)
        update_location = kwargs.get("update_location", None)
        reset_notes = kwargs.get("reset_notes", None)

        deleted_status = TaskStatus.objects.get(name="deleted")

        task = Task.objects.get(id=id)

        update_task_history(info=info, task=task, update_location=update_location)

        task.task_creator_id = task_creator
        task.task_activity_id = task_activity
        task.task_start_date = task_start_date
        task.task_end_date = task_end_date
        if task_status:
            task.task_status_id = task_status

            if task_status == str(deleted_status.id):
                task.deleted_at = datetime.datetime.now()
                task.deleted_by = info.context.user.id

        if task_notes is not None:
            task.task_notes = task_notes

        # if resetNotes is set to True, wipe out the notes.
        if reset_notes:
            task.task_notes = None

        if task_assignee is not None and task_assignee != "":
            task.task_assignee_id = task_assignee
        task.task_plan_id = task_plan
        task.modified_by = info.context.user.id

        task.save()

        if task_details:
            for num in task_details:
                for detail in num.task_details:
                    try:
                        task_detail = TaskDetails.objects.get(
                            task=task,
                            activity_detail_id=detail["activity_detail"],
                            detail_set_num=num.set_num,
                        )
                    except TaskDetails.DoesNotExist:
                        task_detail = None

                    if task_detail:
                        task_detail.detail_value = detail["detail_value"]
                        task_detail.modified_by = info.context.user.id
                        task_detail.modified_at = datetime.now()
                        task_detail.save()

                    else:
                        task_detail = TaskDetails()
                        task_detail.detail_set_num = num.set_num
                        task_detail.task = task
                        task_detail.activity_detail_id = detail["activity_detail"]
                        task_detail.detail_value = detail["detail_value"]
                        task_detail.created_by = info.context.user.id
                        task_detail.modified_by = info.context.user.id
                        task_detail.save()

        if task_equipment:
            for equipment in task_equipment:
                task_equipment = TaskEquipment()
                task_equipment.task = task
                task_equipment.equipment_id = equipment["equipment"]
                task_equipment.created_by = info.context.user.id
                task_equipment.modified_by = info.context.user.id
                task_equipment.save()

        create_notification(action="update", task=task, info=info)

        return TaskUpdateMutation(task=task)


def update_task_history(info, task, update_location=None):
    """
    Update the task_history table when the task is being updated.
    :param info:
    :param task:
    :param update_location:
    :return:
    """

    task_history = TaskHistory(
        update_user_id=info.context.user.id,
        status_date_change=datetime.datetime.now(datetime.timezone.utc),
        task_status=task.task_status,
        created_by=info.context.user.id,
        modified_by=info.context.user.id,
        task_id=task,
    )
    if task.task_assignee is not None:

        task_history.assigned_user = task.task_assignee

    # Made optional if user declines to let us know their location.
    if update_location is not None:
        task_history.status_change_location = update_location

    task_history.save()


def create_notification(action, task, info):
    """
    Create a notification and determine who gets the notification.
    :param action: what action is being taken on the task
    :param task: The task sqlalchemy object
    :param info: session info object
    :return:
    """
    valid_actions = ['create', 'update']
    special_status = ['accepted', 'declined', 'completed']
    user_first_name = info.context.user.first_name
    user_first_name = user_first_name.capitalize()
    user_last_name = info.context.user.last_name
    user_last_name = user_last_name.capitalize()
    user_name = f"{user_first_name} {user_last_name}"

    if action not in valid_actions:
        raise GraphQLError(f"Invalid action type.  Valid actions are: {valid_actions}.")

    if task.task_creator == info.context.user and task.task_assignee is not None:
        recipient = task.task_assignee.id
    elif task.task_assignee == info.context.user:
        recipient = task.task_creator.id
    else:
        recipient = None

    if action == 'create':
        if task.task_creator != task.task_assignee and task.task_assignee is not None and recipient is not None:
            # Send assignee or creator notification if they aren't the same person.
            devices = FCMDevice.objects.filter(user_id=recipient, active=True).distinct('device_id', 'registration_id')
            title = "New Task Assigned"
            body = f"You have been assigned a {task.task_activity.name.lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} by {user_name}."

            send_notification(devices=devices, title=title, body=body)
        elif task.task_assignee is None:
            # If no assignee, send to everyone but the creator on the given farm.
            farm_users = get_farm_users(task)
            devices = FCMDevice.objects.filter(user_id__in=farm_users, active=True).distinct('device_id', 'registration_id')
            title = "New Available Task"
            body = f"A new {task.task_activity.name.lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} has been made available by {user_name}."

            send_notification(devices=devices, title=title, body=body)

    elif action == 'update':
        if task.task_creator != task.task_assignee and task.task_assignee is not None:
            # Send assignee/creator notification if they aren't the same person.
            devices = FCMDevice.objects.filter(user_id=recipient, active=True).distinct('device_id', 'registration_id')

            if task.task_status.name in special_status:
                notification_status = task.task_status.name
            else:
                notification_status = 'updated'

            title = f"A Task Has Been {notification_status.capitalize()}"
            body = f"The {task.task_activity.name.lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} has been {notification_status} by {user_name}."

            send_notification(devices=devices, title=title, body=body)

            if task.task_status.name == 'declined':
                # When task is declined, the farm users need to also be notified.
                farm_users = get_farm_users(task)
                devices = FCMDevice.objects.filter(user_id__in=farm_users, active=True).distinct('device_id', 'registration_id')
                title = "Declined Task Available"
                body = f"The {task.task_activity.name.lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} is now available."

        elif task.task_assignee is None:
            # If no assignee, send to everyone but the creator on the given farm.
            farm_users = get_farm_users(task)
            devices = FCMDevice.objects.filter(user_id__in=farm_users, active=True).distinct('device_id', 'registration_id')
            title = "An Available Task Has Been Updated"
            body = f"The {task.task_activity_name.lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} has been updated by {user_name}."

            send_notification(devices=devices, title=title, body=body)


def get_farm_users(task):
    """
    For the given task, get the farm's users, except the creator.
    :param task:
    :return:
    """

    return ShepherdUser.objects.filter(farm_members__farm__location__plan=task.task_plan_id).exclude(id=task.task_creator_id)


def send_notification(devices, title, body):
    """
    Basic send message
    :param devices: query result object of firebase devices to send notifications to
    :param title: String title of the notification
    :param body: String body of the notification
    :return:
    """
    devices.send_message(
        title=title,
        body=body,
        sound=True,
        api_key=os.getenv("fcm_server_key")
    )


class Mutation(graphene.ObjectType):
    add_task = TaskCreateMutation.Field()
    update_task = TaskUpdateMutation.Field()
    update_task_status = TaskStatusUpdateMutation.Field()
