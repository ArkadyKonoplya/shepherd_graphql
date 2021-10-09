import datetime
import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from activity.models import Activity
from crop.models import Crop
from farm.models import Farm, OrganizationType, OrganizationLocationRel, OrganizationRole, FarmUsers
from field.models import Location, LocationType
from plan.models import Plan
from task.models import Task, TaskStatus, TaskHistory

from shepherd.schema import schema


class PlanTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()
        self.user = get_user_model().objects.create(
            username="plan_test",
            id=user_id,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.client.authenticate(self.user)

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


        self.crop1 = mixer.blend(
            Crop,
            id=uuid.uuid4(),
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

        self.task1 = mixer.blend(
            Task,
            id=uuid.uuid4(),
            task_creator=self.user,
            task_location=self.location1,
            task_activity=self.activity1,
            task_custom_activity=None,
            task_status=self.available_status,
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
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_history_1 = mixer.blend(
            TaskHistory,
            id=uuid.uuid4(),
            task_id=self.task5,
            update_user=self.user,
            assigned_user=self.user,
            status_date_change=datetime.datetime.today() - datetime.timedelta(days=1),
            status_change_location="0101000020E61000002959F38876545940C2823463D15E4140",
            task_status=self.accepted_status,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_history_2 = mixer.blend(
            TaskHistory,
            id=uuid.uuid4(),
            task_id=self.task5,
            update_user=self.user,
            assigned_user=self.user,
            status_date_change=datetime.datetime.today() - datetime.timedelta(hours=6),
            status_change_location="0101000020E61000002959F38876545940C2823463D15E4140",
            task_status=self.deleted_status,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_history_3 = mixer.blend(
            TaskHistory,
            id=uuid.uuid4(),
            task_id=self.task5,
            update_user=self.user,
            assigned_user=self.user,
            status_date_change=datetime.datetime.today() - datetime.timedelta(hours=2),
            status_change_location="0101000020E61000002959F38876545940C2823463D15E4140",
            task_status=self.deleted_status,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def get_farm_plans_no_plans(self):
        """
        Testing for when no plans for current/future years are available.
        :return:
        """
        get_farm_plans_query = """
            query GetFarm($farm: String!)
            {
                getFarmPlans(farm: $farm){
                    id
                    planYear
                    location{
                        name
                    }
                }
            }
        """

        variables = {"farm": self.farm2.id}

        response = self.client.execute(get_farm_plans_query, variables)
        errors = response.errors

        assert (
                f"{self.farm2.id} does not have plans for the current or future years."
                in errors[0].message
        )

    def test_add_plan(self):

        add_plan_mutation = """
            mutation getPlan($crop: String!, $location: String!, $plan_year: String!)
            {
                addPlan(crop: $crop, location: $location, planYear: $plan_year)
                {
                    plan
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "crop": str(self.crop1.id),
            "location": str(self.location1.id),
            "plan_year": "2021",
        }

        response = self.client.execute(add_plan_mutation, variables)
        content = response.data

        assert len(content["addPlan"]) == 1

    def test_delete_plan(self):

        delete_plan_mutation = """
            mutation getPlan($plan: String!)
            {
                deletePlan(plan: $plan)
                {
                    success
                }
            }
        """

        variables = {"plan": str(self.plan.id)}

        response = self.client.execute(delete_plan_mutation, variables)
        content = response.data

        assert content["deletePlan"]["success"] is True

    def test_get_location_plans(self):

        get_location_plans_query = """
            query getPLan($location: String!)
            {
                getLocationPlans(location: $location)
                {
                    id
                }
            }
        """

        variables = {"location": str(self.location1.id)}

        response = self.client.execute(get_location_plans_query, variables)
        content = response.data

        assert len(content["getLocationPlans"]) == 1

    def test_get_plan_tasks_results(self):
        get_plan_tasks_query = """
            query getVars($plan: String!)
            {
                getPlanTasks(planId: $plan)
                {
                    id
                    history
                    {
                        id
                        statusDateChange
                    }
                }
            }
        """

        variables = {"plan": str(self.plan.id)}

        response = self.client.execute(get_plan_tasks_query, variables)
        content = response.data

        assert len(content["getPlanTasks"]) == 5

    def test_get_farm_plans(self):
        get_farm_plans_query = """
            query taskParams($farm: String!)
            {
                getFarmPlans(farmId: $farm){
                    id
                    planYear
                    location{
                        name
                        organization{
                            id
                        }
                    }
                    tasks
                    {
                        id
                    }
                }
            }
        """

        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_farm_plans_query, variables)
        content = response.data

        assert len(content["getFarmPlans"]) == 1
        assert len(content["getFarmPlans"][0]["tasks"]) == 5

    def test_get_farm_plan(self):
        get_farm_plan_query = """
            query getFarmPlanParams($farm: String!, $plan: String!)
            {
                getFarmPlan(farmId: $farm, planId: $plan)
                {
                    id
                    planYear
                }
            }
        """

        variables = {"farm": str(self.farm1.id), "plan": str(self.plan.id)}

        response = self.client.execute(get_farm_plan_query, variables)

        content = response.data
        assert len(content["getFarmPlan"]) == 2

    def test_get_plan_activity_log(self):
        get_plan_activity_log_query = """
            query getVars($plan: String!)
            {
                getPlanActivityLog(planId: $plan)
                {
                    id
                }
            }
        """

        variables = {
            "plan": str(self.plan.id)
        }

        response = self.client.execute(get_plan_activity_log_query, variables)
        content = response.data

        assert len(content["getPlanActivityLog"]) == 3
