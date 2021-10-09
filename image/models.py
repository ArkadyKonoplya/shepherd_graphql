import uuid

from django.conf import settings
from django.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class BackgroundImage(models.Model):
    class Meta:
        db_table = "background_image"
        ordering = ["filename"]

    id = models.UUIDField(
        db_column="background_image_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    description = models.TextField(db_column="image_description", blank=True, null=True)
    filename = models.CharField(db_column="image_filename", max_length=750, null=False)
    image_approved = models.BooleanField(default=False)
    image_for_day = models.IntegerField(blank=True, null=True)
    image_previously_used = models.BooleanField(default=False)
    image_submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return f"{self.filename} - {self.description}"
