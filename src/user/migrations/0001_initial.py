# Generated by Django 3.2.8 on 2023-02-09 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('bio', models.TextField(blank=True, max_length=80, null=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(default='', max_length=128)),
            ],
        ),
    ]
