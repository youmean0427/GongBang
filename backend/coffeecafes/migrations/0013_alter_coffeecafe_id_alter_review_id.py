# Generated by Django 5.0.2 on 2024-03-12 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffeecafes', '0012_coffeecafe_coffee_coffeecafe_plug_coffeecafe_seat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffeecafe',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
