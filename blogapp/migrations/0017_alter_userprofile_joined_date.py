# Generated by Django 4.0.6 on 2022-08-11 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0016_alter_userprofile_joined_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='joined_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
