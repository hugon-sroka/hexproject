# Generated by Django 4.0.2 on 2022-06-12 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_img_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='user',
            new_name='userprofile',
        ),
    ]
