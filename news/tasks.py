from .models import User, Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date, timedelta

from news.models import CategorySubscribers


def sending_mail(today):
    start_week = today - timedelta(days=7)
    end_week = today

    post_list = Post.objects.filter(time_create_post__range=(start_week, end_week))
    category_id = []
    post_pk = []
    for post in post_list:
        category_id.extend(post.category.values_list('id', flat=True))
        post_pk.append(post.pk)

    category_id_list = list(set(category_id))
    subscribers_list = list(CategorySubscribers.objects.filter(
        category__in=category_id_list).values_list('subscribers_id', flat=True))

    for pk in subscribers_list:
        subscriber = User.objects.get(pk=pk)
        email = subscriber.email
        username = subscriber.username
        subscriber_posts = Post.objects.filter(
            time_create_post__range=(start_week, end_week),
            category__in=category_id_list)



        html_content = render_to_string(
            'news/reminder_week.html',
            context=
            {'subscriber_posts': subscriber_posts,
             'username': username,
             'domain_url': settings.DOMAIN,}
        )

        msg = EmailMultiAlternatives(
            subject="Новые посты за неделю",
            from_email='django.testemail@yandex.ru',
            to=[email,]
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()