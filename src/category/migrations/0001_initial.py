from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('log', '0006_auto_20220115_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('user_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('logs', models.ManyToManyField(blank=True, to='log.Log')),
            ],
        ),
    ]
