import uuid

from django.conf import settings
from django.contrib.gis.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField
from martor.models import MartorField


class Message(models.Model):
    class Meta:
        db_table = "task_message"

    id = models.UUIDField(
        db_column="message_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="message_recipient",
        null=False,
        on_delete=models.CASCADE,
        related_name="message_recipient_user",
    )
    farm = models.ForeignKey(
        "farm.Farm", db_column="organization_id", null=False, on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="message_sender",
        null=False,
        on_delete=models.CASCADE,
        related_name="message_sender_user",
    )
    task = models.ForeignKey(
        "Task", db_column="task_id", null=False, on_delete=models.CASCADE
    )
    message_year = models.IntegerField(null=False)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    message = MartorField(db_column="task_message", blank=True, null=True)
    message_location = models.PointField(blank=True, null=True)
    message_image = models.CharField(max_length=750, blank=True, null=True)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.message


class TaskHistory(models.Model):
    class Meta:
        db_table = "task_history"

    id = models.UUIDField(
        db_column="task_history_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    task_id = models.ForeignKey(
        "Task",
        db_column="task_id",
        on_delete=models.DO_NOTHING,
        related_name="task_history",
    )
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_column="user_update_id", on_delete=models.CASCADE, related_name="historical_update_user"
    )
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_column="assigned_user_id", on_delete=models.CASCADE, related_name="historical_assigned_user", blank=True, null=True
    )
    status_date_change = models.DateTimeField()
    status_change_location = models.PointField(blank=True, null=True)
    task_status = models.ForeignKey(
        "TaskStatus", db_column="task_status_id", on_delete=models.CASCADE
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)


class Task(models.Model):
    class Meta:
        db_table = "task"

    id = models.UUIDField(
        db_column="task_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    task_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="task_creator_id",
        null=False,
        on_delete=models.CASCADE,
        related_name="task_creator_user",
    )
    task_activity = models.ForeignKey("activity.Activity", db_column="task_activity_id", null=False, on_delete=models.DO_NOTHING)
    task_custom_activity = models.ForeignKey("activity.CustomActivity", db_column="task_custom_activity_id", null=True, on_delete=models.DO_NOTHING, default=None)
    task_start_date = models.DateTimeField()
    task_end_date = models.DateTimeField()
    task_status = models.ForeignKey(
        "TaskStatus", db_column="task_status_id", on_delete=models.CASCADE
    )
    task_notes = MartorField(blank=True, null=True)
    task_assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="task_assignee_id",
        null=True,
        on_delete=models.CASCADE,
        related_name="task_assignee_user",
    )
    task_amount = models.FloatField(blank=True, null=True)
    task_verification_image = models.CharField(max_length=750, blank=True, null=True)
    is_draft = models.BooleanField(default=False)
    task_available_date = models.DateTimeField(blank=True, null=True)
    detail = models.ManyToManyField("activity.ActivityDetail", through="TaskDetails")
    equipment = models.ManyToManyField("equipment.Equipment", through="TaskEquipment")
    task_plan = models.ForeignKey(
        "plan.Plan", db_column="task_plan_id", on_delete=models.CASCADE, related_name="plan_tasks"
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_activity_name(self):
        """
        Since custom activites are in a separate table, need a custom function to try to get the activity first, custom activity second.
        :return:
        """
        from activity.models import Activity, CustomActivity

        try:
            activity = Activity.objects.get(pk=self.task_activity)
            return activity.name
        except:
            activity = CustomActivity.objects.get(pk=self.task_activity)
            return activity.name
        else:
            return "Unknown Activity"


class TaskDetails(models.Model):
    class Meta:
        db_table = "task_details"

    id = models.UUIDField(
        db_column="task_detail_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    activity_detail = models.ForeignKey(
        "activity.ActivityDetail",
        null=False,
        on_delete=models.CASCADE,
        related_name="task_activity_detail",
    )
    detail_value = models.CharField(db_column="activity_detail_value", max_length=250)
    task = models.ForeignKey(
        "Task", null=False, on_delete=models.CASCADE, related_name="detail_tasks"
    )
    detail_set_num = models.IntegerField()
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return f"{self.task.id} - {self.activity_detail} {self.detail_value}"


class TaskEquipment(models.Model):
    class Meta:
        db_table = "task_equipment"

    id = models.UUIDField(
        db_column="task_equipment_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    task = models.ForeignKey(
        "Task", null=False, on_delete=models.CASCADE, related_name="equipment_task"
    )
    equipment = models.ForeignKey(
        "equipment.Equipment",
        null=False,
        on_delete=models.CASCADE,
        related_name="task_equipment",
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)


class TaskStatus(models.Model):
    class Meta:
        db_table = "task_status_type"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="task_status_type_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(db_column="task_status_name", max_length=75)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.name

