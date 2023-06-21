# Generated by Django 4.2 on 2023-06-20 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0014_remove_menu_table_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu_table',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='restaurant.category'),
        ),
    ]
