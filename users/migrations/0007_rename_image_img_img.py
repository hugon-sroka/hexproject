# Generated by Django 4.0.2 on 2022-06-12 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_userprofile_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='image',
            new_name='img',
        ),
    ]
