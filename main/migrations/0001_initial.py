# Generated by Django 5.1.6 on 2025-02-15 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CategoryModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("title", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="ItemModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("title", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.categorymodel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Item",
                "verbose_name_plural": "Items",
                "unique_together": {("slug", "category")},
            },
        ),
        migrations.CreateModel(
            name="LinkModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("url", models.URLField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("working", "Working"),
                            ("not_verified", "Not Verified"),
                            ("not_working", "Not Working"),
                        ],
                        default="not_verified",
                        max_length=255,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.itemmodel"
                    ),
                ),
            ],
            options={
                "verbose_name": "Link",
                "verbose_name_plural": "Links",
            },
        ),
        migrations.CreateModel(
            name="LinkClickModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "link",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.linkmodel"
                    ),
                ),
            ],
            options={
                "verbose_name": "Link Click",
                "verbose_name_plural": "Link Clicks",
            },
        ),
        migrations.CreateModel(
            name="LinkActionModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("working", "Working"),
                            ("not_working", "Not Working"),
                            ("spam", "Spam"),
                        ],
                        max_length=255,
                    ),
                ),
                ("ip_address", models.GenericIPAddressField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "link",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.linkmodel"
                    ),
                ),
            ],
            options={
                "verbose_name": "Link Action",
                "verbose_name_plural": "Link Actions",
            },
        ),
    ]
