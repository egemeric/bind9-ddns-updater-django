# Generated by Django 3.1 on 2020-08-13 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddns_updater', '0006_auto_20200810_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='Client_LAST_ACCESS',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]