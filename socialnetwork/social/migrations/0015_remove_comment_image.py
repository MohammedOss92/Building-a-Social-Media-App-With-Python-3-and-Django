# Generated by Django 4.1.1 on 2024-09-01 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0014_comment_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='image',
        ),
    ]