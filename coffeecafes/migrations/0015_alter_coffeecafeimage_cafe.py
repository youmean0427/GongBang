# Generated by Django 5.0.2 on 2024-03-13 08:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffeecafes', '0014_alter_review_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffeecafeimage',
            name='cafe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cafe_images', to='coffeecafes.coffeecafe'),
        ),
    ]