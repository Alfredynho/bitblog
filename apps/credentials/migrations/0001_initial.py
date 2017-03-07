# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-12 07:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oauth2_provider.generators
import oauth2_provider.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(db_index=True, default=oauth2_provider.generators.generate_client_id, max_length=100, unique=True)),
                ('redirect_uris', models.TextField(blank=True, help_text='Allowed URIs list, space separated', validators=[oauth2_provider.validators.validate_uris])),
                ('client_type', models.CharField(choices=[('confidential', 'Confidential'), ('public', 'Public')], max_length=32)),
                ('authorization_grant_type', models.CharField(choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials')], max_length=32)),
                ('client_secret', models.CharField(blank=True, db_index=True, default=oauth2_provider.generators.generate_client_secret, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('skip_authorization', models.BooleanField(default=False)),
                ('has_confirmation', models.BooleanField(default=False, help_text='Marca este campo  si quieres que esta aplicación envíe una confirmación por correo antes de activar una cuenta', verbose_name='Confirmación en el Registro')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Logo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credentials_platformapp', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Aplicación',
                'verbose_name_plural': 'Aplicaciones',
            },
        ),
    ]