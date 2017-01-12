from django.conf.urls import url

from apps.credentials.transactions import (
    ResetPasswordView,
    confirm_register,
)
from apps.credentials.views import GetNumberPhoneView

urlpatterns = [

    url(
        regex=r'^credentials/account-activation/(?P<token>.*)/$',
        view=confirm_register,
        name="account-activation",
    ),

    url(
        regex=r'^credentials/reset-password/(?P<token>.*)/$',
        view=ResetPasswordView.as_view(),
        name="reset-password",
    ),
    url(
        regex=r'^accounts/login/mobile/$',
        view=GetNumberPhoneView.as_view(),
        name='view-login-mobile'
    ),
]