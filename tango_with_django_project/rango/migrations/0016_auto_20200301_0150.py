# Generated by Django 2.2.3 on 2020-03-01 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0015_auto_20200229_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='password',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=10000),
        ),
    ]