# Generated by Django 3.1.2 on 2020-10-19 16:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Crop",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_column="crop_id",
                        default=uuid.UUID("4457f10f-45c4-45bc-9810-d7a822463172"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(db_column="crop_name", max_length=75)),
            ],
            options={
                "db_table": "crop_type",
            },
        ),
    ]
