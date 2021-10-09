import uuid

from django.conf import settings
from django.db import models

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField


class Farm(models.Model):
    class Meta:
        db_table = "organization"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="organization_id", primary_key=True, default=uuid.uuid4, editable=False,
    )
    type = models.ForeignKey(
        "OrganizationType", db_column="organization_type_id", on_delete=models.CASCADE
    )
    name = models.CharField(db_column="organization_name", max_length=750, blank=True, null=True)
    code = models.CharField(
        db_column="organization_code", unique=True, max_length=11, blank=True, null=True
    )
    location = models.ManyToManyField(
        "field.Location", through="OrganizationLocationRel"
    )
    main_location = models.ForeignKey(
        "field.Location",
        db_column="main_location",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="main_farm_location",
    )
    subscription = models.ForeignKey('djstripe.Subscription', null=True, blank=True, on_delete=models.SET_NULL, help_text="The team's Stripe Subscription object, if it exists.")
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return self.name


class OrganizationTypeRel(models.Model):
    class Meta:
        db_table = "organization_type_rel"

    id = models.UUIDField(
        db_column="organization_type_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    farm = models.ForeignKey("Farm", blank=False, on_delete=models.CASCADE)
    farm_type = models.ForeignKey(
        "OrganizationType", blank=False, on_delete=models.CASCADE
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return f"{self.farm} {self.farm_type}"


class FarmUsers(models.Model):
    class Meta:
        db_table = "organization_users"

    id = models.UUIDField(
        db_column="organization_user_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="user_id",
        blank=False,
        on_delete=models.CASCADE,
        related_name="farm_members",
    )
    farm = models.ForeignKey(
        "Farm",
        db_column="organization_id",
        blank=False,
        on_delete=models.CASCADE,
        related_name="member_farms",
    )
    role = models.ForeignKey(
        "OrganizationRole", db_column="organization_role_id", on_delete=models.CASCADE
    )
    default_farm = models.BooleanField(db_column="default_organization", default=False)
    customer = models.ForeignKey('djstripe.Customer', null=True, blank=True, on_delete=models.SET_NULL, help_text="The member's Stripe Customer object for this team, if it exists.")
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()


class OrganizationLocationRel(models.Model):
    class Meta:
        db_table = "organization_location_rel"

    id = models.UUIDField(
        db_column="organization_location_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    farm = models.ForeignKey(
        "Farm",
        db_column="organization_id",
        blank=False,
        on_delete=models.CASCADE,
        related_name="farm_locations",
    )
    location = models.ForeignKey(
        "field.Location",
        db_column="location_id",
        blank=False,
        on_delete=models.CASCADE,
        related_name="location_farms",
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()


class OrganizationRel(models.Model):
    class Meta:
        db_table = "organization_rel"

    id = models.UUIDField(
        db_column="organization_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    parent_farm = models.ForeignKey(
        "Farm",
        db_column="parent_organization_id",
        on_delete=models.CASCADE,
        related_name="parent_farm",
    )
    child_farm = models.ForeignKey(
        "Farm",
        db_column="child_organization_id",
        on_delete=models.CASCADE,
        related_name="child_farm",
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()


class OrganizationRole(models.Model):
    class Meta:
        db_table = "organization_role"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="organization_role_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        db_column="organization_role_name", unique=True, blank=False, max_length=250
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return self.name


class OrganizationType(models.Model):
    class Meta:
        db_table = "organization_type"
        ordering = ["name"]

    id = models.UUIDField(
        db_column="organization_type_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        db_column="organization_type_name", unique=True, max_length=250
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return self.name


class OrganizationTypeLocationTypeRel(models.Model):
    class Meta:
        db_table = "organization_type_location_type_rel"

    id = models.UUIDField(
        db_column="organization_type_location_type_rel_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    farm_type = models.ForeignKey(
        "OrganizationType",
        db_column="organization_type_id",
        blank=False,
        on_delete=models.CASCADE,
    )
    location_type = models.ForeignKey(
        "field.LocationType",
        db_column="location_type_id",
        blank=False,
        on_delete=models.CASCADE,
    )
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return f"{self.farm_type} - {self.location_type}"
