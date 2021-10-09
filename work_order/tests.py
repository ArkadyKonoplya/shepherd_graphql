import datetime
import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from activity.models import Activity
from crop.models import Crop
from equipment.models import Equipment, EquipmentModel, EquipmentType, EquipmentMake
from farm.models import Farm, OrganizationType, OrganizationRole, FarmUsers
from field.models import Location, LocationType
from plan.models import Plan
from task.models import Task, TaskStatus
from work_order.models import WorkOrderStatus, WorkOrder


from shepherd.schema import schema


class WorkOrderTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):

        user_id = uuid.uuid4()

        self.user = get_user_model().objects.create(
            username='work_order_test',
            id=user_id,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.client.authenticate(self.user)

        self.crop1 = mixer.blend(
            Crop,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_status1 = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="available",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_status2 = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="accepted",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_status3 = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="declined",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_status4 = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="assigned",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_status5 = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="deleted",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.work_order_status1 = mixer.blend(
            WorkOrderStatus,
            id=uuid.uuid4(),
            name="open",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.work_order_status2 = mixer.blend(
            WorkOrderStatus,
            id=uuid.uuid4(),
            name="completed",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.work_order_status3 = mixer.blend(
            WorkOrderStatus,
            id=uuid.uuid4(),
            name="in progress",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.farm_type = mixer.blend(
            OrganizationType,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.farm1 = mixer.blend(
            Farm,
            id=uuid.uuid4(),
            type=self.farm_type,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.role1 = mixer.blend(
            OrganizationRole,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.farm_user1 = mixer.blend(
            FarmUsers,
            id=uuid.uuid4(),
            farm=self.farm1,
            user=self.user,
            role=self.role1,
            default_farm=True,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.activity1 = mixer.blend(
            Activity,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.activity2 = mixer.blend(
            Activity,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.location_type1 = mixer.blend(
            LocationType,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.location1 = mixer.blend(
            Location,
            id=uuid.uuid4(),
            type=self.location_type1,
            geo_center="0101000020E61000002959F38876545940C2823463D15E4140",
            drawn_area="0103000020E61000000100000005000000C8ED160062545940796C650B905E4140744E6B52895459401BA686434D5E4140C67E95FB9C5459406CD484D79F5E4140938BE9C15C545940BD793849D95E4140C8ED160062545940796C650B905E4140",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        today = datetime.datetime.now()

        self.plan = mixer.blend(
            Plan,
            id=uuid.uuid4(),
            plan_year=today.year,
            location=self.location1,
            crop=self.crop1,
            planner=self.user,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )


        self.equipment_type1 = mixer.blend(
            EquipmentType,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.equipment_make1 = mixer.blend(
            EquipmentMake,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.equipment_model1 = mixer.blend(
            EquipmentModel,
            id=uuid.uuid4(),
            equipment_type=self.equipment_type1,
            make=self.equipment_make1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.equipment1 = mixer.blend(
            Equipment,
            id=uuid.uuid4(),
            make_model=self.equipment_model1,
            name="Test Farm Equipment 1",
            farm=self.farm1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
            equipment_type=None,
        )

        self.work_order = mixer.blend(
            WorkOrder,
            id=uuid.uuid4(),
            activity=self.activity1,
            start_date=today,
            end_date=today,
            available_date=today,
            farm=self.farm1,
            work_order_status=self.work_order_status1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def test_create_work_order_with_name(self):
        create_work_order_mutation = """
            mutation getVars($activity: String!, $start_date: DateTime!, $end_date: DateTime!, $work_order_name: String!, $available_date: DateTime!)
            {
                addWorkOrder(activity: $activity, startDate: $start_date, endDate: $end_date, workOrderName: $work_order_name, availableDate: $available_date)
                {
                    workOrder
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "activity": str(self.activity1.id),
            "start_date": datetime.datetime.today(),
            "end_date": datetime.datetime.today(),
            "work_order_name": "Test Work Order",
            "available_date": datetime.datetime.today(),
        }

        response = self.client.execute(create_work_order_mutation, variables)
        content = response.data

        assert len(content["addWorkOrder"]["workOrder"]) == 1

    def test_create_work_order_with_generated_name(self):
        create_work_order_mutation = """
                    mutation getVars($activity: String!, $start_date: DateTime!, $end_date: DateTime!, $available_date: DateTime!)
                    {
                        addWorkOrder(activity: $activity, startDate: $start_date, endDate: $end_date, availableDate: $available_date)
                        {
                            workOrder
                            {
                                workOrderName
                            }
                        }
                    }
                """

        variables = {
            "activity": str(self.activity1.id),
            "start_date": datetime.datetime.today(),
            "end_date": datetime.datetime.today(),
            "available_date": datetime.datetime.today(),
        }

        response = self.client.execute(create_work_order_mutation, variables)
        content = response.data

        assert content["addWorkOrder"]["workOrder"]["workOrderName"] == f"{self.activity1.name} in TBD"

    def test_work_order_task_generation_send_all_workers(self):
        wo_task_generation_mutation = """
            mutation getVars($work_order: String!, $equipment: [EquipmentInput], $task_plans: [PlanInput], $task_assignee: [TaskAssigneeInput], $send_all_workers: Boolean!)
            {
                generateWorkOrderTasks(workOrderId: $work_order, equipment: $equipment, taskPlans: $task_plans, taskAssignee: $task_assignee, sendAllWorkers: $send_all_workers)
                {
                    workOrder
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "work_order": str(self.work_order.id),
            "equipment": [
                {"equipment": str(self.equipment1.id)}
            ],
            "task_plans": [
                {"plan": str(self.plan.id)}
            ],
            "task_assignee": [
                {"assignee": str(self.user.id)}
            ],
            "send_all_workers": True,
        }

        response = self.client.execute(wo_task_generation_mutation, variables)
        content = response.data

        assert len(content["generateWorkOrderTasks"]["workOrder"]) == 1

    def test_work_order_task_generation_send_all_workers_no_assignees(self):
        wo_task_generation_mutation = """
            mutation getVars($work_order: String!, $equipment: [EquipmentInput], $task_plans: [PlanInput], $send_all_workers: Boolean!)
            {
                generateWorkOrderTasks(workOrderId: $work_order, equipment: $equipment, taskPlans: $task_plans, sendAllWorkers: $send_all_workers)
                {
                    workOrder
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "work_order": str(self.work_order.id),
            "equipment": [
                {"equipment": str(self.equipment1.id)}
            ],
            "task_plans": [
                {"plan": str(self.plan.id)}
            ],
            "send_all_workers": True,
        }

        response = self.client.execute(wo_task_generation_mutation, variables)
        errors = response.errors

        assert "No workers were selected." in errors[0].message

    def test_work_order_task_generation_not_send_all_workers(self):
        wo_task_generation_mutation = """
            mutation getVars($work_order: String!, $equipment: [EquipmentInput], $task_plans: [PlanInput], $task_assignee: [TaskAssigneeInput], $send_all_workers: Boolean!)
            {
                generateWorkOrderTasks(workOrderId: $work_order, equipment: $equipment, taskPlans: $task_plans, taskAssignee: $task_assignee, sendAllWorkers: $send_all_workers)
                {
                    workOrder
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "work_order": str(self.work_order.id),
            "equipment": [
                {"equipment": str(self.equipment1.id)}
            ],
            "task_plans": [
                {"plan": str(self.plan.id)}
            ],
            "task_assignee": [
                {"assignee": str(self.user.id)}
            ],
            "send_all_workers": False,
        }

        response = self.client.execute(wo_task_generation_mutation, variables)
        content = response.data

        assert len(content["generateWorkOrderTasks"]["workOrder"]) == 1

    def test_work_order_update(self):
        wo_update_mutation = """
            mutation getVars($work_order_id: String!, $activity: String!, $start_date: DateTime!, $end_date: DateTime!)
            {
                updateWorkOrder(workOrderId: $work_order_id, activity: $activity, startDate: $start_date, endDate: $end_date)
                {
                    workOrder
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "work_order_id": str(self.work_order.id),
            "activity": str(self.activity2.id),
            "start_date": datetime.datetime.today(),
            "end_date": datetime.datetime.today(),
        }

        response = self.client.execute(wo_update_mutation, variables)
        content = response.data

        assert len(content["updateWorkOrder"]["workOrder"]) == 1

    def test_work_order_status_update(self):
        update_work_order_status_mutation = """
            mutation getVars($work_order_id: String!)
            {
                updateWorkOrderStatus(workOrderId: $work_order_id)
                {
                    workOrder
                    {
                        id
                    }
                }
            } 
        """

        variables = {
            "work_order_id": str(self.work_order.id),
        }

        response = self.client.execute(update_work_order_status_mutation, variables)
        content = response.data

        assert len(content["updateWorkOrderStatus"]["workOrder"]) == 1

    def test_get_farm_open_work_orders(self):
        get_farm_open_work_orders = """
            query getVars($farm: String!)
            {
                getFarmOpenWorkOrders(farmId: $farm)
                {
                    id
                    workOrderName
                }
            }
        """

        variables = {
            "farm": str(self.farm1.id),
        }

        response = self.client.execute(get_farm_open_work_orders, variables)
        content = response.data

        assert len(content["getFarmOpenWorkOrders"]) == 1
