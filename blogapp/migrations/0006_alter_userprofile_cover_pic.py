# Generated by Django 4.0.6 on 2022-08-07 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_userprofile_cover_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cover_pic',
            field=models.ImageField(default='default.jpg', null=True, upload_to='coverpics'),
        ),
    ]
