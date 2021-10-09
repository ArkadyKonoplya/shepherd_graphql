# Generated by Django 3.1.2 on 2020-10-19 16:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("crop", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Farm",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="organization_id",
                        default=uuid.UUID("1d96d874-5ed7-4ff0-99c0-8ae847661b3e"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_column="organization_name", max_length=750, null=True
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        db_column="organization_code",
                        max_length=11,
                        null=True,
                        unique=True,
                    ),
                ),
            ],
            options={
                "db_table": "organization",
            },
        ),
        migrations.CreateModel(
            name="FarmType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="organization_type_rel_id",
                        default=uuid.UUID("1a0f1f3f-f065-48df-8fbe-583fadaa35b7"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
            options={
                "db_table": "organization_type_rel",
            },
        ),
        migrations.CreateModel(
            name="FarmUsers",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="organization_user_id",
                        default=uuid.UUID("fc904d54-c3b2-4560-ab1e-44d1d0f950f9"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
            options={
                "db_table": "organization_users",
            },
        ),
        migrations.CreateModel(
            name="OrganizationLocationRel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="organization_location_rel_id",
                        default=uuid.UUID("da8241a5-0dd9-4d0a-aca3-e3bb040b0ef9"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
            options={
                "db_table": "organization_location_rel",
            },
        ),
        migrations.CreateModel(
            name="OrganizationRole",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="organization_role_id",
                        default=uuid.UUID("6d7a195d-bb0a-46dd-9244-31e02ba396b2"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_column="organization_role_name", max_length=250, unique=True
                    ),
                ),
            ],
            options={
                "db_table": "organization_role",
            },
        ),
        migrations.CreateModel(
            name="OrganizationType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="organization_type_id",
                        default=uuid.UUID("da526428-dec9-4b43-9f98-55f6fdbdbe2f"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_column="organization_type_name", max_length=250, unique=True
                    ),
                ),
            ],
            options={
                "db_table": "organization_type",
            },
        ),
        migrations.CreateModel(
            name="OrganizationTypeActivityRel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="organization_type_activity_rel_id",
                        default=uuid.UUID("63af445f-c7da-412e-a898-579a8bd52d75"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(db_column="activity_sort_order", default=0),
                ),
            ],
            options={
                "db_table": "organization_type_activity_rel",
            },
        ),
        migrations.CreateModel(
            name="OrganizationTypeLocationTypeRel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="organization_type_location_type_rel_id",
                        default=uuid.UUID("b18bace1-34dc-4620-8830-c9335a6ff7bd"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
            options={
                "db_table": "organization_type_location_type_rel",
            },
        ),
        migrations.CreateModel(
            name="Plan",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="plan_id",
                        default=uuid.UUID("a0e8e356-e1bf-43cb-acad-33f1a840d826"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("plan_year", models.IntegerField()),
                (
                    "crop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="crop.crop"
                    ),
                ),
            ],
            options={
                "db_table": "organization_plan",
            },
        ),
    ]