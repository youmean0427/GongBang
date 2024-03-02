# Generated by Django 4.2.7 on 2024-02-27 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coffeecafes', '0006_coffeecafe_note_coffeecafe_parking_coffeecafe_toilet_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user_review',
        ),
        migrations.AddField(
            model_name='review',
            name='user_name',
            field=models.TextField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]