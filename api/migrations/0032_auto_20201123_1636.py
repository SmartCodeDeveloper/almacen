# Generated by Django 3.0.8 on 2020-11-23 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20201123_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='manifest',
            name='delivery',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='manifest',
            name='receive',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
