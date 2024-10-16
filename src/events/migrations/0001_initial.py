# Generated by Django 5.0.3 on 2024-03-23 23:21

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("canceled", "Canceled"),
                            ("completed", "Completed"),
                            ("created", "Created"),
                            ("ongoing", "Ongoing"),
                        ],
                        default="created",
                        max_length=25,
                    ),
                ),
                ("location", models.CharField(db_index=True, max_length=255)),
                ("capacity", models.BigIntegerField()),
                ("description", models.TextField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                "verbose_name": "event",
                "verbose_name_plural": "events",
            },
        ),
        migrations.CreateModel(
            name="EventAttendance",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "attendance",
                "verbose_name_plural": "attendances",
            },
        ),
        migrations.CreateModel(
            name="EventCategory",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
        ),
    ]
