# Generated by Django 4.2.14 on 2024-08-01 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("eLearningApp", "0005_appuser_active_courseassignment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appuser",
            name="active",
        ),
        migrations.RemoveField(
            model_name="appuser",
            name="fname",
        ),
        migrations.RemoveField(
            model_name="appuser",
            name="lname",
        ),
    ]
