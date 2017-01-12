# -*- encoding:utf-8 -*-

from django.views.generic import TemplateView


class MenuMixin(object):
    def get_context_data(self, **kwargs):
        context = super(MenuMixin, self).get_context_data(**kwargs)
        context["menu"] = self.menu
        return context


class LandingView(TemplateView):
    template_name = "landing.html"

    # def get(self, request, *args, **kwargs):
    #
    #     if request.user and request.user.is_authenticated():
    #         return HttpResponseRedirect(reverse('users:view-dashboard'))
    #     return super(LandingView, self).get(request, *args, **kwargs)

