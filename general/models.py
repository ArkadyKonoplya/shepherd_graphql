import uuid

from django.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class Acknowledgements(models.Model):
    class Meta:

        db_table = "acknowledgements"

    id = models.UUIDField(
        db_column="acknowledgement_id",
        null=False,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    acknowledgement = models.TextField(null=False)
    display_acknowledgement = models.BooleanField(default=True)
    acknowledgement_order = models.IntegerField(null=False)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.UUIDField(null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):

        return self.acknowledgement
