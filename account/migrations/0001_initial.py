# Generated by Django 3.0.8 on 2020-07-12 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_idx', models.CharField(max_length=50)),
                ('user_id', models.CharField(max_length=50)),
                ('user_password', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('user_registerdate', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
