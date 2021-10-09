import uuid

from django.contrib.gis.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class WorkOrder(models.Model):
    class Meta:
        db_table = "work_order"

    id = models.UUIDField(
        db_column="work_order_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    work_order_name = models.CharField(max_length=750, blank=True, null=True)
    activity = models.ForeignKey("activity.Activity", null=False, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    available_date = models.DateTimeField()
    farm = models.ForeignKey(
        "farm.Farm", db_column="farm_id", blank=False, on_delete=models.DO_NOTHING
    )
    tasks_completed = models.IntegerField(default=0, blank=True)
    total_tasks = models.IntegerField(blank=True, null=True)
    work_order_status = models.ForeignKey("WorkOrderStatus", db_column="work_order_status", null=False, on_delete=models.DO_NOTHING, related_name="work_order_status")
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)


class WorkOrderStatus(models.Model):
    class Meta:
        db_table = "work_order_status_type"

    id = models.UUIDField(
        db_column="work_order_status_type_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(db_column="work_order_status_name", max_length=75)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.name


class WorkOrderTaskRel(models.Model):
    class Meta:
        db_table = "work_order_task_rel"

    id = models.UUIDField(
        db_column="work_order_task_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    work_order = models.ForeignKey(
        "WorkOrder",
        db_column="work_order_id",
        null=False,
        on_delete=models.CASCADE,
        related_name="task_work_orders",
    )
    task = models.ForeignKey(
        "task.Task",
        db_column="task_id",
        null=False,
        on_delete=models.CASCADE,
        related_name="work_order_tasks",
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)


class WorkOrderEquipmentRel(models.Model):
    class Meta:
        db_table = "work_order_equipment_rel"

    id = models.UUIDField(
        db_column="work_order_equipment_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    work_order = models.ForeignKey(
        "WorkOrder", db_column="work_order_id", null=False, on_delete=models.DO_NOTHING
    )
    equipment = models.ForeignKey(
        "equipment.Equipment",
        db_column="equipment_id",
        null=False,
        on_delete=models.DO_NOTHING,
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
