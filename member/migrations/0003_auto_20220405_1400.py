# Generated by Django 2.2 on 2022-04-05 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20220322_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='lon',
            field=models.FloatField(null=True),
        ),
    ]