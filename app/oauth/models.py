from django.db import models
from oauth2_provider.models import AbstractApplication
from django.utils.translation import ugettext_lazy as _

class WarpApplication(AbstractApplication):

    CATEGORY_WEB = "WEB"
    CATEGORY_MOBILE = "MOBILE"
    CATEGORY_CHOICES = [
        (CATEGORY_WEB, _("WEB")),
        (CATEGORY_MOBILE, _("MOBILE")),
    ]

    logo = models.ImageField(
        verbose_name=_("Logo"),
        blank=True,
        null=True,
    )

    category = models.CharField(
        verbose_name=_("Category"),
        max_length=10,
        default=CATEGORY_WEB,
        choices=CATEGORY_CHOICES,
    )

    class Meta:
        verbose_name = _('application')
        verbose_name_plural = _('applications')
        # app_label = 'authx'
