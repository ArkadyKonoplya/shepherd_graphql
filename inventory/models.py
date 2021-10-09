import uuid

from django.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class Inventory(models.Model):
    class Meta:
        db_table = "inventory"

    id = models.UUIDField(
        db_column="inventory_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    item = models.CharField(db_column="inventory_item", null=False, max_length=750)
    quantity = models.FloatField(db_column="inventory_quantity", null=False)
    farm_id = models.ForeignKey(
        "farm.Farm", db_column="organization_id", null=False, on_delete=models.CASCADE
    )
    unit_of_measure = models.ForeignKey(
        "InventoryUnitOfMeasure",
        db_column="inventory_uom",
        null=False,
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey("field.Location", blank=True, null=True, on_delete=models.CASCADE)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()


class InventoryUnitOfMeasure(models.Model):
    class Meta:
        db_table = "inventory_uom_type"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="inventory_uom_type_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(db_column="uom_type_name", max_length=250)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    class Meta:
        db_table = "shopping_list"

    id = models.UUIDField(
        db_column="shopping_list_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    item = models.CharField(db_column="shopping_list_item", max_length=750, null=False)
    quantity = models.FloatField(db_column="shopping_list_quantity", null=False)
    farm_id = models.ForeignKey(
        "farm.Farm", db_column="organization_id", null=False, on_delete=models.CASCADE
    )
    unit_of_measure = models.ForeignKey(
        "InventoryUnitOfMeasure",
        db_column="shopping_list_uom",
        null=False,
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey("field.Location", blank=True, null=True, on_delete=models.CASCADE)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
