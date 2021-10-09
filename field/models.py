import uuid

from django.contrib.gis.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class Location(models.Model):
    class Meta:
        db_table = "location"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="location_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(db_column="location_name", null=False, max_length=750)
    type = models.ForeignKey(
        "LocationType",
        db_column="location_type_id",
        null=False,
        on_delete=models.CASCADE,
    )
    acres = models.FloatField()
    image = models.CharField(db_column="location_image", max_length=750)
    geo_center = models.PointField(
        db_column="location_geo_center", null=False, srid=4326
    )
    drawn_area = models.PolygonField(
        db_column="location_drawn_area", null=False, srid=4326
    )
    legal_name = models.CharField(blank=True, null=True, max_length=750)
    organization = models.ManyToManyField(
        "farm.Farm",
        through="farm.OrganizationLocationRel",
        related_name="location_organizations",
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.geo_center = self.drawn_area.centroid
        super().save(*args, **kwargs)


class LocationType(models.Model):
    class Meta:
        db_table = "location_type"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="location_type_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        db_column="location_type_name", unique=True, null=False, max_length=250
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return self.name
