# Generated by Django 4.2.7 on 2024-02-27 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coffeecafes', '0007_remove_review_user_review_review_user_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user_name',
        ),
    ]
