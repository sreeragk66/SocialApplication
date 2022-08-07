# Generated by Django 4.0.6 on 2022-08-07 14:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogapp', '0008_alter_userprofile_cover_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='liked_by',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]