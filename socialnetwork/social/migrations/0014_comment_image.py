# Generated by Django 4.1.1 on 2024-09-01 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0013_tag_alter_comment_options_comment_tags_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/comment_images/'),
        ),
    ]
