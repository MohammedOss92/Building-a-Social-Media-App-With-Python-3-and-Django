# Generated by Django 4.1.1 on 2024-09-02 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0016_comment_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/comment_images'),
        ),
    ]