# -*- encoding:utf-8 -*-

from urllib.request import urlopen
import hashlib

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def new_user(self, request):
        return super(AccountAdapter, self).new_user(request)

    def populate_username(self, request, user):
        return super(AccountAdapter, self).populate_username(request, user)

    def confirm_email(self, request, email_address):
        return super(AccountAdapter, self).confirm_email(request, email_address)

    def generate_unique_username(self, txts, regex=None):
        return super(AccountAdapter, self).generate_unique_username(txts, regex)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def new_user(self, request, sociallogin):
        return super(SocialAccountAdapter, self).new_user(request, sociallogin)

    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
        avatar_size = 256
        picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
            hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
            avatar_size
        )

        if sociallogin.account.provider == 'facebook':
            f_name = sociallogin.account.extra_data['first_name']
            l_name = sociallogin.account.extra_data['last_name']
            if f_name:
                user.first_name = f_name
            if l_name:
                user.last_name = l_name

            # verified = sociallogin.account.extra_data['verified']

            picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
                sociallogin.account.uid, avatar_size)

        image_url = picture_url
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()
        user.photo.save("photo_user_%s.png" % user.pk, File(img_temp))
        user.save()

        return user

    def populate_user(self, request, sociallogin, data):
        return super(SocialAccountAdapter, self).populate_user(request, sociallogin, data)


