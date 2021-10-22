# Generated by Django 3.0.9 on 2021-10-22 20:43

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('wagtailimages', '0023_add_choose_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('hero_copy', wagtail.core.fields.RichTextField(blank=True, null=True)),
                ('hero_video', models.URLField(blank=True, help_text='URL to video that supports the oEmbed protocol, such as a link to a YouTube or Vimeo video. If a video is present, hero image will not display.', null=True)),
                ('hero_signup_enabled', models.BooleanField(default=False)),
                ('content', wagtail.core.fields.StreamField([('content_section', wagtail.core.blocks.StructBlock([('background', wagtail.core.blocks.StructBlock([('color', wagtail.core.blocks.ChoiceBlock(choices=[('light', 'Light'), ('dark', 'Dark')], help_text='Color of background for the content section. It is recommended to alternate background colors to create visual sepration between content sections.')), ('image', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('content_options', wagtail.core.blocks.StreamBlock([('copy', wagtail.core.blocks.StructBlock([('richtext', wagtail.core.blocks.RichTextBlock()), ('text_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left Aligned'), ('center', 'Center Aligned'), ('right', 'Right Aligned')]))], icon='pilcrow')), ('cards_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('copy', wagtail.core.blocks.RichTextBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('link', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(help_text='Button page will override button URL if present.', required=False))]), icon='grip')), ('signup_block', wagtail.core.blocks.RawHTMLBlock(help_text='Insert the HTML embed code from the VAN link you would like to embed here.', icon='form', required=True)), ('blockquote', wagtail.core.blocks.BlockQuoteBlock(icon='openquote')), ('donation_block', wagtail.core.blocks.StructBlock([('copy', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('refcode', wagtail.core.blocks.CharBlock(help_text='Add a custom ActBlue refcode, if desired. If this is blank, we will use the default ActBlue refcode.', required=False))], icon='plus')), ('button_block', wagtail.core.blocks.StructBlock([('copy', wagtail.core.blocks.CharBlock(required=True)), ('link', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(help_text='Button page will override button URL if present.', required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left Aligned'), ('center', 'Center Aligned'), ('right', 'Right Aligned')]))], icon='link'))], required=False))], icon='edit'))], blank=True)),
                ('hero_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('meta_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]