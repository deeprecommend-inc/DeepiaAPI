# Generated by Django 3.2.8 on 2021-11-03 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
