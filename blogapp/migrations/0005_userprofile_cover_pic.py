# Generated by Django 4.0.6 on 2022-08-07 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_userprofile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cover_pic',
            field=models.ImageField(null=True, upload_to='coverpics'),
        ),
    ]
