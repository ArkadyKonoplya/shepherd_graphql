import uuid

from django.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class Equipment(models.Model):
    class Meta:
        db_table = "equipment"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="equipment_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    make_model = models.ForeignKey(
        "EquipmentModel",
        db_column="equipment_make_model_id",
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    name = models.CharField(db_column="equipment_name", null=False, max_length=250)
    farm = models.ForeignKey(
        "farm.Farm", db_column="organization_id", null=False, on_delete=models.CASCADE
    )
    serial_num = models.CharField(db_column="serial_num", blank=True, null=True, max_length=250)
    equipment_type = models.ForeignKey(
        "EquipmentType",
        db_column="equipment_type",
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return self.name


class EquipmentMake(models.Model):
    class Meta:
        db_table = "equipment_make"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="equipment_make_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(db_column="equipment_make_name", null=False, max_length=250)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.name


class EquipmentModel(models.Model):
    class Meta:
        db_table = "equipment_make_model"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="equipment_make_model_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    make = models.ForeignKey(
        EquipmentMake,
        db_column="equipment_make_id",
        null=False,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        db_column="equipment_model_name", null=False, max_length=750
    )
    equipment_type = models.ForeignKey(
        "EquipmentType",
        db_column="equipment_type_id",
        null=False,
        on_delete=models.CASCADE,
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return f"{self.make} {self.name}"


class EquipmentType(models.Model):
    class Meta:
        db_table = "equipment_type"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="equipment_type_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        db_column="equipment_type_name", null=False, unique=True, max_length=250
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return self.name


class EquipmentUser(models.Model):
    class Meta:
        db_table = "equipment_user_rel"

    id = models.UUIDField(
        db_column="equipment_user_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    equipment = models.ForeignKey(Equipment, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey("user.ShepherdUser", null=False, on_delete=models.CASCADE)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
