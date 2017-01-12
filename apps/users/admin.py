# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.utils.translation import ugettext_lazy as _

from .models import User, UserAction


class UserChangeForm(UserChangeFormBase):

    class Meta(UserChangeFormBase.Meta):
        model = User


class UserCreationForm(UserCreationFormBase):
    email = forms.EmailField(
        label=_("Email"),
    )

    error_message = UserCreationFormBase.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationFormBase.Meta):
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
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'photo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'full',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ("type", "user", "creation_date", "expiration_date", )
    list_filter = ("type", )

    class Meta:
        model = UserAction
