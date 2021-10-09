import uuid

from django.conf import settings
from django.contrib.gis.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class Plan(models.Model):
    class Meta:
        db_table = "organization_plan"
        ordering = ["plan_year", "location", "crop"]

    id = models.UUIDField(
        db_column="plan_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    crop = models.ForeignKey("crop.Crop", null=False, on_delete=models.CASCADE)
    location = models.ForeignKey("field.Location", null=False, on_delete=models.CASCADE)
    planner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE
    )
    plan_year = models.IntegerField(null=False)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):

        return f"{self.plan_year} - {self.location.name} - {self.crop.name}"
