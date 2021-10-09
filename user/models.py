import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_extensions.db.models import CreationDateTimeField, ModificationDateTimeField

from timezone_field import TimeZoneField


class ShepherdUser(AbstractUser):
    class Meta:
        db_table = "shepherd_user"
        ordering = ["last_name", "first_name"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=75, blank=False)
    current_points = models.IntegerField(default=0)
    lifetime_points = models.IntegerField(default=0)
    onboard_complete = models.BooleanField(default=False)
    profile_image = models.ImageField(db_column="profile_image", upload_to="profile_images/", max_length="150")
    stripe_customer_id = models.CharField(max_length=255, null=True)
    stripe_subscription_id = models.CharField(max_length=255, null=True)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
    timezone = TimeZoneField(choices_display="WITH_GMT_OFFSET")

    def __str__(self):

        return f"{self.first_name} {self.last_name}"


class UserValidations(models.Model):
    class Meta:
        db_table = "shepherd_user_validations"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        blank=False,
        on_delete=models.CASCADE,
        related_name="user_validations",
        primary_key=True,
    )
    activation_key = models.CharField(max_length=255, default=1)
    password_reset_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)
    first_login = models.BooleanField(default=False)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=ShepherdUser)
def update_user_validations(sender, instance, created, **kwargs):
    if created:
        UserValidations.objects.create(
            user=instance,
            created_by=instance.created_by,
            modified_by=instance.modified_by,
        )


class UserCertifications(models.Model):
    class Meta:
        db_table = "shepherd_user_certifications"

    id = models.UUIDField(
        db_column="shepherd_user_certification_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    cert_name = models.CharField(max_length=250, blank=False)
    cert_body = models.CharField(max_length=250, blank=False)
    cert_id = models.CharField(max_length=100, blank=False)
    cert_body_site = models.CharField(max_length=250, blank=True, null=True)
    cert_image = models.CharField(max_length=750, blank=True, null=True)
    cert_date = models.DateField(blank=True, null=True)
    cert_expire_date = models.DateField(blank=True, null=True)
    cert_user = models.ForeignKey("ShepherdUser", blank=False, on_delete=models.CASCADE)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()


class UserPointActivity(models.Model):
    class Meta:
        db_table = "shepherd_user_point_activity"

    id = models.UUIDField(
        db_column="shepherd_user_point_activity_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey("ShepherdUser", blank=False, on_delete=models.CASCADE)
    point_activity = models.ForeignKey(
        "PointActivityType", blank=False, on_delete=models.CASCADE
    )
    points_earned_spent = models.IntegerField(blank=False)
    activity_date = models.DateTimeField()
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()


class PointActivityType(models.Model):
    class Meta:
        db_table = "point_activity_type"

    id = models.UUIDField(
        db_column="point_activity_type_id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    point_activity_name = models.CharField(max_length=250, blank=False, unique=True)
    point_activity_description = models.TextField()
    default_point_value = models.IntegerField(default=0)
    max_times_earnable = models.IntegerField(default=0)
    available_from_date = models.DateTimeField()
    available_to_date = models.DateTimeField()
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()


class PointLevels(models.Model):
    class Meta:
        db_table = "point_levels"

    id = models.UUIDField(
        db_column="point_level_id", primary_key=True, default=uuid.uuid4, editable=False
    )
    point_level_name = models.CharField(max_length=250, blank=False, unique=True)
    points_required = models.IntegerField(blank=False, unique=True)
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()
