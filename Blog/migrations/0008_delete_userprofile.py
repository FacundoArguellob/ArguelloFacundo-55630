# Generated by Django 4.2.4 on 2023-09-01 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0007_remove_userprofile_img_userprofile_profile_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
