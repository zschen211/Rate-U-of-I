# Generated by Django 3.0.8 on 2020-07-29 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_friend_current_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friend',
            old_name='friend',
            new_name='users',
        ),
    ]
