import operator
import re
from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template import Context
from django.template.loader import get_template
from django.views.generic.edit import FormView

from tapioca.exceptions import ClientError
from tapioca_disqus import Disqus

from django.http import Http404, HttpResponse, request
from django.views.generic import View
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Site

from .models import EntryPage


class EntryPageServe(View):
    """
    This class is responsible to serve entries with a proper blog url format:
    http://wwww.example.com/2015/10/01/my-first-post

    If you set your blog as Wagtail Root page, the url is like the above example.
    Otherwise if you have a multiple blog instances, you need to pass the slug of the blog
    page instance that you want to use:
    http://wwww.example.com/weblog/2015/10/01/my-first-post
    http://wwww.example.com/videblog/2015/10/01/my-first-video
    """

    def get(self, request, *args, **kwargs):
        if not request.site:
            raise Http404
        if request.resolver_match.url_name == 'entry_page_serve_slug':
            path_components = list(operator.itemgetter(0, -1)(request.path.strip('/').split('/')))
        else:
            path_components = [request.path.strip('/').split('/')[-1]]
        page, args, kwargs = request.site.root_page.specific.route(request, path_components)

        for fn in hooks.get_hooks('before_serve_page'):
            result = fn(page, request, args, kwargs)
            if isinstance(result, HttpResponse):
                return result
        return page.serve(request, *args, **kwargs)


class EntryPageUpdateCommentsView(View):

    def post(self, request, entry_page_id, *args, **kwargs):
        try:
            entry_page = EntryPage.objects.get(pk=entry_page_id)
            blog_page = entry_page.blog_page
            disqus_client = Disqus(api_secret=blog_page.disqus_api_secret)
            try:
                params = {'forum': blog_page.disqus_shortname, 'thread': 'ident:{}'.format(entry_page_id)}
                thread = disqus_client.threads_details().get(params=params)
                entry_page.num_comments = thread.response.posts().data()
                entry_page.save()
                return HttpResponse()
            except ClientError:
                raise Http404
        except EntryPage.DoesNotExist:
            raise Http404

class InjectOwnerMixin(object):

    def get_site_domain(self, request):

        dd = request.META['HTTP_HOST']
        pat = r'(?P<domain>.*):.*'
        m = re.match(pat, dd)
        return m.group('domain')

    def get_root_from_domain(self, domain):
        es = Site.objects.filter(hostname__contains=domain).exists()
        if es:
            es = Site.objects.filter(hostname__contains=domain).first()
            return es.root_page
        return None

    def get_context_data(self, **kwargs):

        context = super(InjectOwnerMixin, self).get_context_data(**kwargs)

        context['domain'] = self.get_site_domain(self.request)
        root_page = self.get_root_from_domain(context['domain'])

        if root_page:
            context['blog_page'] = root_page
        return context


class PortfolioPage(InjectOwnerMixin, TemplateView):
    template_name = "blog/portfolio_page.html"


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

class ContactPage(InjectOwnerMixin, FormView):
    template_name = "blog/contact_page.html"
    form_class = ContactForm
    success_url = '/contact/thanks/'

    def form_valid(self, form):
        name = self.request.POST.get('name', '')
        email = self.request.POST.get('email', '')
        subject = self.request.POST.get('subject', '')
        message = self.request.POST.get('message', '')

        # Email the profile with the
        # contact information
        template = get_template('blog/partials/contact_template.txt')

        context = Context({
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        })
        content = template.render(context)

        to_email = settings.BLOG_ADMIN_EMAIL
        blog_owner = self.get_root_from_domain(self.get_site_domain(self.request)).owner
        if blog_owner and blog_owner.email:
            to_email = blog_owner.email




        email_message = EmailMessage(
            subject=_("New contact form submission"),
            body=content,
            from_email=email,
            to=[to_email],
        )

        # import ipdb; ipdb.set_trace()

        email_message.send()
        return super(ContactPage, self).form_valid(form)

class ContactSuccessPage(InjectOwnerMixin, TemplateView):
    template_name = 'blog/contact_thanks.html'