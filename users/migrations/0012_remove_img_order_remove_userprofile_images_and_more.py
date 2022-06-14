# Generated by Django 4.0.2 on 2022-06-12 18:10

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_userprofile_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='img',
            name='order',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='images',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.FileField(default=1, upload_to=users.models.upload_to),
            preserve_default=False,
        ),
    ]
