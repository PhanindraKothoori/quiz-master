# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_exam_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='length',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='exam',
            name='questioncount',
            field=models.IntegerField(default=0),
        ),
    ]