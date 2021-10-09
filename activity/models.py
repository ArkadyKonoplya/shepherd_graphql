import uuid

from django.conf import settings
from django.contrib.gis.db import models
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class BaseActivity(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(db_column="activity_type_name", unique=True, max_length=250)
    requires_crop = models.BooleanField(default=False)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)


class Activity(BaseActivity):
    class Meta:
        db_table = "activity_type"
        ordering = ("sort_order",)

    id = models.UUIDField(
        db_column="activity_type_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    sort_order = models.IntegerField()

    def __str__(self):
        return self.name


class CropTypeActivityType(models.Model):
    class Meta:
        db_table = "crop_type_activity_type"

    id = models.UUIDField(
        db_column="crop_type_activity_type_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    crop = models.ForeignKey("crop.Crop", db_column="crop_type_id", on_delete=models.DO_NOTHING, related_name="activity_crops")
    activity = models.ForeignKey("Activity", db_column="activity_type_id", on_delete=models.DO_NOTHING, related_name="crop_activities")
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)


class CustomActivity(BaseActivity):
    class Meta:
        db_table = "organization_custom_activity_type"

    id = models.UUIDField(
        db_column="organization_custom_activity_type",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    farm = models.ForeignKey("farm.Farm", db_column="organization_id", on_delete=models.DO_NOTHING, related_name="custom_activity_farm")


class ActivityDetail(models.Model):
    class Meta:
        db_table = "activity_detail"

    id = models.UUIDField(
        db_column="activity_detail_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        db_column="activity_detail_name", max_length=250, unique=True
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.name


class ActivityDetailRel(models.Model):
    class Meta:
        db_table = "activity_type_detail_rel"

    id = models.UUIDField(
        db_column="activity_type_detail_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    activity = models.ForeignKey(
        "Activity", db_column="activity_type_id", null=False, on_delete=models.CASCADE
    )
    activity_detail = models.ForeignKey(
        "ActivityDetail", null=False, on_delete=models.CASCADE
    )
    sort_order = models.IntegerField()
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return f"{self.activity} - {self.activity_detail}"


class FarmTypeActivityRel(models.Model):
    class Meta:
        db_table = "organization_type_activity_rel"

    id = models.UUIDField(
        db_column="organization_type_activity_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    farm_type = models.ForeignKey(
        "farm.OrganizationType",
        null=False,
        db_column="organization_type_id",
        on_delete=models.CASCADE,
    )
    activity_type = models.ForeignKey(
        "activity.Activity", null=False, on_delete=models.CASCADE
    )
    sort_order = models.IntegerField(
        db_column="activity_sort_order", null=False, default=0
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return f"{self.farm_type} - {self.activity_type}"


class LocationTypeActivityType(models.Model):
    class Meta:
        db_table = "location_type_activity_type_rel"

    id = models.UUIDField(
        db_column="location_type_activity_type_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    location_type = models.ForeignKey(
        "field.LocationType", null=False, on_delete=models.CASCADE
    )
    activity_type = models.ForeignKey(
        "activity.Activity", null=False, on_delete=models.CASCADE
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return f"{self.location_type} - {self.activity_type}"