# Generated by Django 4.1 on 2022-10-25 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostSubscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
                ('subscribers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.subscribers')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='subscribers',
            field=models.ManyToManyField(through='news.PostSubscribers', to='news.subscribers'),
        ),
    ]
