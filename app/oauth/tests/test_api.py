try:
    import urllib.parse as urllib
except ImportError:
    import urllib

from rest_framework import status
from rest_framework.reverse import reverse


from users.models import User, UserAction
from users.serializers import UserSerializer
from users.tests.factories import UserFactory

from oauth2_provider.models import get_application_model
from oauth2_provider.compat import get_user_model
from django.core import mail

from contrib import codes
from contrib.mixins import OauthTestCase



Application = get_application_model()
UserModel = get_user_model()

class AuthAPITests(OauthTestCase):

    def setUp(self):
        self.config()
        self.authenticate()

    def __do_data4web(self):
        user_data = UserSerializer(UserFactory.build()).data
        _data = user_data.copy()
        _data["password"] = "1234567890x"
        _data["client_id"] = self.app_web.client_id
        _data["client_secret"] = self.app_web.client_secret
        return user_data, _data

    def __do_data4mobile(self):
        user_data = UserSerializer(UserFactory.build()).data
        _data = user_data.copy()
        _data["password"] = "1234567890x"
        _data["client_id"] = self.app_mobile.client_id
        _data["client_secret"] = self.app_mobile.client_secret
        return user_data, _data

    def __do_register_user(self, activate=False):

        if activate:
            user_data, _data = self.__do_data4mobile()
        else:
            user_data, _data = self.__do_data4web()

        response = self.client.post(reverse('auth:register'), _data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=user_data["username"])

        if activate:
            self.assertEqual(user.is_active, True)
        else:
            self.assertEqual(user.is_active, False)

        return user


    def __do__reset_password(self, email_or_user=None):
        url = reverse('auth:reset-password')
        mail.outbox = []
        response = self.client.post(path=url,data={"email_or_user": email_or_user},format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.SUCCESS_RESET_PASSWORD_SENT)
        self.assertEqual(len(mail.outbox), 1)

    def test_register_from_web(self):
        """
        Test: /api/auth/register/ with WEB Client
        """

        # Set WEB data
        user_data, _data = self.__do_data4web()
        response = self.client.post(reverse('auth:register'), _data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Disponibility
        self.assertEqual(User.objects.filter(username=user_data["username"]).count(), 1) # Atomicity
        user = User.objects.get(username=user_data["username"])
        self.assertEqual(response.data, user_data) # Validity
        self.assertEqual(user.is_active, False) # Rules for client
        self.assertEqual(len(mail.outbox), 1) # Email sent


    def test_register_from_mobile(self):
        """
        Test: /api/auth/register/ with MOBILE Client
        """
        # Set MOBILE data
        user_data, _data = self.__do_data4mobile()
        response = self.client.post(reverse('auth:register'), _data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Disponibility
        self.assertEqual(User.objects.filter(username=user_data["username"]).count(), 1) # Atomicity
        user = User.objects.get(username=user_data["username"])
        self.assertEqual(response.data, user_data) # Validity
        self.assertEqual(user.is_active, True) # Rules for client
        self.assertEqual(len(mail.outbox), 1) # Email sent


    def test_send_confirmation(self):
        """
        URL:
            - POST /api/auth/register/actions/send-confirmation/

        CHECKPOINTS:
            1. Request Serializer validity.
            2. Email sent, only user is Inactive.
            3. Response Statuses.
            4. Validity  of the token sent.
            5. WarpResponse formats.
        """
        # settings
        url = reverse('auth:send-confirmation')

        # --> valid request - USERNAME
        mail.outbox = []
        response = self.client.post(path=url,data={"email_or_user": self.user.username},format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.SUCCESS_REGISTER_CONFIRMATION_SENT)

        # --> valid request - EMAIL
        mail.outbox = []
        response = self.client.post(path=url,data={"email_or_user": self.user.email},format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.SUCCESS_REGISTER_CONFIRMATION_SENT)

        # --> empty request
        mail.outbox = []
        response = self.client.post(path=url,data={},format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_MISSING_ARGUMENTS)

        # --> nonexistent user/email request
        mail.outbox = []
        response = self.client.post(path=url,data={"email_or_user": "xx@yyy.com"},format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(mail.outbox), 0)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_NONEXISTENT_ACCOUNT)



    def test_register_confirm(self):
        """
        URL:
            - POST /api/auth/register/actions/confirm/

        CHECKPOINTS:
            - Request Serializer validity
            - Confirm, only if user is inactive.
            - Response Statuses.
            - Validity  of the received token.
            - WarpResponse formats.
        """
        # settings
        url = reverse('auth:confirm-register')

        # --> empty request
        self.assert_missing_arguments(url)

        # --> invalid token
        response = self.client.post(path=url,data={"token": "whatever"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_TOKEN)

        # --> valid token

        user = self.__do_register_user(activate=False)
        token = user.user_actions.get(type=UserAction.ACTION_ENABLE_ACCOUNT).token
        response = self.client.post(path=url,data={"token": token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user.refresh_from_db()
        self.assertEqual(user.is_active, True)



    def test_check_username(self):
        """
        URL:
            - POST /api/auth/actions/check-username/

        CHECKPOINTS:
            - Request Serializer validity
            - Response Statuses.
            - WarpResponse formats.
        """
        # settings
        url = reverse('auth:check-username')

        # --> empty request
        self.assert_missing_arguments(url)

        # --> nonexistent username
        response = self.client.post(path=url,data={"username": "jvacx"},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.STATUS_AVAILABLE_USERNAME)

        # --> existent username
        user = self.__do_register_user(activate=True)

        response = self.client.post(path=url,data={"username": user.username},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.STATUS_REGISTERED_USER)


    def test_check_email(self):
        """
        URL:
            - POST /api/auth/actions/check-email/

        CHECKPOINTS:
            - Request Serializer validity
            - Response Statuses.
            - WarpResponse formats.
        """
        # settings
        url = reverse('auth:check-email')

        # --> empty request
        self.assert_missing_arguments(url)

        # --> nonexistent email
        response = self.client.post(path=url,data={"email": "xxx@yyy.zzz"},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.STATUS_AVAILABLE_EMAIL)

        # --> existent email
        user = self.__do_register_user(activate=True)

        response = self.client.post(path=url,data={"email": user.email},format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.STATUS_REGISTERED_USER)


    def test_reset_password(self):
        """
        URL:
            - POST /api/auth/actions/reset-password/

        CHECKPOINTS:
            - Request Serializer validity
            - Email sent.
            - Validate reset token.
            - Response Statuses.
            - WarpResponse formats.
        """
        # settings
        url = reverse('auth:reset-password')

        # --> empty request
        self.assert_missing_arguments(url)

        # --> invalid user
        response = self.client.post(path=url,data={"email_or_user": "xxx@yyy.zzz"},format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_NONEXISTENT_ACCOUNT)


        # --> inactive user by username/email
        user = self.__do_register_user(activate=False)

        response = self.client.post(path=url,data={"email_or_user": user.username},format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INACTIVE_ACCOUNT)

        response = self.client.post(path=url,data={"email_or_user": user.email},format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INACTIVE_ACCOUNT)


        # --> valid user by username/email
        user.is_active = True
        user.save()

        self.__do__reset_password(email_or_user=user.username)
        self.__do__reset_password(email_or_user=user.email)


    def test_confirm_reset_password(self):
        """
        URL:
            - POST /api/auth/actions/confirm-reset-password/

        CHECKPOINTS:
            - Request Serializer validity.
            - Email sent.
            - Validate reset token.
            - Response Statuses.
            - WarpResponse formats.
        """
        # settings
        url = reverse('auth:confirm-reset-password')

        # --> empty request
        self.assert_missing_arguments(url)

        # --> invalid token
        response = self.client.post(path=url,data={"token": "xxyyzz", "password": "xxxyyyzzz"},format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_TOKEN)

        # --> valid token, inactive account
        user = self.__do_register_user(activate=True)
        self.__do__reset_password(email_or_user=user.username)
        user.refresh_from_db()
        user.is_active = False
        user.save()


        token = user.user_actions.get(type=UserAction.ACTION_RESET_PASSWORD).token
        response = self.client.post(path=url, data={"token": token, "password": "xxxyyyzzz"}, format='json')


        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INACTIVE_ACCOUNT)

        # --> valid token, valid account
        user.is_active = True
        user.save()

        # action_reset = user.useractions
        response = self.client.post(path=url, data={"token": token, "password": "xxxyyyzzz"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.SUCCESS_PASSWORD_RESET)


    def test_make_token(self):
        """
        URL:
            - POST /api/auth/actions/make-token/

        CHECKPOINTS:
            - Request Serializer validity.
            - Response Statuses.
            - Access Token Operation.
            - WarpResponse formats.
        """
        # settings
        url = reverse('auth:make-token')

        # empty request
        self.assert_missing_arguments(url)

        # invalid or inexistent client
        data = dict()
        data["client_id"] = "xxx"
        data["client_secret"] = "yyy"
        data["email_or_user"] = self.username
        data["password"] = self.password

        response = self.client.post(path=url,data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_APPLICATION)

        # invalid credentials
        data["client_id"] = self.app_mobile.client_id
        data["client_secret"] = self.app_mobile.client_secret
        data["email_or_user"] = "xxx@yyy.zzz"
        data["password"] = "xxxyyyzzz"

        response = self.client.post(path=url,data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_USER_CREDENTIALS)

        # valid client usermail/email
        # this test was covered by Django oauth toolkit, is unnecessary in to have in here.

        # TODO test token in a single operation


    def test_refresh_token(self):
        """
        URL:
            - POST /api/auth/actions/refresh-token/

        CHECKPOINTS:
            - Request Serializer validity.
            - Response Statuses.
            - New Access Token Operation.
            - Old Access Token invalidation.
            - WarpResponse formats.
        """
        # settings
        url = reverse('auth:refresh-token')

        # empty request
        self.assert_missing_arguments(url)

        # invalid or inexistent client/refresh_token
        data = dict()
        data["client_id"] = "xxx"
        data["client_secret"] = "yyy"
        data["refresh_token"] = "zzz"
        data["grant_type"] = "refresh_token"

        response = self.client.post(path=url,data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_APPLICATION)

        # invalid refresh token
        data["client_id"] = self.application.client_id
        data["client_secret"] = self.application.client_secret
        data["refresh_token"] = "xxxyyyzzz"

        response = self.client.post(path=url,data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_REFRESH_TOKEN)


        # ------------------
        # TODO  TEST FUNCTIONALTY
        # ------------------

        # # ---> Make request and get Acces Token
        # url = reverse('auth:make-token')
        # data = dict()
        # data["client_id"] = self.application.client_id
        # data["client_secret"] = self.application.client_secret
        # data["email_or_user"] = self.user_username
        # data["password"] = self.user_password
        # data["grant_type"] = "password"
        #
        # response = self.client.post(path=url,data=data, format='multipart')

        # ---> Send refresh token and get new Access Token

        # url = reverse('auth:refresh-token')
        # data["refresh_token"] = "xxxyyyzzz"


        # ---> Use the new acesss token

    def test_revoke_token(self):
        """
        URL:
            - POST /api/auth/actions/revoke-token/

        CHECKPOINTS:
            - Request Serializer validity.
            - Response Statuses.
            - Access Token invalidation.
            - WarpResponse formats.
        """
        # settings
        url = reverse('auth:revoke-token')

        # empty request
        self.assert_missing_arguments(url)

        # invalid or inexistent client
        data = dict()
        data["client_id"] = "xxx"
        data["client_secret"] = "yyy"
        data["token"] = "zzz"

        response = self.client.post(path=url,data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_APPLICATION)

        # invalid token
        data["client_id"] = self.application.client_id
        data["client_secret"] = self.application.client_secret
        data["token"] = "xxxyyyzzz"

        response = self.client.post(path=url,data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_TOKEN)


        # VALID REQUEST TESTS was covered in django oauth toolkit

        # TODO verify that old token doen't exist


    def test_convert_token(self):
        """
        URL:
            - POST /api/auth/actions/convert-token/

        CHECKPOINTS:
            - Request Serializer validity.
            - Response Statuses.
            - Access Token operation.
            - WarpResponse formats.
        """
        # settings - provide a social access token
        url = reverse('auth:convert-token')

        # empty request
        self.assert_missing_arguments(url)

        # invalid or inexistent client
        data = dict()
        data["client_id"] = "xxx"
        data["client_secret"] = "yyy"
        data["backend"] = "facebook"
        data["token"] = "xxxyyyzzz"

        response = self.client.post(path=url,data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_warp_response(response)
        self.assertEqual(response.data["code"], codes.ERROR_INVALID_APPLICATION)

        # # invalid backend
        # data["client_id"] = self.application.client_id
        # data["client_secret"] = self.application.client_secret
        # data["backend"] = "xxyyyzzz"
        #
        # response = self.client.post(path=url,data=data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.__assert_warp_response(response)
        # self.assertEqual(response.data["code"], codes.ERROR_UNSUPPORTED_SOCIAL_BACKEND)

        # TODO verify that old token doen't exist