import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from crop.models import Crop
from farm.models import (
    Farm,
    FarmUsers,
    OrganizationType,
    OrganizationLocationRel,
    OrganizationTypeLocationTypeRel,
    OrganizationRole,
)
from field.models import Location, LocationType
from plan.models import Plan

from shepherd.schema import schema


class FarmTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()
        user2_id = uuid.uuid4()
        self.user = get_user_model().objects.create(
            username="farm_test",
            id=user_id,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.user2 = get_user_model().objects.create(
            username="owner_test",
            id=user2_id,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.user3 = get_user_model().objects.create(
            username="user_test",
            id=uuid.uuid4(),
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
        self.farm_type2 = mixer.blend(
            OrganizationType,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.farm_type3 = mixer.blend(
            OrganizationType,
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
        self.role2 = mixer.blend(
            OrganizationRole,
            id=uuid.uuid4(),
            name="owner",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.farm1 = mixer.blend(
            Farm,
            id=uuid.uuid4(),
            type=self.farm_type,
            code="ABC123",
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

        self.farm_user = mixer.blend(
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
            user=self.user,
            role=self.role1,
            default_farm=True,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.farm_user3 = mixer.blend(
            FarmUsers,
            id=uuid.uuid4(),
            farm=self.farm1,
            user=self.user2,
            role=self.role2,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.crop1 = mixer.blend(
            Crop,
            id=uuid.uuid4(),
            name="test crop",
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

        self.org_loc1 = mixer.blend(
            OrganizationLocationRel,
            id=uuid.uuid4(),
            farm=self.farm1,
            location=self.location1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.org_loc2 = mixer.blend(
            OrganizationLocationRel,
            id=uuid.uuid4(),
            farm=self.farm1,
            location=self.location2,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.org_loc3 = mixer.blend(
            OrganizationLocationRel,
            id=uuid.uuid4(),
            farm=self.farm1,
            location=self.location3,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        today = datetime.today()
        self.plan = mixer.blend(
            Plan,
            id=uuid.uuid4(),
            crop=self.crop1,
            location=self.location1,
            plan_year=today.year,
            planner=self.user,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def test_check_valid_farm_code(self):
        check_valid_farm_code_query = """
           query GetFarmCode($code: String!)
           {
               checkValidFarmCode(code: $code){
                  id
               }
           }
           """

        variables = {"code": self.farm1.code}

        response = self.client.execute(check_valid_farm_code_query, variables)
        content = response.data

        assert len(content["checkValidFarmCode"]) == 1

    def test_check_valid_farm_code_invalid(self):
        check_invalid_farm_code_query = """
            query GetFarmCode($code: String!)
           {
               checkValidFarmCode(code: $code)
               {
                 id
               }
           }
        """

        variables = {"code": "AAABBBCCC"}

        response = self.client.execute(check_invalid_farm_code_query, variables)
        errors = response.errors

        assert (
            "The farm with code AAABBBCCC doesn't exist. Please check your code and try again."
            in errors[0].message
        )

    def test_get_farm_response(self):
        get_farm_query = """
        query GetFarm($farm: String!, $username: String!)
        {
            getFarm(farm: $farm, username: $username){
                name
            }
        }
        """
        variables = {"farm": str(self.farm1.id), "username": str(self.user.username)}
        response = self.client.execute(get_farm_query, variables)
        content = response.data

        assert len(content["getFarm"]) == 1

    def test_get_farm_counts(self):
        get_farm_counts_query = """
            query getFarmCounts($farm: String!)
            {
                getFarmCounts(farm: $farm)
                {
                    workerCount,
                    fieldCount,
                    equipmentCount,
                    inventoryCount,
                }
            }
        """

        variables = {
            "farm": str(self.farm1.id),
        }

        response = self.client.execute(get_farm_counts_query, variables)
        content = response.data
        assert content["getFarmCounts"]["workerCount"] == 2
        assert content["getFarmCounts"]["fieldCount"] == 3
        assert content["getFarmCounts"]["inventoryCount"] == 0
        assert content["getFarmCounts"]["equipmentCount"] == 0

    def test_get_farm_locations(self):
        get_farm_locations_query = """
        query GetFarm($farm: String!)
        {
            getFarmLocations(farm: $farm){
                location{
                    id
                    name
                }
            }
        }
        """

        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_farm_locations_query, variables)
        content = response.data

        assert len(content["getFarmLocations"]) == 3

    def test_get_farm_roles(self):
        get_farm_roles_query = """
            query
             { getFarmRoles
               {
                id
                name
               }
             }
        """

        response = self.client.execute(get_farm_roles_query)
        content = response.data

        assert len(content["getFarmRoles"]) == 2

    def test_add_farm(self):
        add_farm_mutation = """
            mutation GetFarmType($type: String!)
            {
                addFarm(name: "Test Farm", code: "abc123", farmType: $type){
                    farm {
                        name
                    }
                }
            }
        """
        variables = {"type": str(self.farm_type.id)}

        response = self.client.execute(add_farm_mutation, variables)
        content = response.data

        assert len(content["addFarm"]) == 1

    def test_get_farm_types(self):
        get_farm_types_query = """
            query
            {
                getFarmTypes
                {
                    id
                    name
                }
            }

        """

        response = self.client.execute(get_farm_types_query)
        content = response.data

        assert len(content["getFarmTypes"]) == 3

    def test_add_farm_user_additional_farm(self):
        """
        Test verifies that if a user gets added to an additional farm, default farm is FALSE
        :return:
        """
        add_farm_user = """
            mutation GetFarm($farm: String!, $user: String!, $role: String!)
            {
                addFarmUser(farm: $farm, user: $user, role: $role){
                    farmUser{
                        id,
                        defaultFarm
                    }
                }
            }
        """
        variables = {
            "farm": str(self.farm2.id),
            "user": str(self.user2.id),
            "role": str(self.role1.id),
        }

        response = self.client.execute(add_farm_user, variables)
        content = response.data

        assert len(content["addFarmUser"]["farmUser"]) == 2
        assert content["addFarmUser"]["farmUser"]["defaultFarm"] is False

    def test_add_farm_user_no_previous_farm(self):
        add_farm_user = """
            mutation GetFarm($farm: String!, $user: String!, $role: String!)
            {
                addFarmUser(farm: $farm, user: $user, role: $role){
                    farmUser{
                        id,
                        defaultFarm
                    }
                }
            }
        """
        variables = {
            "farm": str(self.farm1.id),
            "user": str(self.user3.id),
            "role": str(self.role1.id),
        }

        response = self.client.execute(add_farm_user, variables)
        content = response.data

        assert len(content["addFarmUser"]["farmUser"]) == 2
        assert content["addFarmUser"]["farmUser"]["defaultFarm"] is True

    def test_add_farm_user_already_member(self):
        add_farm_user = """
                    mutation GetFarm($farm: String!, $user: String!, $role: String!)
                    {
                        addFarmUser(farm: $farm, user: $user, role: $role){
                            farmUser{
                                id,
                                defaultFarm
                            }
                        }
                    }
                """
        variables = {"farm": str(self.farm1.id), "user": str(self.user.id), "role": str(self.role1.id)}

        response = self.client.execute(add_farm_user, variables)
        errors = response.errors

        assert "User is already member of this farm." in errors[0].message

    def test_update_farm_user(self):
        update_farm_user = """
            mutation getFarmUser($farm: String!, $user: String!, $role: String!)
            {
                updateFarmUser(farm: $farm, user: $user, role: $role)
                {
                    farmUser
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "farm": str(self.farm1.id),
            "user": str(self.user.id),
            "role": str(self.role2.id),
        }

        response = self.client.execute(update_farm_user, variables)
        content = response.data
        assert len(content["updateFarmUser"]["farmUser"]) == 1

    def test_update_farm_user_new_default_farm(self):
        update_farm_user = """
            mutation getFarmUser($farm: String!, $user: String!, $role: String!, $default_farm: Boolean!)
            {
                updateFarmUser(farm: $farm, user: $user, role: $role, defaultFarm: $default_farm)
                {
                    farmUser
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "farm": str(self.farm1.id),
            "user": str(self.user.id),
            "role": str(self.role2.id),
            "default_farm": True,
        }

        response = self.client.execute(update_farm_user, variables)
        content = response.data

        assert len(content["updateFarmUser"]["farmUser"]) == 1

    def test_remove_farm_user(self):
        remove_farm_user = """
            mutation GetFarm($farm: String!, $user: String!)
            {
                removeFarmUser(farm: $farm, user: $user){
                    success
                }
            }
        """
        variables = {"farm": str(self.farm1.id), "user": str(self.user.id)}

        response = self.client.execute(remove_farm_user, variables)
        content = response.data

        assert content["removeFarmUser"]["success"] is True

    def test_remove_farm_user_owner(self):
        remove_farm_user = """
            mutation GetFarm($farm: String!, $user: String!)
            {
                removeFarmUser(farm: $farm, user: $user){
                    success
                }
            }
        """
        variables = {"farm": str(self.farm1.id), "user": str(self.user2.id)}

        response = self.client.execute(remove_farm_user, variables)
        errors = response.errors

        assert "Owners are unable to be removed from their farms." in errors[0].message

    def test_remove_farm(self):
        remove_farm_mutation = """
            mutation GetFarm($farm: ID!)
            {
                removeFarm(farmId: $farm){
                    farm{
                        id
                    }
                }
            }
        """
        variables = {"farm": str(self.farm2.id)}

        response = self.client.execute(remove_farm_mutation, variables)
        content = response.data
        assert len(content["removeFarm"]) == 1
