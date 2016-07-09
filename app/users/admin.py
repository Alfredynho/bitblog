# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import User, UserAction


class OwnUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User


class OwnUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
    )

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    form = OwnUserChangeForm
    add_form = OwnUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'photo', 'phone', 'bio')}),
        (_('Social'), {'fields': ('twitter', 'facebook', 'instagram', 'github')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide','full',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ("type", "user", "creation_date", "expiration_date", )
    list_filter = ("type", )

    class Meta:
        model = UserAction