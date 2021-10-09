import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from django.db.models import Count

from equipment.schema import EquipmentInput
from plan.schema import PlanInput
from task.schema import TaskAssigneeInput
from work_order.schema import WorkOrderType

from task.mutation import create_notification

from activity.models import Activity
from equipment.models import Equipment
from farm.models import Farm
from plan.models import Plan
from task.models import Task, TaskStatus, TaskEquipment
from work_order.models import WorkOrder, WorkOrderStatus, WorkOrderTaskRel, WorkOrderEquipmentRel


class WorkOrderCreateMutation(graphene.Mutation):
    """
    mutation used to create base work orders.
    """

    work_order = graphene.Field(WorkOrderType)

    class Arguments:
        activity = graphene.String(required=True)
        start_date = graphene.DateTime(required=True)
        end_date = graphene.DateTime(required=True)
        work_order_name = graphene.String()
        available_date = graphene.DateTime()

    @login_required
    def mutate(self, info, activity, start_date, end_date, **kwargs):

        work_order_name = kwargs.get("work_order_name", None)
        available_date = kwargs.get("available_date", None)

        activity = Activity.objects.get(id=activity)
        available_status = WorkOrderStatus.objects.get(name='open')
        farm = Farm.objects.get(member_farms__default_farm=True, member_farms__user_id=info.context.user.id)

        work_order = WorkOrder()

        if work_order_name is not None:
            work_order.work_order_name = work_order_name
        else:
            work_order.work_order_name = f"{activity.name} in TBD"

        if available_date is not None:
            work_order.available_date = available_date

        work_order.activity = activity
        work_order.start_date = start_date
        work_order.end_date = end_date
        work_order.farm = farm
        work_order.work_order_status = available_status
        work_order.created_by = info.context.user.id
        work_order.modified_by = info.context.user.id

        work_order.save()

        return WorkOrderCreateMutation(work_order=work_order)


class WorkOrderUpdateMutation(graphene.Mutation):
    """
    mutation used to update base work orders.
    """
    work_order = graphene.Field(WorkOrderType)

    class Arguments:
        activity = graphene.String(required=True)
        start_date = graphene.DateTime(required=True)
        end_date = graphene.DateTime(required=True)
        work_order_name = graphene.String()
        available_date = graphene.DateTime()
        work_order_id = graphene.String(required=True)

    @login_required
    def mutate(self, info, activity, start_date, end_date, work_order_id, **kwargs):

        work_order_name = kwargs.get("work_order_name", None)
        available_date = kwargs.get("available_date", None)

        #deleted_status = WorkOrderStatus.objects.get(name='deleted')

        work_order = WorkOrder.objects.get(id=work_order_id)

        if work_order_name is not None:
            work_order.work_order_name = work_order_name
        else:

            if work_order.work_order_name is None:
                work_order.work_order_name = f"{work_order.activity.name} in TBD"

        if available_date is not None:
            work_order.available_date = available_date

        work_order.activity_id = activity
        work_order.start_date = start_date
        work_order.end_date = end_date
        work_order.modified_by = info.context.user.id

        work_order.save()

        return WorkOrderUpdateMutation(work_order=work_order)


