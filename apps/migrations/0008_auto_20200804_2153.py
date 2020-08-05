# Generated by Django 3.0.8 on 2020-08-05 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_auto_20200731_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='placeID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='apps.Place'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='userID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='apps.User'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='placeID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='apps.Place'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='userID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='apps.User'),
        ),
    ]
