# Generated by Django 3.0.8 on 2020-11-18 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_product_minstockclient'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