class WorkOrderTaskGenerationMutation(graphene.Mutation):
    """
    Once work order is created, need to know details for generating tasks.
    """

    work_order = graphene.Field(WorkOrderType)

    class Arguments:
        work_order_id = graphene.String(required=True)
        equipment = graphene.List(EquipmentInput)
        task_plans = graphene.List(PlanInput)
        task_assignee = graphene.List(TaskAssigneeInput)
        send_all_workers = graphene.Boolean()

    @login_required
    def mutate(self, info, work_order_id, task_plans, **kwargs):

        send_all_workers = kwargs.get('send_all_workers', False)
        task_assignee = kwargs.get('task_assignee', None)
        equipment = kwargs.get("equipment", None)

        work_order = WorkOrder.objects.get(id=work_order_id)

        if send_all_workers is True:
            # If no workers are selected, then tasks generated are sent to all farm users as available
            # If workers are selected, then tasks generated are sent just to those workers as available.

            if task_assignee is None:

                raise GraphQLError("No workers were selected.")

            else:
                assigned_status = TaskStatus.objects.get(name="assigned")

                for plan in task_plans:
                    for assignee in task_assignee:
                        new_task = Task(
                            task_creator=info.context.user,
                            task_status=assigned_status,
                            task_assignee_id=assignee['assignee'],
                            task_plan_id=plan['plan'],
                            task_start_date=work_order.start_date,
                            task_end_date=work_order.end_date,
                            task_available_date=work_order.available_date,
                            task_activity=work_order.activity,
                            created_by=info.context.user.id,
                            modified_by=info.context.user.id,
                        )
                        new_task.save()

                        if work_order.total_tasks is None:
                            work_order.total_tasks = 0

                        work_order.total_tasks = work_order.total_tasks + 1
                        work_order.save()

                        work_order_task = WorkOrderTaskRel(
                            work_order=work_order,
                            task=new_task,
                            created_by=info.context.user.id,
                            modified_by=info.context.user.id,
                        )
                        work_order_task.save()

                        if equipment is not None:
                            for item in equipment:
                                work_order_equipment = WorkOrderEquipmentRel(
                                    work_order=work_order,
                                    equipment_id=item['equipment'],
                                    created_by=info.context.user.id,
                                    modified_by=info.context.user.id
                                )
                                work_order_equipment.save()

                                task_equipment = TaskEquipment(
                                    task=new_task,
                                    equipment_id=item['equipment'],
                                    created_by=info.context.user.id,
                                    modified_by=info.context.user.id,
                                )
                                task_equipment.save()

                        create_notification(action="create", task=new_task, info=info)

        else:
            available_status = TaskStatus.objects.get(name="available")
            task_plans_count = len(task_plans)

            for plan in task_plans:
                new_task = Task(
                    task_creator=info.context.user,
                    task_status=available_status,
                    task_plan_id=plan['plan'],
                    task_start_date=work_order.start_date,
                    task_end_date=work_order.end_date,
                    task_available_date=work_order.available_date,
                    task_activity=work_order.activity,
                    created_by=info.context.user.id,
                    modified_by=info.context.user.id,
                )
                new_task.save()

                if work_order.total_tasks is None:
                    work_order.total_tasks = 0

                work_order.total_tasks = work_order.total_tasks + 1
                work_order.save()

                work_order_task = WorkOrderTaskRel(
                    work_order=work_order,
                    task=new_task,
                    created_by=info.context.user.id,
                    modified_by=info.context.user.id,
                )
                work_order_task.save()

                create_notification(action="create", task=new_task, info=info)

                plan = Plan.objects.get(id=plan['plan'])

                if task_plans_count == 1:
                    if work_order.work_order_name is None:
                        work_order.work_order_name = f"{work_order.activity.name} in {plan.location.name}"

            if task_plans_count > 1:
                if work_order.work_order_name is None:
                    wo_name = f"{work_order.activity.name} in {task_plans_count} Locations"

                    wo_name_count = WorkOrder.objects.filter(name=f"{work_order.activity.name} in {task_plans_count} Locations").count()

                    if wo_name_count == 0:
                        work_order.work_order_name = wo_name
                    else:
                        work_order.work_order_name = f"{wo_name} ({wo_name_count + 1})"

        return WorkOrderTaskGenerationMutation(work_order=work_order)


class WorkOrderStatusUpdateMutation(graphene.Mutation):

    work_order = graphene.Field(WorkOrderType)

    class Arguments:
        work_order_id = graphene.String(required=True)

    @login_required
    def mutate(self, info, work_order_id):
        """
        Checks the tasks associated with the work order and updates the task counts on the work order accordingly.
        :param info:
        :param work_order_id:
        :return:
        """

        work_order = WorkOrder.objects.get(id=work_order_id)

        work_order_completed_status = WorkOrderStatus.objects.get(name='completed')
        work_order_in_progress_status = WorkOrderStatus.objects.get(name="in progress")

        tasks = WorkOrderTaskRel.objects.select_related("task__task_status").filter(work_order=work_order)

        task_count_total = tasks.filter(task__task_status__name__in=("accepted", "archived", "assigned", "available", "completed", "declined")).count()

        completed_task_count = tasks.filter(task__task_status__name__in=("completed")).count()

        work_order.total_tasks = task_count_total
        work_order.tasks_completed = completed_task_count

        if task_count_total == completed_task_count:
            work_order.work_order_status = work_order_completed_status
        elif completed_task_count < task_count_total:
            work_order.work_order_status = work_order_in_progress_status

        work_order.save()

        return WorkOrderUpdateMutation(work_order=work_order)


class Mutation(graphene.ObjectType):
    add_work_order = WorkOrderCreateMutation.Field()
    update_work_order_status = WorkOrderStatusUpdateMutation.Field()
    update_work_order = WorkOrderUpdateMutation.Field()
    generate_work_order_tasks = WorkOrderTaskGenerationMutation.Field()