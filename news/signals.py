from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post, CategorySubscribers


@receiver(post_save, sender=Post)
def notify_post_create(instance, **kwargs):

    post = instance
    post_title = post.title
    post_text = post.text[:50] + '...'
    category_id = post.category.values_list('id', flat=True)
    news_pk = post.pk

    for cat_id in category_id:

        subscribers_list = list(
            CategorySubscribers.objects.filter(category=cat_id).values_list('subscribers_id', flat=True))
        for pk in subscribers_list:
            subscriber = User.objects.get(pk=pk)
            email = subscriber.email
            username = subscriber.username

            html_content = render_to_string(
                'news/reminder.html',
                context=
                {'post_title': post_title,
                 'post_text': post_text,
                 'username': username,
                 'news_pk': news_pk,
                 'domain_url': settings.DOMAIN, }
            )

            msg = EmailMultiAlternatives(
                subject=post_title,
                from_email='django.testemail@yandex.ru',
                to=[email, ]
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()
