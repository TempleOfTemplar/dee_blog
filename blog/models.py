# Create your models here.
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from streams.blocks import TitleAndTextBlock, RichTextBlock, SimpleRichTextBlock, CardBlock, CTABlock


class BlogAuthorsOrderable(Orderable):
    """This allow us to select one or more authors"""

    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author")
    ]


@register_snippet
class BlogAuthor(models.Model):
    """Blog author for snippet"""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+'
    )

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            ImageChooserPanel("image")
        ], heading="Name and image"),
        MultiFieldPanel([
            FieldPanel("website")
        ], heading="Links")
    ]

    def __str__(self):
        """string representation"""
        return self.name

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = "BLog Authors"


@register_snippet
class BlogCategory(models.Model):
    """blog category for a snippet"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        max_length=255,
        help_text="Slug to identify posts by category"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug")
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog category"
        verbose_name_plural = "Blog categories"
        ordering = ["name"]


class BlogListingPage(RoutablePageMixin, Page):
    """Listing page for Blog pages"""

    template = "blog/blog_listing_page.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="override default title")
    content_panels = Page.content_panels + [
        FieldPanel("custom_title")
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custon stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        all_posts = BlogDetailPage.objects.all().order_by('-first_published_at')
        paginator = Paginator(all_posts, 1)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["authors"] = BlogAuthor.objects.all()
        context["reverse_url"] = self.reverse_subpage('latest_posts')
        context["categories"] = BlogCategory.objects.all()
        return context

    @route(r'^latest/?$', name='latest_posts')
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request=None):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_posts"),
                "lastmod": self.last_published_at or self.latest_revision_created_at,
                "priority": 0.9,
            }
        )
        return sitemap


class BlogDetailPage(Page):
    """Parental blog detail page"""

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="override default title")

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL
    )

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    content = StreamField(
        [
            ("title_and_text", TitleAndTextBlock()),
            ("full_richtext", RichTextBlock()),
            ("simple_richtext", SimpleRichTextBlock()),
            ("cards", CardBlock()),
            ("cta", CTABlock())
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("banner_image"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
        ], heading="Author(s)"),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
        ], heading="Categories"),
        StreamFieldPanel("content")
    ]


class ArticleBlogPage(BlogDetailPage):
    """subcassed blog page for aticles"""
    template = "blog/article_blog_page.html"
    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Best size for this image will be 1400x400'
    )

    content_panels = BlogDetailPage.content_panels + [
        FieldPanel("subtitle"),
        ImageChooserPanel("intro_image")
    ]


class VideoBlogPage(BlogDetailPage):
    """Video subclass page"""
    template = "blog/video_blog_page.html"

    youtube_video_id = models.CharField(max_length=30)
    content_panels = BlogDetailPage.content_panels + [
        FieldPanel("youtube_video_id"),
    ]
