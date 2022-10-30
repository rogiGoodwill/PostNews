# Generated by Django 4.1 on 2022-10-26 05:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0002_subscribers_postsubscribers_post_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
