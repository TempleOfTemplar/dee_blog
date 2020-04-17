from django.db import models

# Create your models here.
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class SocialMediaSettings(BaseSetting):
    """Sotcial media settings"""

    vkontakte = models.URLField(blank=True, null=True, help_text="Ссылка на Вконтакте")
    telegram = models.URLField(blank=True, null=True, help_text="Ссылка на Telegram")
    youtube = models.URLField(blank=True, null=True, help_text="Ссылка на YouTube")

    panels = [
        MultiFieldPanel([
            FieldPanel("vkontakte"),
            FieldPanel("telegram"),
            FieldPanel("youtube"),
        ], heading="Ссылки на социальные сети"
        )
    ]
