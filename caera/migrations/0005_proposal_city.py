# Generated by Django 5.2.1 on 2025-06-01 12:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("caera", "0004_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="proposal",
            name="city",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="caera.city"
            ),
            preserve_default=False,
        ),
    ]
