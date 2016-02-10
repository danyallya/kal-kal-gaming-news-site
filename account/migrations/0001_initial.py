# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True)),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('birth_date', models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')),
                ('code', models.CharField(null=True, max_length=200, blank=True, verbose_name='کد فراموشی گذرواژه')),
                ('gender', models.CharField(max_length=50, verbose_name='جنسیت', choices=[('1', 'مذکر'), ('2', 'مؤنث')], default='')),
                ('mobile', models.CharField(validators=[django.core.validators.RegexValidator(message='شماره تماس اشتباه است', regex='^\\d{11}$', code='invalid_mobile')], max_length=15, blank=True, verbose_name='شماره تماس', null=True)),
                ('activation_code', models.CharField(null=True, max_length=200, blank=True, verbose_name='کد فعال سازی')),
                ('activation_date', models.DateTimeField(null=True, blank=True, verbose_name='تاریخ فعال سازی')),
                ('last_day_message', models.DateField(null=True, blank=True, verbose_name='آخرین تاریخ پیغام دادن')),
                ('activated', models.BooleanField(verbose_name='فعال شده', default=True)),
                ('level', models.IntegerField(verbose_name='سطح', default=3)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group', related_name='user_set', blank=True, verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission', related_name='user_set', blank=True, verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
