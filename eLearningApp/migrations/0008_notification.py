# Generated by Django 4.2.14 on 2024-08-02 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("eLearningApp", "0007_alter_courseenrollment_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("message", models.TextField()),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "receiving_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]