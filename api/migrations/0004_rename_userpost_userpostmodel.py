# Generated by Django 4.2.1 on 2023-05-24 20:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPost',
            new_name='UserPostModel',
        ),
    ]
