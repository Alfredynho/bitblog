# -*- encoding:utf-8 -*-

from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


REQUIRED_FIELDS = getattr(settings, 'PROFILE_REQUIRED_FIELDS', ['email'])


class User(AbstractUser):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = REQUIRED_FIELDS

    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        db_index=True,
    )

    email = models.EmailField(
        _('email address'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
        unique=True,
        db_index=True,
    )

    photo = models.ImageField(
        _('Photo'),
        upload_to='users/%Y/%m/%d',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def natural_key(self):
        return self.username

    def save(self, *args, **kwargs):
        """ ensure instance has usable password when created """
        if not self.pk and self.has_usable_password() is False:
            self.set_password(self.password)

        super(User, self).save(*args, **kwargs)

    def change_password(self, new_password):
        """
        Changes password and sends a signal
        """
        self.set_password(new_password)
        self.save()
        # password_changed.send(sender=self.__class__, user=self)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def send_email(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        app_label = 'users'


class UserAction(models.Model):

    ACTION_ENABLE_ACCOUNT = "ENABLE_ACCOUNT"
    ACTION_RESET_PASSWORD = "RESET_PASSWORD"
    ACTION_DISABLE_ACCOUNT = "DISABLE_ACCOUNT"
    ACTION_CHANGE_EMAIL = "CHANGE_EMAIL"
    ACTION_CHANGE_USERNAME = "CHANGE_USERNAME"
    ACTION_TYPE = (
        (ACTION_ENABLE_ACCOUNT, "ENABLE_ACCOUNT"),
        (ACTION_RESET_PASSWORD, "RESET_PASSWORD"),
        (ACTION_DISABLE_ACCOUNT, "DISABLE_ACCOUNT"),
        (ACTION_CHANGE_EMAIL, "CHANGE_EMAIL"),
        (ACTION_CHANGE_USERNAME, "CHANGE_USERNAME"),
    )

    user = models.ForeignKey("User", related_name="user_actions")
    type = models.CharField(
        max_length=50,
        choices=ACTION_TYPE,
        db_index=True,
    )

    creation_date = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(db_index=True,)
    token = models.CharField(max_length=150, db_index=True)
    value = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')
        app_label = 'users'
