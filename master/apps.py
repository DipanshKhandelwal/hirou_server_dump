from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MasterConfig(AppConfig):
    name = 'master'
    verbose_name = _('Master')
    verbose_name_plural = _('Masters')
