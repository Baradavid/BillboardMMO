# Generated by Django 4.2 on 2023-05-02 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0003_category_subscribers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_name',
        ),
    ]
