# Generated by Django 4.2.14 on 2024-08-07 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eLearningApp", "0010_chat"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(db_index=True, max_length=100)),
                ("file", models.FileField(upload_to="")),
            ],
        ),
    ]
