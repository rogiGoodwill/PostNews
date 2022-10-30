# Generated by Django 4.1 on 2022-10-26 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('news', '0004_alter_subscribers_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='subscribers',
            field=models.ManyToManyField(through='news.PostSubscribers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postsubscribers',
            name='subscribers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Subscribers',
        ),
    ]