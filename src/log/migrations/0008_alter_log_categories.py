# Generated by Django 3.2.8 on 2022-03-06 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_remove_category_logs'),
        ('log', '0007_log_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='category.Category'),
        ),
    ]
