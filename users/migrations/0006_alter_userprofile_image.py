# Generated by Django 4.0.2 on 2022-06-12 17:26

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_img_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.FileField(upload_to=users.models.upload_to),
        ),
    ]
