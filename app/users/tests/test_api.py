import json

from django.core import mail
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from contrib import codes
from contrib.mixins import OauthTestCase
from users.models import UserAction

from users.serializers import UserSerializer, UserUpdateSerializer

from oauth2_provider.models import get_application_model, AccessToken
from oauth2_provider.compat import get_user_model



Application = get_application_model()
UserModel = get_user_model()

class AccountAPITests(OauthTestCase):

    def setUp(self):
        self.config()
        self.authenticate()

    def __cancel_account(self, user):
        url = reverse('account:cancel')

        self.authenticate(user=user)

        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.SUCCESS_CANCEL_ACCOUNT_SENT)
        self.assertEqual(len(mail.outbox), 1)


    def __update_profile(self, user):
        url = reverse('account:profile')

        self.authenticate(user=user)

        self.user.email = "aaa@bbb.ccc"
        self.user.first_name = "Archundia"
        self.user.last_name = "Ramos"


        user_data = UserUpdateSerializer(self.user).data
        response = self.client.put(path=url, data=user_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_profile(self):
        """
        URL:
            - GET /api/account/profile/

        CHECKPOINTS:
            - Request Serializer validity.
            - Response Statuses.
            - Access Token invalidation.
            - WarpResponse formats.
        """

        url = reverse('account:profile')

        # Invalid access_token
        self.authenticate(token="xxxyyyzzz")
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO convert this response to WarpResponse

        # Valid access_token
        self.authenticate()
        response = self.client.get(path=url)
        user_dict = UserSerializer(self.user, many=False).data # serialized dict
        resp_dict = json.loads(response.content.decode("utf-8")) # response dict
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_dict, resp_dict)


    def test_update_profile(self):
        """
        URL:
            - PUT /api/account/profile/

        CHECKPOINTS:
            - Request Serializer validity.
            - Response Statuses.
            - Access Token operation.
            - WarpResponse formats.
        """
        url = reverse('account:profile')

        # Invalid access_token
        self.authenticate(token="xxxyyyzzz")
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO convert this response to WarpResponse

        # Make changes
        user = self.make_user()
        self.__update_profile(user)

    def test_cancel(self):
        """
        URL:
            - GET|POST /api/account/actions/cancel/

        CHECKPOINTS:
            - create a user
            - get access token
            - get token to cancel account
            - use token to cancel account
            - test when token not is sended
            - test when token is invalid
        """

        url = reverse('account:cancel')

        # Invalid access_token
        self.authenticate(token="xxxyyyzzz")
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO convert this response to WarpResponse

        # Valid access_token
        user = self.make_user()
        self.__cancel_account(user)


    def test_cancel_confirm(self):
        """
        URL:
            - GET|POST /api/account/actions/cancel/

        CHECKPOINTS:
            - create a user and access_token
            - get token to cancel account
            - use token to cancel account
            - test when token not is sended
            - test when token is invalid
        """

        url = reverse('account:cancel')

        # Missing arguments
        self.assert_missing_arguments(url)

        # Invalid access_token
        self.authenticate(token="xxxyyyzzz")
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO convert this response to WarpResponse

        # Valid access_token
        user = self.make_user()
        self.__cancel_account(user)

        token = user.user_actions.get(type=UserAction.ACTION_DISABLE_ACCOUNT).token
        response = self.client.post(path=url, data={"token": token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.SUCCESS_ACCOUNT_DISABLED)


    def test_change_email(self):
        """
        URL:
            - POST /api/account/actions/change-email/

        CHECKPOINTS:
            - create a user and access_token
            - udate a user with a change on email
            - get change email token
            - use the change email token to change email
            - test if new email is valid and saved
            - test when email is invalid
            - test login with new email
        """
        url = reverse('account:change-email')

        # Missing arguments
        self.assert_missing_arguments(url)

        # invalid credentials
        self.authenticate(token="xxxyyyzzz")
        response = self.client.post(path=url, data={"token": "aaabbbccc"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO convert this response to WarpResponse

        # valid user, invalid token
        user = self.make_user()
        self.__update_profile(user)

        response = self.client.post(path=url, data={"token": "aaabbbccc"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_TOKEN)

        # Valid user, valid token
        token = user.user_actions.get(type=UserAction.ACTION_CHANGE_EMAIL).token
        response = self.client.post(path=url, data={"token": token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.SUCCESS_EMAIL_UPDATED)

    def test_clear_sessions(self):
        """
        URL:
            - GET /api/account/profile/

        CHECKPOINTS:
            - Create an user and 3 access tokens
            - send request to clear sessions
            - test if not exist more acces token related to user
        """
        url = reverse('account:clear-sessions')

        # invalid credentials
        self.authenticate(token="xxxyyyzzz")
        response = self.client.get(path=url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO convert this response to WarpResponse

        # make 3 access_tokens and send post request to clear them
        user = self.make_user()

        self.authenticate(user=user)
        self.authenticate(user=user)
        self.authenticate(user=user)

        count = AccessToken.objects.filter(user=user).count()
        self.assertEqual(count, 3)

        response = self.client.get(path=url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.SUCCESS_SESSIONS_CLEARED)

        count = AccessToken.objects.filter(user=user).count()
        self.assertEqual(count, 0)


    def test_logout(self):
        """
        URL:
            - PUT /api/account/profile/

        CHECKPOINTS:
            - Create a user
            - Create 1 access tokens
            - Send token from acces_token
            - Test if this acces_token doesn't exist
        """

        url = reverse('account:logout')

        # invalid credentials
        self.authenticate(token="xxxyyyzzz")
        response = self.client.get(path=url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO convert this response to WarpResponse

        user = self.make_user()
        self.authenticate(user=user)
        response = self.client.get(path=url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.SUCCESS_LOGOUT)

