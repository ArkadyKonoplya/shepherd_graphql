import datetime
import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from activity.models import Activity
from crop.models import Crop
from field.models import LocationType, Location
from farm.models import OrganizationLocationRel, Farm, OrganizationType
from task.models import Task, TaskStatus, TaskHistory
from plan.models import Plan

from shepherd.schema import schema


class FieldTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()
        today = datetime.datetime.today()

        self.user = get_user_model().objects.create(
            username="equipment_test",
            id=user_id,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.client.authenticate(self.user)

        self.location_type1 = mixer.blend(
            LocationType,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.location_type2 = mixer.blend(
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
        self.location3 = mixer.blend(
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

        self.farm_loc1 = mixer.blend(
            OrganizationLocationRel,
            id=uuid.uuid4(),
            farm=self.farm1,
            location=self.location1,
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

        self.task1 = mixer.blend(
            Task,
            id=uuid.uuid4(),
            task_creator=self.user,
            task_location=self.location1,
            task_activity=self.activity1,
            task_custom_activity=None,
            task_status=self.accepted_status,
            task_crop=self.crop1,
            task_assignee=self.user,
            task_plan=self.plan,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.task_history_1 = mixer.blend(
            TaskHistory,
            id=uuid.uuid4(),
            task_id=self.task1,
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
            task_id=self.task1,
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
            task_id=self.task1,
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

    def test_create_location_mutation_response(self):
        add_location_query = """
            mutation locationParam($location_name: String!, $location_type_id: String!, $acres: Float!, $image: String!
                                , $drawn_area: String!, $legal_name: String!, $farm_id: String!)
            {
                addLocation(locationName: $location_name, locationTypeId: $location_type_id, acres: $acres, image: $image,
                            drawnArea: $drawn_area, legalName: $legal_name, farmId: $farm_id)
                {
                    location{
                        id
                    }
                }
            }
        """

        variables = {
            "location_name": "test location",
            "location_type_id": str(self.location_type1.id),
            "acres": 123.34,
            "image": "\/home\/ameadows\/Downloads\/external-content.duckduckgo.com.jpeg",
            "drawn_area": "POLYGON((-78.6207918152582 35.5963473238645,-78.6206335649117 35.5965828721579,-78.6205316409598 35.5966831980725,-78.6203841194504 35.5967682569015,-78.6207918152582 35.5963473238645))",
            "legal_name": "Test Legal Name",
            "farm_id": str(self.farm1.id),
        }

        response = self.client.execute(add_location_query, variables)
        content = response.data

        assert len(content["addLocation"]) == 1

    def test_update_location_mutation_same_farm_response(self):
        update_location_query = """
                    mutation locationParam($location_id: String!, $location_name: String!, $location_type_id: String!
                                           , $acres: Float!, $image: String!, $drawn_area: String!, $legal_name: String!
                                           , $farm_id: String!)
                    {
                        updateLocation(locationId: $location_id, locationName: $location_name
                                       , locationTypeId: $location_type_id, acres: $acres, image: $image,
                                       drawnArea: $drawn_area, legalName: $legal_name, farmId: $farm_id)
                        {
                            location{
                                id
                            }
                        }
                    }
                """

        variables = {
            "location_id": str(self.location1.id),
            "location_name": self.location1.name,
            "location_type_id": str(self.location_type1.id),
            "acres": 123.34,
            "image": "\/home\/ameadows\/Downloads\/external-content.duckduckgo.com.jpeg",
            "drawn_area": "POLYGON((-78.6207918152582 35.5963473238645,-78.6206335649117 35.5965828721579,-78.6205316409598 35.5966831980725,-78.6203841194504 35.5967682569015,-78.6207918152582 35.5963473238645))",
            "legal_name": "Test Legal Name",
            "farm_id": str(self.farm1.id),
        }

        response = self.client.execute(update_location_query, variables)
        content = response.data

        assert len(content["updateLocation"]) == 1

    def test_update_location_mutation_different_farm_response(self):
        update_location_query = """
                    mutation locationParam($location_id: String!, $location_name: String!, $location_type_id: String!
                                           , $acres: Float!, $image: String!, $drawn_area: String!, $legal_name: String!
                                           , $farm_id: String!)
                    {
                        updateLocation(locationId: $location_id, locationName: $location_name
                                       , locationTypeId: $location_type_id, acres: $acres, image: $image,
                                       drawnArea: $drawn_area, legalName: $legal_name, farmId: $farm_id)
                        {
                            location{
                                id
                            }
                        }
                    }
                """

        variables = {
            "location_id": str(self.location1.id),
            "location_name": self.location1.name,
            "location_type_id": str(self.location_type1.id),
            "acres": 123.34,
            "image": "\/home\/ameadows\/Downloads\/external-content.duckduckgo.com.jpeg",
            "drawn_area": "POLYGON((-78.6207918152582 35.5963473238645,-78.6206335649117 35.5965828721579,-78.6205316409598 35.5966831980725,-78.6203841194504 35.5967682569015,-78.6207918152582 35.5963473238645))",
            "legal_name": "Test Legal Name",
            "farm_id": str(self.farm2.id),
        }

        response = self.client.execute(update_location_query, variables)
        content = response.data

        assert len(content["updateLocation"]) == 1

    def test_get_all_location_types_response(self):
        get_all_location_types_query = """
        query{
            getAllLocationTypes{
                id
                name
            }
        }
        """

        response = self.client.execute(get_all_location_types_query)
        content = response.data

        assert len(content["getAllLocationTypes"]) == 2

    def test_get_location(self):
        get_location_query = """
        query getParams($location: String!)
        {
            getLocation(locationId: $location)
            {
                id
                weather
                {
                    currently
                    {
                        time
                    }
                }
            }
        }
        """

        variables = {"location": str(self.location1.id)}

        response = self.client.execute(get_location_query, variables)
        content = response.data

        assert len(content["getLocation"]) == 2

    def test_delete_location(self):
        delete_location = """
            mutation getVars($location: String!)
            {
                deleteLocation(locationId: $location)
                {
                    success
                }
            }
        """

        variables = {"location": str(self.location2.id)}

        response = self.client.execute(delete_location, variables)
        content = response.data

        assert content["deleteLocation"]["success"] is True

    def test_delete_location_with_tasks(self):
        delete_location = """
            mutation getVars($location: String!)
            {
                deleteLocation(locationId: $location)
                {
                    success
                }
            }
        """

        variables = {"location": str(self.location1.id)}

        response = self.client.execute(delete_location, variables)
        errors = response.errors

        assert f"{self.location1.name} can not be deleted.  There are 1 active tasks in progress. Please " \
               f"complete or delete tasks before deleting this location." in errors[0].message

    def test_get_location_activity_log(self):
        get_location_activity_log = """
            query getVars($location: String!)
            {
                getLocationActivityLog(locationId: $location)
                {
                    id
                }
            }
        """

        variables = {"location": str(self.location1.id)}

        response = self.client.execute(get_location_activity_log, variables)
        content = response.data

        assert len(content["getLocationActivityLog"]) == 3