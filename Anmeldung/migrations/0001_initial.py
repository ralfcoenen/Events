# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('bezeichnung', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Teilnehmer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('vorname', models.CharField(max_length=40)),
                ('strasse', models.CharField(max_length=60)),
                ('plz', models.CharField(max_length=8)),
                ('ort', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('event', models.ForeignKey(to='Anmeldung.Event')),
            ],
        ),
    ]
