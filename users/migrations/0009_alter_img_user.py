# Generated by Django 4.0.2 on 2022-06-12 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_userprofile_image_remove_userprofile_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
