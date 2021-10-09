import uuid

from django.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class Crop(models.Model):
    class Meta:
        db_table = "crop_type"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="crop_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(db_column="crop_name", max_length=75)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    deleted_by = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.name
