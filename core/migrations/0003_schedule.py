# Generated by Django 2.0.2 on 2018-03-03 10:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_medication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('week', 'Week'), ('day', 'Day'), ('hour', 'Hour'), ('minute', 'Minute'), ('second', 'Second'), ('once', 'Once')], max_length=6)),
                ('day', models.CharField(blank=True, choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], max_length=3)),
                ('time', models.CharField(blank=True, max_length=5, validators=[django.core.validators.RegexValidator(message='HH:MM format', regex='^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')])),
                ('counter', models.IntegerField(blank=True)),
                ('module_nums', models.CharField(max_length=250, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Module Number(s)')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
