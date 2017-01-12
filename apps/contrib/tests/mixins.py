# # -*- encoding:utf-8 -*-
import json



from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.test import APIClient, APITransactionTestCase

from oauth2_provider.compat import get_user_model
from oauth2_provider.models import get_application_model, AbstractApplication

from apps.users.tests.factories import UserFactory

Application = get_application_model()
UserModel = get_user_model()


class OauthTestCase(APITransactionTestCase):

    DEFAULT_TEST_PASSWORD = "KhuDmZ2zMUcRhjaqocyxfPht"

    def config(self):

        self.client = APIClient()

        # Testing User
        self.user = self.make_user()
        self.username = self.user.username
        self.password = self.DEFAULT_TEST_PASSWORD

        # Testing App
        self.app = Application(
            user=self.user, name="Testing App",
            client_type=AbstractApplication.CLIENT_PUBLIC,
            authorization_grant_type=AbstractApplication.GRANT_PASSWORD,
        )
        self.app.save()

    def make_user(self, commit=False):
        user = UserFactory.build()
        user.set_password(self.DEFAULT_TEST_PASSWORD)
        if commit:
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

            url = reverse('credentials:login')
            data = dict()
            data["client_id"] = self.app.client_id
            data["client_secret"] = self.app.client_secret
            data["email_or_username"] = username
            data["password"] = self.DEFAULT_TEST_PASSWORD
            data["grant_type"] = "password"

            response = self.client.post(path=url, data=data, format='json')
            self.key = json.loads(response.content.decode("utf-8"))
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.key["access_token"])
            self.access_token = self.key["access_token"]

    def assert_error_response(self, response):
        self.assertEqual("detail" in response.data, True)
        self.assertEqual("code" in response.data, True)

    def assert_token_response(self, response):
        self.assertEqual("expires_in" in response.data, True)
        self.assertEqual("access_token" in response.data, True)
        self.assertEqual("scope" in response.data, True)
        self.assertEqual("refresh_token" in response.data, True)
        self.assertEqual("token_type" in response.data, True)
