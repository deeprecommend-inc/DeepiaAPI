# Generated by Django 3.2.8 on 2021-11-13 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0004_log_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
