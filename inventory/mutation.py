import graphene
from graphql_jwt.decorators import login_required

from inventory.models import Inventory, ShoppingList
from inventory.schema import InventoryType, ShoppingListType


class InventoryAddMutation(graphene.Mutation):
    class Arguments:
        item = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        farm = graphene.String(required=True)
        unit_of_measure = graphene.String(required=True)
        location = graphene.String(required=True)

    inventory_item = graphene.Field(InventoryType)

    @login_required
    def mutate(self, info, item, quantity, farm, unit_of_measure, location):

        inventory_item = Inventory(
            item=item,
            quantity=quantity,
            farm_id_id=farm,
            unit_of_measure_id=unit_of_measure,
            location_id=location,
        )
        inventory_item.created_by = info.context.user.id
        inventory_item.modified_by = info.context.user.id

        inventory_item.save()

        return InventoryAddMutation(inventory_item=inventory_item)


class InventoryDeleteMutation(graphene.Mutation):

    success = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)

    @login_required
    def mutate(self, info, id):
        inventory_item = Inventory.objects.get(pk=id)
        inventory_item.delete()

        return InventoryDeleteMutation(success=True)


class InventoryMoveMutation(graphene.Mutation):
    class Arguments:
        inventory_id = graphene.String(required=True)

    shopping_list_item = graphene.Field(ShoppingListType)

    @login_required
    def mutate(self, info, inventory_id):
        inventory_item = Inventory.objects.get(pk=inventory_id)

        new_shopping_list_item = ShoppingList()
        new_shopping_list_item.item = inventory_item.item
        new_shopping_list_item.quantity = inventory_item.quantity
        new_shopping_list_item.farm_id = inventory_item.farm_id
        new_shopping_list_item.unit_of_measure = inventory_item.unit_of_measure
        new_shopping_list_item.created_by = info.context.user.id
        new_shopping_list_item.modified_by = info.context.user.id
        new_shopping_list_item.save()

        inventory_item.delete()

        return InventoryMoveMutation(shopping_list_item=new_shopping_list_item)


class ShoppingListAddMutation(graphene.Mutation):
    class Arguments:
        item = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        farm = graphene.String(required=True)
        unit_of_measure = graphene.String(required=True)

    shopping_list_item = graphene.Field(ShoppingListType)

    @login_required
    def mutate(self, info, item, quantity, farm, unit_of_measure):
        shopping_list_item = ShoppingList(
            item=item,
            quantity=quantity,
            farm_id_id=farm,
            unit_of_measure_id=unit_of_measure,
        )
        shopping_list_item.created_by = info.context.user.id
        shopping_list_item.modified_by = info.context.user.id

        shopping_list_item.save()

        return ShoppingListAddMutation(shopping_list_item=shopping_list_item)


class ShoppingListDeleteMutation(graphene.Mutation):

    success = graphene.Boolean()

    class Arguments:
        shopping_id = graphene.String(required=True)

    @login_required
    def mutate(self, info, shopping_id):
        shopping_list_item = ShoppingList.objects.get(pk=shopping_id)
        shopping_list_item.delete()

        return ShoppingListDeleteMutation(success=True)


class ShoppingListMoveMutation(graphene.Mutation):
    class Arguments:
        item_id = graphene.String(required=True)

    inventory_item = graphene.Field(InventoryType)

    @login_required
    def mutate(self, info, item_id):
        shopping_list_item = ShoppingList.objects.get(id=item_id)

        new_inventory_item = Inventory()
        new_inventory_item.item = shopping_list_item.item
        new_inventory_item.quantity = shopping_list_item.quantity
        new_inventory_item.farm_id = shopping_list_item.farm_id
        new_inventory_item.unit_of_measure = shopping_list_item.unit_of_measure
        new_inventory_item.created_by = info.context.user.id
        new_inventory_item.modified_by = info.context.user.id
        new_inventory_item.save()

        shopping_list_item.delete()

        return ShoppingListMoveMutation(inventory_item=new_inventory_item)


class Mutation(graphene.ObjectType):
    add_inventory = InventoryAddMutation.Field()
    add_shopping_list = ShoppingListAddMutation.Field()

    remove_inventory = InventoryDeleteMutation.Field()
    remove_shopping_list = ShoppingListDeleteMutation.Field()

    move_inventory = InventoryMoveMutation.Field()
    move_shopping_list = ShoppingListMoveMutation.Field()
