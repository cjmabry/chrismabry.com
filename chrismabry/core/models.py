from django.db import models

from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel

CHARFIELD_LONG_LENGTH = 256


@register_setting
class SiteContentSettings(BaseSetting):
    meta_description_default = models.CharField(max_length=CHARFIELD_LONG_LENGTH, blank=True)
    meta_image_default = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('meta_description_default'),
        ImageChooserPanel('meta_image_default'),
    ]

    class Meta:
        verbose_name = 'Site Content Settings'


class BasePage(Page):
    """Base page to provide basic config for all pages"""
    meta_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('meta_image'),
    ]

    class Meta:
        abstract = True


# Reusable ContentStreamField
class ContentStreamField(models.Model):
    content = StreamField([
        ('content_section', blocks.StructBlock([
            ('background', blocks.StructBlock([
                ('color', blocks.ChoiceBlock(
                    help_text="Color of background for the content section. It is recommended to alternate background colors to create visual sepration between content sections.",
                    required=True,
                    choices=[
                        ('light', 'Light'),
                        ('dark', 'Dark'),
                    ]
                )),
                ('image', ImageChooserBlock(required=False))
            ])),
            ('content_options', blocks.StreamBlock([
                ('copy', blocks.StructBlock([
                    ('richtext', blocks.RichTextBlock()),
                    ('text_alignment', blocks.ChoiceBlock(
                        choices=[
                            ('left', 'Left Aligned'),
                            ('center', 'Center Aligned'),
                            ('right', 'Right Aligned'),
                        ],
                        default='left'
                    )),
                ], icon="pilcrow")),
                ('cards_block', blocks.ListBlock(
                    blocks.StructBlock([
                        ('copy', blocks.RichTextBlock(required=True)),
                        ('image', ImageChooserBlock(required=False)),
                        ('link', blocks.URLBlock(required=False)),
                        ('page', blocks.PageChooserBlock(required=False, help_text="Button page will override button URL if present.")),
                    ]), icon="grip"
                )),
                ('signup_block', blocks.RawHTMLBlock(required=True, help_text="Insert the HTML embed code from the VAN link you would like to embed here.",icon="form")),
                ('blockquote', blocks.BlockQuoteBlock(icon="openquote")),
                ('donation_block', blocks.StructBlock([
                    ('copy', blocks.RichTextBlock()),
                    ('image', ImageChooserBlock(required=False)),
                    ('refcode', blocks.CharBlock(required=False, help_text="Add a custom ActBlue refcode, if desired. If this is blank, we will use the default ActBlue refcode.")),
                ], icon="plus")),
                ('button_block', blocks.StructBlock([
                    ('copy', blocks.CharBlock(required=True)),
                    ('link', blocks.URLBlock(required=False)),
                    ('page', blocks.PageChooserBlock(required=False, help_text="Button page will override button URL if present.")),
                    ('alignment', blocks.ChoiceBlock(
                        choices=[
                            ('left', 'Left Aligned'),
                            ('center', 'Center Aligned'),
                            ('right', 'Right Aligned'),
                        ],
                        default='left'
                    )),
                ], icon="link")),
            ], required=False))
        ], icon="edit"))
    ], blank=True)

    content_stream_field_panels = [
        StreamFieldPanel('content')
    ]

    class Meta:
        abstract = True
