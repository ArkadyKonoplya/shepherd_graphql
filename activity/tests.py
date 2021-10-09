import datetime
import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from activity.models import Activity, ActivityDetail, ActivityDetailRel, FarmTypeActivityRel, CustomActivity
from farm.models import Farm, OrganizationType, FarmUsers, OrganizationRole

from shepherd.schema import schema


class ActivityTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()
        self.user = get_user_model().objects.create(
            username="activity_test",
            id=user_id,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.client.authenticate(self.user)

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

        self.custom_activity1 = mixer.blend(
            CustomActivity,
            farm_id=str(self.farm1.id),
            name="Custom Activity 1",
            requires_crop=True,
            id=uuid.uuid4(),
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

        self.farm_user = mixer.blend(
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

    def test_get_activity_details(self):
        get_activity_details_query = """
            query getActivity($activity: String!)
            {
                getActivityDetails(activityId: $activity)
                {
                    id
                    activityDetail
                    {
                        id
                        name
                    }
                }
            }
        """
        variables = {"activity": str(self.activity1.id)}

        response = self.client.execute(get_activity_details_query, variables)
        content = response.data

        assert len(content["getActivityDetails"]) == 2

    def test_get_all_activity_details_results(self):
        get_all_activity_details_query = """
            query
            {
                getAllActivityDetails
                {
                    id
                    name
                }
            }
        """

        response = self.client.execute(get_all_activity_details_query)
        content = response.data

        assert len(content["getAllActivityDetails"]) == 3

    def test_get_all_activity_types_results(self):
        get_all_activity_types_query = """
                query
                {
                    getAllActivityTypes
                    {
                        id
                        name
                    }
                }
            """

        response = self.client.execute(get_all_activity_types_query)
        content = response.data

        assert len(content["getAllActivityTypes"]) == 2

    def test_get_farm_activities(self):
        get_farm_activities_query = """
            query farmParam($farm: String!)
            {
                getFarmActivities(farm: $farm)
                {
                    ... on CustomActivityType
                    {
                        id
                        name
                    }
                    ... on ActivityType
                    {
                        id
                        name
                    }
                }
            }
        """
        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_farm_activities_query, variables)
        content = response.data

        assert len(content["getFarmActivities"]) == 3

    def test_create_custom_activity(self):
        create_custom_activity_mutation = """
            mutation getParams($name: String!, $requires_crop: Boolean!)
            {
                addCustomActivity(name: $name, requiresCrop: $requires_crop)
                {
                    customActivity
                    {
                        name
                    }
                }
            }
        """

        variables = {
            "name": "Test Custom Activity",
            "requires_crop": True,
        }

        response = self.client.execute(create_custom_activity_mutation, variables)
        content = response.data

        assert content["addCustomActivity"]["customActivity"]["name"] == "Test Custom Activity"

    def test_update_custom_activity(self):
        update_custom_activity_mutation = """
            mutation getParams($id: String!, $name: String!, $requires_crop: Boolean!)
            {
                updateCustomActivity(id: $id, name: $name, requiresCrop: $requires_crop)
                {
                    success
                }
            }
        """

        variables = {
            "id": str(self.custom_activity1.id),
            "name": "Revised Activity Name",
            "requires_crop": True,
        }

        response = self.client.execute(update_custom_activity_mutation, variables)
        content = response.data

        assert content["updateCustomActivity"]["success"] is True

    def test_delete_custom_activity(self):
        delete_custom_activity_mutation = """
            mutation getParams($id: String!)
            {
                deleteCustomActivity(id: $id)
                {
                    success
                }
            }
        """

        variables = {
            "id": str(self.custom_activity1.id)
        }

        response = self.client.execute(delete_custom_activity_mutation, variables)
        content = response.data

        assert content["deleteCustomActivity"]["success"] is True