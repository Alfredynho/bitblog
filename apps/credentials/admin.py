# -*- encoding:utf-8 -*-

from django.contrib import admin

from apps.credentials.models import PlatformApp

#
# @admin.register(PlatformApp)
# class PlatformAppAdmin(admin.ModelAdmin):
#     list_display = ["name", "client_id", "client_secret"]
#
#     class Meta:
#         model = PlatformApp
