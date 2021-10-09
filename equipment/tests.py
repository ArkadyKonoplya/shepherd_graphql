import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from farm.models import Farm, FarmUsers, OrganizationRole
from equipment.models import (
    Equipment,
    EquipmentMake,
    EquipmentModel,
    EquipmentType,
    EquipmentUser,
)
from farm.models import OrganizationType
from shepherd.schema import schema


class EquipmentTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()
        self.user = get_user_model().objects.create(
            username="equipment_test",
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

        self.equipment_type1 = mixer.blend(
            EquipmentType,
            id=uuid.uuid4(),
            name="Tractor",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.equipment_type2 = mixer.blend(
            EquipmentType,
            id=uuid.uuid4(),
            name="Combine",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.equipment_make1 = mixer.blend(
            EquipmentMake,
            id=uuid.uuid4(),
            name="John Deere",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.equipment_make2 = mixer.blend(
            EquipmentMake,
            id=uuid.uuid4(),
            name="Case",
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.equipment_model1 = mixer.blend(
            EquipmentModel,
            id=uuid.uuid4(),
            name="Testing",
            equipment_type=self.equipment_type1,
            make=self.equipment_make1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.equipment_model2 = mixer.blend(
            EquipmentModel,
            id=uuid.uuid4(),
            name="CX60",
            equipment_type=self.equipment_type1,
            make=self.equipment_make2,
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
            equipment_type=self.equipment_type1,
        )
        self.equipment2 = mixer.blend(
            Equipment,
            id=uuid.uuid4(),
            make_model=self.equipment_model2,
            name="test Farm Equipment 2",
            equipment_type=self.equipment_type1,
            farm=self.farm1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def test_get_all_farm_equipment_response(self):
        get_all_farm_equipment_query = """
        query GetFarmUsername($farm: String!)
        {
            getAllFarmEquipment(farm: $farm){
                id
                name
            }
        }
        """
        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_all_farm_equipment_query, variables)
        content = response.data

        assert len(content["getAllFarmEquipment"]) == 2

    def test_get_all_equipment_makes_response(self):
        get_all_equipment_makes_query = """
        query
        {
            getAllEquipmentMakes{
                pageInfo {
                    startCursor
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                edges {
                    cursor
                    node {
                        id
                }
                }
            }
        }
        """

        response = self.client.execute(get_all_equipment_makes_query)
        content = response.data

        assert len(content["getAllEquipmentMakes"]) == 2

    def test_get_all_equipment_models_response(self):
        get_all_equipment_models_query = """
        query
        {
            getAllEquipmentModels{
                pageInfo {
                    startCursor
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                edges {
                    cursor
                    node {
                        id
                }
                }
            }
        }
        """

        response = self.client.execute(get_all_equipment_models_query)
        content = response.data
        assert len(content["getAllEquipmentModels"]) == 2

    def test_get_all_equipment_types_response(self):
        get_all_equipment_types_query = """
        query
        {
            getAllEquipmentTypes {
                id
                name
            }
        }
        """

        response = self.client.execute(get_all_equipment_types_query)
        content = response.data
        assert len(content["getAllEquipmentTypes"]) == 2

    def test_add_equipment_response(self):
        add_equipment = """
            mutation addEquipmentVariables($make_model: String!, $name: String!, $farm: String!)
            {
                addEquipment(makeModel: $make_model, name: $name, farm: $farm)
                {
                    equipment
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "make_model": str(self.equipment_model1.id),
            "name": "Test No Serial Num",
            "farm": str(self.farm1.id),
        }

        response = self.client.execute(add_equipment, variables)
        content = response.data

        assert len(content["addEquipment"]) == 1

    def test_add_equipment_response_no_make_model(self):
        add_equipment = """
            mutation addEquipmentVariables($name: String!, $farm: String!)
            {
                addEquipment(name: $name, farm: $farm)
                {
                    equipment
                    {
                        id
                    }
                }
            }
        """

        variables = {
            "name": "Test No Serial Num",
            "farm": str(self.farm1.id),
        }

        response = self.client.execute(add_equipment, variables)
        content = response.data

        assert len(content["addEquipment"]) == 1

    def test_add_equipment_response_with_serial_num(self):
        add_equipment = """
            mutation addEquipmentVariables($make_model: String!, $name: String!, $farm: String!, $serial_num: String!)
            {
                addEquipment(makeModel: $make_model, name: $name, farm: $farm, serialNum: $serial_num)
                {
                    equipment
                    {
                        serialNum
                    }
                }
            }
        """

        variables = {
            "make_model": str(self.equipment_model1.id),
            "name": "Test Serial Num",
            "farm": str(self.farm1.id),
            "serial_num": "TEST1234",
        }

        response = self.client.execute(add_equipment, variables)
        content = response.data

        assert content["addEquipment"]["equipment"]["serialNum"] == "TEST1234"

    def test_update_equipment(self):
        update_equipment = """
            mutation getVars($id: String!, $make_model: String!, $name: String!, $farm: String!)
            {
                updateEquipment(id: $id, makeModel: $make_model, name: $name, farm: $farm)
                {
                    success
                }
            }
        """

        variables = {
            "id": str(self.equipment1.id),
            "make_model": str(self.equipment1.make_model.id),
            "name": "Updated Name",
            "farm": str(self.equipment1.farm.id),
        }

        response = self.client.execute(update_equipment, variables)
        content = response.data

        assert content["updateEquipment"]["success"] is True

    def test_update_equipment_no_make_model(self):
        update_equipment = """
            mutation getVars($id: String!, $name: String!, $farm: String!)
            {
                updateEquipment(id: $id, name: $name, farm: $farm)
                {
                    success
                }
            }
        """

        variables = {
            "id": str(self.equipment1.id),
            "name": "Updated Name",
            "farm": str(self.equipment1.farm.id),
        }

        response = self.client.execute(update_equipment, variables)
        content = response.data

        assert content["updateEquipment"]["success"] is True

    def test_update_equipment_equipment_type(self):
        update_equipment = """
                mutation getVars($id: String!, $name: String!, $farm: String!, $type: String!)
                {
                    updateEquipment(id: $id, name: $name, farm: $farm, equipmentType: $type)
                    {
                        success
                    }
                }
            """

        variables = {
            "id": str(self.equipment1.id),
            "name": "Updated Name",
            "farm": str(self.equipment1.farm.id),
            "type": str(self.equipment_type1.id),
        }

        response = self.client.execute(update_equipment, variables)
        content = response.data

        assert content["updateEquipment"]["success"] is True

    def test_delete_equipment(self):
        delete_equipment = """
            mutation getVars($id: String!)
            {
                deleteEquipment(id: $id)
                {
                    success
                }
            }
        """

        variables = {"id": str(self.equipment2.id)}

        response = self.client.execute(delete_equipment, variables)
        content = response.data

        assert content["deleteEquipment"]["success"] is True

    def test_find_equipment_make(self):
        make_query = """
            query getVars($search: String!)
            {
                findEquipmentMake(search: $search)
                {
                  pageInfo {
                    startCursor
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                edges {
                    cursor
                    node {
                        id
                        name
                    }
                }
                }
            }
        """

        variables = {
            "search": "John"
        }

        response = self.client.execute(make_query, variables)
        content = response.data

        assert len(content["findEquipmentMake"]["edges"]) == 1

    def test_find_equipment_model(self):
        model_query = """
            query getVars($search: String!, $make_id: String!)
            {
                findEquipmentModel(search: $search, makeId: $make_id)
                {
                  pageInfo {
                    startCursor
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                edges {
                    cursor
                    node {
                        id
                        name
                    }
                }
                }
            }
        """

        variables = {
            "make_id": str(self.equipment_make1.id),
            "search": "Test"
        }

        response = self.client.execute(model_query, variables)
        content = response.data

        assert len(content["findEquipmentModel"]["edges"]) == 1

    def test_get_farm_equipment(self):
        get_farm_equipment_query = """
            query getVars($farm: String!, $equipment: String!)
            {
                getFarmEquipment(farm: $farm, equipmentId: $equipment)
                {
                    id
                    name
                }
            }
        """

        variables = {
            "farm": str(self.farm1.id),
            "equipment": str(self.equipment1.id)
        }

        response = self.client.execute(get_farm_equipment_query, variables)
        content = response.data

        assert len(content["getFarmEquipment"]) == 2