import uuid

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from mixer.backend.django import mixer

from farm.models import Farm, OrganizationType, FarmUsers, OrganizationRole
from field.models import Location, LocationType
from inventory.models import Inventory, InventoryUnitOfMeasure, ShoppingList

from shepherd.schema import schema


class InventoryTests(JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        user_id = uuid.uuid4()
        self.user = get_user_model().objects.create(
            username="inventory_test",
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

        self.uom1 = mixer.blend(
            InventoryUnitOfMeasure,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )
        self.uom2 = mixer.blend(
            InventoryUnitOfMeasure,
            id=uuid.uuid4(),
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.inventory_item1 = mixer.blend(
            Inventory,
            id=uuid.uuid1(),
            farm_id=self.farm1,
            unit_of_measure=self.uom1,
            location=self.location1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.inventory_item2 = mixer.blend(
            Inventory,
            id=uuid.uuid1(),
            farm_id=self.farm1,
            unit_of_measure=self.uom2,
            location=self.location1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.shopping_list_item1 = mixer.blend(
            ShoppingList,
            id=uuid.uuid1(),
            farm_id=self.farm1,
            unit_of_measure=self.uom1,
            location=self.location1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

        self.shopping_list_item2 = mixer.blend(
            ShoppingList,
            id=uuid.uuid1(),
            farm_id=self.farm1,
            unit_of_measure=self.uom2,
            location=self.location1,
            created_by=user_id,
            modified_by=user_id,
            deleted_by=None,
            deleted_at=None,
        )

    def test_get_farm_inventory_result(self):
        get_farm_inventory_query = """
        query GetFarm($farm: String!)
        {
            getFarmInventory(farm: $farm){
                id
                item
                quantity
            }
        }
        """
        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_farm_inventory_query, variables)
        content = response.data
        assert len(content["getFarmInventory"]) == 2

    def test_get_farm_shopping_list_result(self):
        get_farm_shopping_list_result = """
        query GetFarm($farm: String!)
        {
            getFarmShoppingList(farm: $farm){
                id
                item
                quantity
            }
        }
        """

        variables = {"farm": str(self.farm1.id)}

        response = self.client.execute(get_farm_shopping_list_result, variables)
        content = response.data
        assert len(content["getFarmShoppingList"]) == 2

    def test_get_inventory_units_of_measure(self):
        get_inventory_uom_results_query = """
            query{
                getInventoryUnitsOfMeasure{
                    id
                    name
                }
            }
        """

        response = self.client.execute(get_inventory_uom_results_query)
        content = response.data

        assert len(content["getInventoryUnitsOfMeasure"]) == 2

    def test_add_inventory_result(self):
        add_inventory_query = """
            mutation inventoryVars($item: String!, $farm: String!, $location: String!, $uom: String!)
            {
                addInventory(item: $item, farm: $farm, location: $location, quantity: 1000, unitOfMeasure: $uom)
                {
                    inventoryItem
                    {
                        id
                        item
                    }
                }
            }
        """

        variables = {
            "item": "testing",
            "farm": str(self.farm1.id),
            "location": str(self.location1.id),
            "uom": str(self.uom1.id),
        }

        response = self.client.execute(add_inventory_query, variables)
        content = response.data

        assert len(content["addInventory"]) == 1

    def test_add_shopping_list_result(self):
        add_shopping_list_query = """
            mutation shoppingVars($item: String!, $farm: String!, $uom: String!)
            {
                addShoppingList(item: $item, quantity: 10000, farm: $farm, unitOfMeasure: $uom)
                {
                    shoppingListItem
                    {
                        id
                        item
                    }
                }
            }
        """

        variables = {
            "item": "shopping test",
            "farm": str(self.farm1.id),
            "uom": str(self.uom1.id),
        }

        response = self.client.execute(add_shopping_list_query, variables)
        content = response.data

        assert len(content["addShoppingList"]) == 1

    def test_remove_inventory_result(self):
        remove_inventory_mutation = """
            mutation inventoryVars($inventory_id: String!)
            {
                removeInventory(id: $inventory_id)
                {
                    success
                }
            }
        """
        variables = {"inventory_id": str(self.inventory_item1.id)}

        response = self.client.execute(remove_inventory_mutation, variables)
        content = response.data

        assert content["removeInventory"]["success"] is True

    def test_remove_shopping_list_result(self):
        remove_shopping_list_mutation = """
            mutation shoppingListVars($shopping_id: String!)
            {
                removeShoppingList(shoppingId: $shopping_id)
                {
                    success
                }
            }
        """

        variables = {"shopping_id": str(self.shopping_list_item1.id)}

        response = self.client.execute(remove_shopping_list_mutation, variables)
        content = response.data

        assert content["removeShoppingList"]["success"] is True

    def test_move_inventory_result(self):
        move_inventory_query = """
            mutation inventoryItem($inventory_id: String!)
            {
                moveInventory(inventoryId: $inventory_id)
                {
                    shoppingListItem
                    {
                        id
                    }
                }
            }
        """

        variables = {"inventory_id": str(self.inventory_item2.id)}

        response = self.client.execute(move_inventory_query, variables)
        content = response.data

        assert len(content["moveInventory"]) == 1

    def test_move_shopping_list_result(self):
        move_shopping_list_query = """
            mutation shoppingItem($shopping_item: String!)
            {
                moveShoppingList(itemId: $shopping_item)
                {
                    inventoryItem
                    {
                        id
                    }
                }
            }
        """

        variables = {"shopping_item": str(self.shopping_list_item2.id)}

        response = self.client.execute(move_shopping_list_query, variables)
        content = response.data

        assert len(content["moveShoppingList"]) == 1
