# Generated by Django 4.2.7 on 2023-12-29 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffeecafes', '0002_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
