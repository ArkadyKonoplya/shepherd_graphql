import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from inventory.models import Inventory, InventoryUnitOfMeasure, ShoppingList


class InventoryType(DjangoObjectType):
    class Meta:
        model = Inventory
        fields = ("id", "item", "quantity", "farm_id", "unit_of_measure")


class InventoryUnitOfMeasureType(DjangoObjectType):
    class Meta:
        model = InventoryUnitOfMeasure
        fields = ("id", "name")


class ShoppingListType(DjangoObjectType):
    class Meta:
        model = ShoppingList
        fields = ("id", "item", "quantity", "farm_id", "unit_of_measure")


class Query(graphene.ObjectType):
    get_farm_inventory = graphene.List(
        InventoryType, farm=graphene.String(required=True)
    )
    get_farm_shopping_list = graphene.List(
        ShoppingListType, farm=graphene.String(required=True)
    )
    get_inventory_units_of_measure = graphene.List(InventoryUnitOfMeasureType)

    @login_required
    def resolve_get_farm_inventory(self, info, farm):
        return Inventory.objects.filter(
            farm_id=farm,
            deleted_at=None,
            farm_id__member_farms__user_id=info.context.user.id,
        )

    @login_required
    def resolve_get_farm_shopping_list(self, info, farm):
        return ShoppingList.objects.filter(
            farm_id=farm,
            deleted_at=None,
            farm_id__member_farms__user_id=info.context.user.id,
        )

    @login_required
    def resolve_get_inventory_units_of_measure(self, info):
        return InventoryUnitOfMeasure.objects.filter(deleted_at=None)


schema = graphene.Schema(query=Query)
