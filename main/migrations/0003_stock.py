# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170321_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('my_product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Product')),
            ],
        ),
    ]
