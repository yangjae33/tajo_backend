# Generated by Django 3.0.8 on 2020-07-20 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='bus_idx',
        ),
    ]