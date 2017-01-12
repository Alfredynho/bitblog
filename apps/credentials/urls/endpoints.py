

from apps.credentials.api import AuthViewSet, TokenViewSet

from django.conf.urls import url
from oauth2_provider.views import AuthorizationView

from apps.credentials.views import FacebookLogin

urlpatterns = [

    url(
        regex=r'^api/credentials/login/$',
        view=TokenViewSet.as_view({'post': 'token'}),
        name="login",
    ),

    url(
        regex=r'^api/credentials/refresh-token/$',
        view=TokenViewSet.as_view({'post': 'refresh'}),
        name="refresh-token",
    ),

    url(
        regex=r'^api/credentials/revoke-token/$',
        view=TokenViewSet.as_view({'post': 'revoke'}),
        name="revoke-token",
    ),

    url(
        regex=r'^api/credentials/facebook/login/$',
        view=FacebookLogin.as_view(),
        name="facebook-login",
    ),


    url(
        regex=r'^api/credentials/reset-password/$',
        view=AuthViewSet.as_view({'post': 'reset_password'}),
        name='reset-password'
    ),

    url(
        regex=r'^api/credentials/confirm-reset-password/$',
        view=AuthViewSet.as_view({'post': 'confirm_reset_password'}),
        name='confirm-reset-password'
    ),

    url(
        regex=r'^api/credentials/authorize/$',
        view=AuthorizationView.as_view(),
        name="authorize",
    ),

    url(
        regex=r'^api/credentials/check-email/$',
        view=AuthViewSet.as_view({'post': 'check_email'}),
        name='check-email',
    ),

    url(
        regex=r'^api/credentials/check-username/$',
        view=AuthViewSet.as_view({'post': 'check_username'}),
        name="check-username",
    ),

    url(
        regex=r'^api/credentials/register/$',
        view=AuthViewSet.as_view({'post': 'register'}),
        name="register",
    ),

    url(
        regex=r'^api/credentials/send-confirmation/$',
        view=AuthViewSet.as_view({'post': 'send_confirmation'}),
        name="send-confirmation",
    ),

    url(
        regex=r'^api/credentials/confirm/$',
        view=AuthViewSet.as_view({'post': 'confirm_register'}),
        name="confirm-register",
    ),

]
