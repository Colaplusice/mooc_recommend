# Generated by Django 2.2.1 on 2020-04-17 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mooc',
            name='class_hour',
            field=models.CharField(max_length=32, verbose_name='学时'),
        ),
    ]
