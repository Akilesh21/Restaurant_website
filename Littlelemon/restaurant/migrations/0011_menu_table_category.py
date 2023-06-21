# Generated by Django 4.2 on 2023-06-19 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0010_menu_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu_table',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='restaurant.category'),
        ),
    ]
