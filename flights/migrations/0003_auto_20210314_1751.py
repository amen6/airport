# Generated by Django 3.1.5 on 2021-03-14 15:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_auto_20210313_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='passengers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
