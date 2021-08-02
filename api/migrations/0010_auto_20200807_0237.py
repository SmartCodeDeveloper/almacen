# Generated by Django 3.0.8 on 2020-08-07 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_order_date_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Employee'),
        ),
    ]
