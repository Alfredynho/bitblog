# -*- encoding:utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django import forms
from django.shortcuts import redirect, render
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

class UserUpdateForm(forms.ModelForm):
    #
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     try:
    #         user = User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return username
    #     raise forms.ValidationError(u'%s already exists' % username)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'photo']


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm


    def get(self, request, *args, **kwargs):
        import ipdb;ipdb.set_trace()

    def post(self, request, *args, **kwargs):
        import ipdb;ipdb.set_trace()
    #     user =  request.user
    #     form = UserUpdateForm(instance=user)

    def get_success_url(self):
        return reverse('users:profile')

    def get_object(self):
        return self.request.user


class MenuMixin(object):
    def get_context_data(self, **kwargs):
        context = super(MenuMixin, self).get_context_data(**kwargs)
        context["menu"] = self.menu
        return context

# NEW VIEWS --------------------------------------------------------


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "users/profile.html"
    menu = "profile"

    def post(self, request, *args, **kwargs):
        user = request.user
        form =  UserUpdateForm(instance=user, data=request.POST, files=request.FILES)
        # import ipdb; ipdb.set_trace()

        if form.is_valid():
            form.save(commit=True)
            return redirect("users:view-profile")
        else:
            return render(request, template_name=self.template_name, context={"form": form})


    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if self.request and self.request.user.is_authenticated():
            context["user"] = self.request.user
        else:
            context["user"] = None

        context["menu"] = self.menu
        return context



class ProfileSessionsView(ProfileView):
    template_name = "users/sessions.html"
    menu = "sessions"


class DashboardView(LoginRequiredMixin, MenuMixin, TemplateView):
    template_name = "management/dashboard.html"
    menu = "dashboard"


class SettingsView(LoginRequiredMixin, MenuMixin, TemplateView):
    template_name = "management/settings.html"
    menu = "settings"

