# -*- encoding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from oauth2_provider.models import AbstractApplication


class PlatformApp(AbstractApplication):

    has_confirmation = models.BooleanField(
        verbose_name=_("Confirmación en el Registro"),
        help_text=_("Marca este campo  si quieres que esta aplicación envíe una confirmación "
                    "por correo antes de activar una cuenta"),
        default=False,
    )

    logo = models.ImageField(
        verbose_name=_("Logo"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Aplicación')
        verbose_name_plural = _('Aplicaciones')
        app_label = "credentials"

