
from django.conf.urls import url
from oauth2_provider.views import AuthorizationView

from oauth.api import AuthViewSet, ConvertTokenView, TokenViewSet

urlpatterns = [

    url(
        regex=r'^actions/make-token/$',
        view=TokenViewSet.as_view({'post': 'token'}),
        name="make-token",
    ),

    url(
        regex=r'^actions/refresh-token/$',
        view=TokenViewSet.as_view({'post': 'refresh'}),
        name="refresh-token",
    ),

    url(
        regex=r'^actions/revoke-token/$',
        view=TokenViewSet.as_view({'post': 'revoke'}),
        name="revoke-token",
    ),

    url(
        regex=r'^actions/convert-token/$',
        view=ConvertTokenView.as_view(),
        name="convert-token",
    ),


    url(
        regex=r'^actions/reset-password/$',
        view=AuthViewSet.as_view({'post': 'reset_password'}),
        name='reset-password'
    ),

    url(
        regex=r'^actions/confirm-reset-password/$',
        view=AuthViewSet.as_view({'post': 'confirm_reset_password'}),
        name='confirm-reset-password'
    ),

    url(
        regex=r'^actions/authorize/$',
        view=AuthorizationView.as_view(),
        name="authorize",
    ),

    url(
        regex=r'^actions/check-email/$',
        view=AuthViewSet.as_view({'post': 'check_email'}),
        name='check-email',
    ),

    url(
        regex=r'^actions/check-username/$',
        view=AuthViewSet.as_view({'post': 'check_username'}),
        name="check-username",
    ),

    url(
        regex=r'^register/$',
        view=AuthViewSet.as_view({'post': 'register'}),
        name="register",
    ),

    url(
        regex=r'^register/actions/send-confirmation/$',
        view=AuthViewSet.as_view({'post': 'send_confirmation'}),
        name="send-confirmation",
    ),

    url(
        regex=r'^register/actions/confirm/$',
        view=AuthViewSet.as_view({'post': 'confirm_register'}),
        name="confirm-register",
    ),


]
