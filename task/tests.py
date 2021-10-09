import datetime
import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from activity.models import Activity, ActivityDetail, ActivityDetailRel, FarmTypeActivityRel
from crop.models import Crop
from equipment.models import Equipment, EquipmentModel, EquipmentType, EquipmentMake
from farm.models import (
    OrganizationType,
    Farm,
    FarmUsers,
    OrganizationLocationRel,
    OrganizationRole,
)
from plan.models import Plan
from work_order.models import WorkOrder

from field.models import Location, LocationType
from task.models import (
    Message,
    TaskHistory,
    Task,
    TaskDetails,
    TaskEquipment,
    TaskStatus,
)
from user.models import ShepherdUser

from shepherd.schema import schema


class TaskTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        datetime_format = "%Y-%m-%d %H:%M:%S"


        user_id = uuid.uuid4()
        self.user = get_user_model().objects.create(
            username="task_test",
            id=user_id,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.client.authenticate(self.user)

        self.user2 = get_user_model().objects.create(
            id=uuid.uuid4(),
            username="task_test2",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.user3 = get_user_model().objects.create(
            id=uuid.uuid4(),
            username="task_test3",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.crop1 = mixer.blend(
            Crop,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.available_status = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="available",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.accepted_status = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="accepted",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.declined_status = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="declined",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.assigned_status = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="assigned",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.deleted_status = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="deleted",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.completed_status = mixer.blend(
            TaskStatus,
            id=uuid.uuid4(),
            name="completed",
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
        self.farm2 = mixer.blend(
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
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.farm_user2 = mixer.blend(
            FarmUsers,
            id=uuid.uuid4(),
            farm=self.farm2,
            user=self.user2,
            role=self.role1,
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

        self.activity_detail1 = mixer.blend(
            ActivityDetail,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.activity_detail2 = mixer.blend(
            ActivityDetail,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.activity_detail3 = mixer.blend(
            ActivityDetail,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.detail_activity1 = mixer.blend(
            ActivityDetailRel,
            id=uuid.uuid4(),
            activity=self.activity1,
            activity_detail=self.activity_detail1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.detail_activity2 = mixer.blend(
            ActivityDetailRel,
            id=uuid.uuid4(),
            activity=self.activity1,
            activity_detail=self.activity_detail2,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.org_activity1 = mixer.blend(
            FarmTypeActivityRel,
            farm_type=self.farm1.type,
            activity_type=self.activity1,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.org_activity2 = mixer.blend(
            FarmTypeActivityRel,
            farm_type=self.farm1.type,
            activity_type=self.activity2,
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

        self.location2 = mixer.blend(
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

        self.plan2 = mixer.blend(
            Plan,
            id=uuid.uuid4(),
            plan_year=today.year,
            location=self.location2,
            crop=self.crop1,
            planner=self.user2,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.farm_location1 = mixer.blend(
            OrganizationLocationRel,
            id=uuid.uuid4(),
            farm=self.farm1,
            location=self.location1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.farm_location2 = mixer.blend(
            OrganizationLocationRel,
            id=uuid.uuid4(),
            farm=self.farm2,
            location=self.location2,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task1 = mixer.blend(
            Task,
            id=uuid.uuid4(),
            task_creator=self.user,
            task_location=self.location1,
            task_activity=self.activity1,
            task_custom_activity=None,
            task_status=self.available_status,
            task_end_date=datetime.datetime.strptime("2021-01-01 00:00:00", datetime_format),
            task_crop=self.crop1,
            task_assignee=self.user,
            task_plan=self.plan,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task2 = mixer.blend(
            Task,
            id=uuid.uuid4(),
            task_creator=self.user,
            task_location=self.location1,
            task_activity=self.activity1,
            task_custom_activity=None,
            task_status=self.available_status,
            task_crop=self.crop1,
            task_assignee=self.user,
            task_end_date=datetime.datetime.today() + datetime.timedelta(hours=1),
            task_plan=self.plan,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task3 = mixer.blend(
            Task,
            id=uuid.uuid4(),
            task_creator=self.user,
            task_location=self.location1,
            task_activity=self.activity2,
            task_custom_activity=None,
            task_status=self.assigned_status,
            task_crop=self.crop1,
            task_end_date=datetime.datetime.strptime("2400-01-01 00:00:00", datetime_format),
            task_assignee=self.user,
            task_plan=self.plan,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task4 = mixer.blend(
            Task,
            id=uuid.uuid4(),
            task_creator=self.user,
            task_location=self.location1,
            task_activity=self.activity2,
            task_custom_activity=None,
            task_status=self.accepted_status,
            task_crop=self.crop1,
            task_assignee=self.user,
            task_plan=self.plan,
            task_end_date=datetime.datetime.strptime("1989-01-01 00:00:00", datetime_format),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
            task_notes="Testing notes"
        )

        self.task5 = mixer.blend(
            Task,
            id=uuid.uuid4(),
            task_creator=self.user,
            task_location=self.location1,
            task_activity=self.activity2,
            task_custom_activity=None,
            task_status=self.deleted_status,
            task_crop=self.crop1,
            task_assignee=self.user,
            task_end_date=datetime.datetime.today() + datetime.timedelta(hours=1),
            task_plan=self.plan,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
            task_notes="Testing notes"
        )

        self.task6 = mixer.blend(
            Task,
            id=uuid.uuid4(),
            task_creator=self.user,
            task_location=self.location1,
            task_activity=self.activity1,
            task_custom_activity=None,
            task_status=self.available_status,
            task_crop=self.crop1,
            task_assignee=None,
            task_plan=self.plan,
            task_end_date=datetime.datetime.today() + datetime.timedelta(hours=1),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task7 = mixer.blend(
            Task,
            id=uuid.uuid4(),
            task_creator=self.user2,
            task_location=self.location2,
            task_activity=self.activity1,
            task_custom_activity=None,
            task_status=self.completed_status,
            task_crop=self.crop1,
            task_assignee=None,
            task_plan=self.plan2,
            task_end_date=datetime.datetime.today() + datetime.timedelta(hours=1),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.message1 = mixer.blend(
            Message,
            id=uuid.uuid4(),
            recipient=self.user,
            farm=self.farm1,
            sender=self.user2,
            task=self.task1,
            message_location="0101000020E61000002959F38876545940C2823463D15E4140",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_detail1 = mixer.blend(
            TaskDetails,
            id=uuid.uuid4(),
            activity_detail=self.activity_detail1,
            task=self.task1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.task_detail2 = mixer.blend(
            TaskDetails,
            id=uuid.uuid4(),
            activity_detail=self.activity_detail2,
            task=self.task1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.task_detail3 = mixer.blend(
            TaskDetails,
            id=uuid.uuid4(),
            activity_detail=self.activity_detail3,
            task=self.task1,
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

        self.task_equipment = mixer.blend(
            TaskEquipment,
            id=uuid.uuid4(),
            task=self.task1,
            equipment=self.equipment1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
            equipment_type=None,
        )

        self.task_history1 = mixer.blend(
            TaskHistory,
            id=uuid.uuid4(),
            status_date_change=today,
            status_change_location="0101000020E61000002959F38876545940C2823463D15E4140",
            task_id=self.task1,
            task_status=self.assigned_status,
            update_user=self.user,
            assigned_user=self.user,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_history2 = mixer.blend(
            TaskHistory,
            id=uuid.uuid4(),
            status_date_change=today,
            status_change_location="0101000020E61000002959F38876545940C2823463D15E4140",
            task_id=self.task1,
            task_status=self.accepted_status,
            update_user=self.user,
            assigned_user=self.user,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def test_get_messages(self):
        get_messages_query = """
            query messageRecipient($recipient: String!)
            {
                getMessages(recipient: $recipient)
                {
                    id
                    message
                    sender
                    {
                        firstName
                        lastName
                    }
                }
            }
        """

        variables = {"recipient": self.user.username}
        response = self.client.execute(get_messages_query, variables)
        content = response.data

        assert len(content["getMessages"]) == 1

    def test_get_inbox_tasks(self):
        get_inbox_tasks_query = """
            query taskParams($farm: String!)
            {
                getInboxTasks(farmId: $farm)
                {
                    id
                    taskDetails
                    {
                        id
                    }
                }
            }
        """

        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_inbox_tasks_query, variables)
        content = response.data

        assert len(content["getInboxTasks"]) == 5

    def test_get_farm_tasks(self):
        get_farm_tasks_query = """
            query farmParam($farm: String!)
            {
                getFarmTasks(farmId: $farm)
                {
                    id
                }
            }
        """
        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_farm_tasks_query, variables)
        content = response.data

        assert len(content["getFarmTasks"]) == 5

    def test_get_available_tasks(self):
        get_available_tasks_query = """
            query farmParam($farm: String!)
            {
                getAvailableTasks(farmId: $farm)
                {
                    id
                }
            }
        """
        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_available_tasks_query, variables)
        content = response.data

        assert len(content["getAvailableTasks"]) == 3

    def test_get_worker_tasks(self):
        get_worker_tasks_query = """
            query 
            {
                getWorkerTasks
                {
                    id
                }
            }
        """

        response = self.client.execute(get_worker_tasks_query)
        content = response.data

        assert len(content["getWorkerTasks"]) == 2

    def test_get_today_tasks(self):
        get_today_tasks_query = """
             query taskParams($farm: String!)
             {
                 getTodayTasks(farmId: $farm)
                 {
                     id
                 }
             }
         """

        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_today_tasks_query, variables)
        content = response.data

        assert len(content["getTodayTasks"]) == 1

    def test_get_task(self):
        get_task_query = """
            query taskParam($task: String!)
            {
                getTask(taskId: $task)
                {
                    id
                    
                }
            }
        """
        variables = {"task": str(self.task1.id)}

        response = self.client.execute(get_task_query, variables)
        content = response.data

        assert len(content["getTask"]) == 1

    def test_get_task_details(self):
        get_task_details_query = """
            query taskParam($task: String!)
            {
                getTaskDetails(taskId: $task)
                {
                    id
                }
            }
        """
        variables = {"task": str(self.task1.id)}

        response = self.client.execute(get_task_details_query, variables)
        content = response.data

        assert len(content["getTaskDetails"]) == 3

    def test_get_all_task_status(self):
        get_all_task_status_query = """
            query 
            {
                getAllTaskStatus
                {
                    id
                    name
                }
            }
        """
        response = self.client.execute(get_all_task_status_query)
        content = response.data

        assert len(content["getAllTaskStatus"]) == 6

    def test_create_task(self):
        create_task_query = """
            mutation getVars($creator: String!, $activity: String!, $start_date: DateTime!
                            , $end_date: DateTime!, $assignee: String!, $status: String!
                            , $notes: String!, $plan: String!, $detail: [TaskDetailsSetInput], $equipment: [TaskEquipmentInput])
            {
                addTask(taskCreator: $creator, taskActivity: $activity
                            , taskStartDate: $start_date, taskEndDate: $end_date
                            , taskStatus: $status, taskNotes: $notes, taskPlan: $plan
                            , taskDetails: $detail, taskEquipment: $equipment, taskAssignee: $assignee)
                {
                    task
                    {
                       taskActivity{
                        name
                       }
                    }
                }      

            }    
        """

        variables = {
            "creator": str(self.user.id),
            "activity": str(self.activity1.id),
            "start_date": self.task1.task_start_date,
            "end_date": self.task1.task_end_date,
            "plan": str(self.plan.id),
            "assignee": str(self.user2.id),
            "status": str(self.accepted_status.id),
            "notes": "Test notes...",
            "detail": [
                {
                    "setNum": 1,
                    "taskDetails": [
                        {
                            "activityDetail": str(self.activity_detail1.id),
                            "detailValue": "abc123",
                        },
                        {
                            "activityDetail": str(self.activity_detail2.id),
                            "detailValue": "2000",
                        },
                    ],
                }
            ],
            "equipment": [{"equipment": str(self.equipment1.id)}],
        }
        response = self.client.execute(create_task_query, variables)
        content = response.data

        assert len(content["addTask"]["task"]) == 1

    def test_create_task_no_assignee(self):
        create_task_query = """
            mutation getVars($creator: String!, $activity: String!, $start_date: DateTime!
                            , $end_date: DateTime!, $status: String!
                            , $notes: String!, $plan: String!, $detail: [TaskDetailsSetInput], $equipment: [TaskEquipmentInput])
            {
                addTask(taskCreator: $creator, taskActivity: $activity
                            , taskStartDate: $start_date, taskEndDate: $end_date
                            , taskStatus: $status, taskNotes: $notes, taskPlan: $plan
                            , taskDetails: $detail, taskEquipment: $equipment)
                {
                    task
                    {
                       taskActivity{
                        name
                       }
                    }
                }      

            }    
        """

        variables = {
            "creator": str(self.user.id),
            "activity": str(self.activity1.id),
            "start_date": self.task1.task_start_date,
            "end_date": self.task1.task_end_date,
            "plan": str(self.plan.id),
            "status": str(self.accepted_status.id),
            "notes": "Test notes...",
            "detail": [
                {
                    "setNum": 1,
                    "taskDetails": [
                        {
                            "activityDetail": str(self.activity_detail1.id),
                            "detailValue": "abc123",
                        },
                        {
                            "activityDetail": str(self.activity_detail2.id),
                            "detailValue": "2000",
                        },
                    ],
                }
            ],
            "equipment": [{"equipment": str(self.equipment1.id)}],
        }
        response = self.client.execute(create_task_query, variables)
        content = response.data

        assert len(content["addTask"]["task"]) == 1

    def test_update_task(self):
        update_task_query = """
            mutation getVars($creator: String!, $activity: String!, $start_date: DateTime!
                            , $end_date: DateTime!, $assignee: String!, $id: String!, $status: String!
                            , $notes: String!, $plan: String!, $detail: [TaskDetailsSetInput]
                            , $equipment: [TaskEquipmentInput], $location: String!)
            {
                updateTask(taskCreator: $creator, taskActivity: $activity
                            , taskStartDate: $start_date, taskEndDate: $end_date
                            , taskAssignee: $assignee, id: $id, taskStatus: $status, taskNotes: $notes, taskPlan: $plan
                            , taskDetails: $detail, taskEquipment: $equipment, updateLocation: $location)
                {
                    task
                    {
                     id
                    }
                }      

            }                

        """
        variables = {
            "creator": str(self.user.id),
            "activity": str(self.activity1.id),
            "start_date": self.task1.task_start_date,
            "end_date": self.task1.task_end_date,
            "plan": str(self.plan.id),
            "assignee": str(self.user2.id),
            "status": str(self.accepted_status.id),
            "notes": "Test notes...",
            "id": str(self.task1.id),
            "detail": [
                {
                    "setNum": 1,
                    "taskDetails": [
                        {
                            "activityDetail": str(self.activity_detail1.id),
                            "detailValue": "abc123",
                        },
                        {
                            "activityDetail": str(self.activity_detail2.id),
                            "detailValue": "2000",
                        },
                    ],
                }
            ],
            "equipment": [{"equipment": str(self.equipment1.id)}],
            "location": "POINT(-78.6207918152582 35.5963473238645)",
        }
        response = self.client.execute(update_task_query, variables)
        content = response.data

        assert len(content["updateTask"]["task"]) == 1

    def test_task_status_update_mutation(self):

        task_status_update_query = """
            mutation getVars($task: String!, $status: String!)
            {
                updateTaskStatus(task: $task, status: $status)
                {
                    success
                }
            }
        """

        variables = {"task": str(self.task3.id), "status": str(self.available_status.id)}

        response = self.client.execute(task_status_update_query, variables)
        content = response.data

        assert content["updateTaskStatus"]["success"] is True

    def test_task_status_update_already_assigned_mutation(self):

        task_status_update_query = """
            mutation getVars($task: String!, $status: String!, $assignee: String!)
            {
                updateTaskStatus(task: $task, status: $status, assignee: $assignee)
                {
                    success
                }
            }
        """

        variables = {
            "task": str(self.task3.id),
            "status": str(self.accepted_status.id),
            "assignee": str(self.user2.id),
        }

        response = self.client.execute(task_status_update_query, variables)
        errors = response.errors

        assert (
            f"Task is already assigned to {self.user.first_name} {self.user.last_name}."
            in errors[0].message
        )

    def test_task_status_update_mutation_with_notes(self):
        task_status_update_query = """
                    mutation getVars($task: String!, $status: String!, $notes: String!)
                    {
                        updateTaskStatus(task: $task, status: $status, taskNotes: $notes)
                        {
                            success
                        }
                    }
                """
        variables = {
            "task": str(self.task1.id),
            "status": str(self.available_status.id),
            "notes": "Adding a note.",
        }

        response = self.client.execute(task_status_update_query, variables)
        content = response.data

        assert content["updateTaskStatus"]["success"] is True

    def test_task_status_update_mutation_no_assignee_status(self):
        task_status_update_query = """
                    mutation getVars($task: String!, $status: String!, $assignee: String!)
                    {
                        updateTaskStatus(task: $task, status: $status, assignee: $assignee)
                        {
                            success
                        }
                    }
                """

        variables = {
            "task": str(self.task1.id),
            "status": str(self.declined_status.id),
            "assignee": str(self.user2.id),
        }

        response = self.client.execute(task_status_update_query, variables)
        content = response.data

        assert content["updateTaskStatus"]["success"] is True

    def test_task_status_update_mutation_no_assignee_status_accepted(self):
        task_status_update_query = """
                    mutation getVars($task: String!, $status: String!, $assignee: String!)
                    {
                        updateTaskStatus(task: $task, status: $status, assignee: $assignee)
                        {
                            success
                        }
                    }
                """

        variables = {
            "task": str(self.task5.id),
            "status": str(self.accepted_status.id),
            "assignee": str(self.user.id),
        }

        response = self.client.execute(task_status_update_query, variables)
        content = response.data

        assert content["updateTaskStatus"]["success"] is True

    def test_task_status_update_mutation_no_assignee_unassigned(self):
        task_status_update_query = """
                    mutation getVars($task: String!, $status: String!)
                    {
                        updateTaskStatus(task: $task, status: $status)
                        {
                            success
                        }
                    }
                """

        variables = {
            "task": str(self.task1.id),
            "status": str(self.declined_status.id),
        }

        response = self.client.execute(task_status_update_query, variables)
        content = response.data

        assert content["updateTaskStatus"]["success"] is True


    def test_update_task_reset_notes(self):
        """
        Testing that the notes field gets reset when reset_notes is true.
        :return:
        """

        task_status_update_query = """
            mutation getVars($task: String!, $status: String!, $reset_notes: Boolean)
            {
                updateTaskStatus(task: $task, status: $status, resetNotes: $reset_notes)
                {
                    success
                }
            }
        """

        variables = {"task": str(self.task3.id), "status": str(self.available_status.id), "reset_notes": True}

        response = self.client.execute(task_status_update_query, variables)
        content = response.data

        assert content["updateTaskStatus"]["success"] is True

    def test_get_worker_activity_log(self):

        worker_activity_log_query = """
            query getVars($worker: String!)
            {
                getWorkerActivityLog(workerId: $worker)
                {
                    id
                    statusDateChange
                }    
            }
        """

        variables = {
            "worker": str(self.user.id)
        }

        response = self.client.execute(worker_activity_log_query, variables)
        content = response.data

        assert len(content["getWorkerActivityLog"]) == 2

    def test_get_equipment_activity_log(self):
        equipment_activity_log_query = """
            query getVars($equipment: String!)
            {
                getEquipmentActivityLog(equipmentId: $equipment)
                {
                    id
                    statusDateChange
                }
            }
        """

        variables = {
            "equipment": str(self.equipment1.id)
        }

        response = self.client.execute(equipment_activity_log_query, variables)
        content = response.data

        assert len(content["getEquipmentActivityLog"]) == 2

    def test_get_farm_activity_log(self):
        farm_activity_log_query = """
            query getVars($farm: String!)
            {
                getFarmActivityLog(farmId: $farm)
                {
                    id
                    statusDateChange
                }
            }
        """

        variables = {
            "farm": str(self.farm1.id)
        }

        response = self.client.execute(farm_activity_log_query, variables)
        content = response.data

        print(response)

        assert len(content["getFarmActivityLog"]) == 2

    def test_get_behind_schedule_tasks(self):
        get_behind_schedule_tasks_query = """
            query getVars($farm: String!)
            {
               getBehindScheduleTasks(farmId: $farm)
               {
                    id
                    taskStartDate
                    taskEndDate
                }
            }
        """

        variables = {
            "farm": str(self.farm1.id)
        }

        response = self.client.execute(get_behind_schedule_tasks_query, variables)
        content = response.data

        assert len(content["getBehindScheduleTasks"]) == 2

    def test_get_in_progress_tasks(self):
        get_in_progress_tasks_query = """
            query getVars($farm: String!)
            {
                getInProgressTasks(farmId: $farm)
                {
                    id
                    taskStartDate
                    taskEndDate
                }
            }
        """

        variables = {
            "farm": str(self.farm1.id)
        }

        response = self.client.execute(get_in_progress_tasks_query, variables)
        content = response.data

        assert len(content["getInProgressTasks"]) == 3

    def test_get_completed_tasks(self):
        get_completed_tasks_query = """
            query getVars($farm: String!)
            {
                getCompletedTasks(farmId: $farm)
                {
                    id
                    taskStartDate
                    taskEndDate
                }
            }
        """

        variables = {
            "farm": str(self.farm2.id)
        }

        response = self.client.execute(get_completed_tasks_query, variables)
        content = response.data

        assert len(content["getCompletedTasks"]) == 1


    def test_get_farm_task_counts(self):
        get_farm_task_counts_query = """
            query getVars($farm: String!)
            {
                getFarmTaskCounts(farmId: $farm)
                {
                    countType
                    count
                }
            }
        """

        variables = {
            "farm": str(self.farm1.id)
        }

        response = self.client.execute(get_farm_task_counts_query, variables)
        content = response.data

        assert len(content["getFarmTaskCounts"]) == 3