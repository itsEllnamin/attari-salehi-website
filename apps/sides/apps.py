from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SidesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.sides"
    verbose_name = _("جانبی‌ها")