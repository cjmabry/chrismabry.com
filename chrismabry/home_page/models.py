from django.db import models

from chrismabry.core.models import BasePage

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(BasePage):

    content_panels = BasePage.content_panels
