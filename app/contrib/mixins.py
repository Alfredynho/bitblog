# # -*- encoding:utf-8 -*-
import json

import re
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITransactionTestCase

from contrib import codes
from oauth.models import WarpApplication
from users.tests.factories import UserFactory
from rest_framework import status

from oauth2_provider.compat import get_user_model
from oauth2_provider.models import get_application_model, AbstractApplication
Application = get_application_model()
UserModel = get_user_model()


class UsernameValidationMixin(object):

    def validate_username(self, value):
        validator = validators.RegexValidator(re.compile('^[\w.-]+$'), "invalid username", "invalid")

        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Required. 255 characters or fewer. Letters, numbers "
                                              "and /./-/_ characters'")
        return value


class OauthTestCase(APITransactionTestCase):

    DEFAULT_TEST_PASSWORD = "12345678x"

    def config(self):

        self.client = APIClient()

        # App user
        self.user = self.make_user()
        self.username = self.user.username
        self.password = self.DEFAULT_TEST_PASSWORD

        # Web App
        self.app_web = Application(
            user=self.user, client_type=AbstractApplication.CLIENT_PUBLIC,
            name="Testing Web App", category=WarpApplication.CATEGORY_WEB,
        )
        self.app_web.save()

        # Mobile App
        self.app_mobile = Application(
            user=self.user, client_type=AbstractApplication.CLIENT_PUBLIC,
            name="Testing Mobile App", category=WarpApplication.CATEGORY_MOBILE,
        )
        self.app_mobile.save()

        self.application = Application(
            name="test_client_credentials_app",
            user=self.user,
            client_type=AbstractApplication.CLIENT_PUBLIC,
            authorization_grant_type=AbstractApplication.GRANT_PASSWORD,
        )
        self.application.save()

    def make_user(self):
        user = UserFactory.build()
        user.set_password(self.DEFAULT_TEST_PASSWORD)
        user.save()
        return user


    def authenticate(self, token=None, user=None):

        self.client.credentials()
        if token:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        else:
            if user:
                username = user.username
            else:
                username = self.username

            url = reverse('auth:make-token')
            data = dict()
            data["client_id"] = self.application.client_id
            data["client_secret"] = self.application.client_secret
            data["email_or_user"] = username
            data["password"] = self.DEFAULT_TEST_PASSWORD
            data["grant_type"] = "password"

            response = self.client.post(path=url,data=data, format='multipart')
            self.key = json.loads(response.content.decode("utf-8"))
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.key["access_token"])
            self.access_token = self.key["access_token"]

    def assert_warp_response(self, response):
        # print(">>>>\n", response, "<<<<<<\n")
        self.assertEqual("message" in response.data, True)
        self.assertEqual("code" in response.data, True)

    def assert_token_response(self, response):
        self.assertEqual("expires_in" in response.data, True)
        self.assertEqual("access_token" in response.data, True)
        self.assertEqual("scope" in response.data, True)
        self.assertEqual("refresh_token" in response.data, True)
        self.assertEqual("token_type" in response.data, True)

    def assert_missing_arguments(self, url):
        response = self.client.post(path=url,data={},format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_MISSING_ARGUMENTS)
