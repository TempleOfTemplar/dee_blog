"""Flexible page"""
from django.db import models
# Create your models here.
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from streams.blocks import *


class FlexPage(Page):
    """Flexible page class"""
    template = "flex/flex_page.html"

    subtitle = models.CharField(max_length=100, null=True, blank=True)
    content = StreamField(
        [
            ("title_and_text", TitleAndTextBlock()),
            ("full_richtext", RichTextBlock()),
            ("simple_richtext", SimpleRichTextBlock()),
            ("cards", CardBlock()),
            ("cta", CTABlock()),
            ("button", ButtonBlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content")
    ]

    class Meta:
        verbose_name = "Flex page"
        verbose_name_plural = "Flex pages"
