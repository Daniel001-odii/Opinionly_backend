# Generated by Django 4.2.1 on 2023-05-13 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.TextField(default=models.CharField(max_length=200)),
        ),
    ]