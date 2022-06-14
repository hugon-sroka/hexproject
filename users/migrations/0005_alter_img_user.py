# Generated by Django 4.0.2 on 2022-06-12 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_img_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='img', to=settings.AUTH_USER_MODEL),
        ),
    ]