from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.aggregates import Count
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Post, PostCategory, User, CategorySubscribers, Category, Author
from .filters import NewsFilter
from .forms import NewsModelForm
from django.conf import settings


# Create your views here.

class NewsListView(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create_post')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class SearchListView(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = context['object'].id
        user_id = self.request.user.id
        # category = PostCategory.objects.filter(post_id=post_id).values_list('category_id', flat=True)
        category = PostCategory.objects.filter(post_id=post_id)
        user_category = CategorySubscribers.objects.filter(subscribers_id=user_id)
        context['is_not_subscribe'] = not user_category.exists()
        # проверить, на какие категории еще не подписан

        not_subscribe_category = []
        for cat in category:
            if cat.category_id not in user_category.values_list('category_id', flat=True):
                not_subscribe_category.append(cat)
        context['category'] = not_subscribe_category
        return context


class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'news/news_add.html'
    form_class = NewsModelForm
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

    def post(self, request, *args, **kwargs):
        author = request.POST.get('author')
        if self.is_limit_news(author):
            return super().post(request, *args, **kwargs)
        else:
            return render(request, "news/news_over_limit.html")

    def is_limit_news(self, author):
        today = date.today()
        news_count = Post.objects.filter(
            author=author, time_create_post__startswith=today).aggregate(Count("id")).get("id__count")
        return news_count < 3

    # @staticmethod
    # def sending_mail(request, new_object):
    #     post = new_object
    #     post_title = post.title
    #     post_text = post.text[:50] + '...'
    #     category_id = post.category.values_list('id', flat=True)
    #     news_pk = post.pk
    #
    #     for cat_id in category_id:
    #
    #         subscribers_list = list(
    #             CategorySubscribers.objects.filter(category=cat_id).values_list('subscribers_id', flat=True))
    #         for pk in subscribers_list:
    #             subscriber = User.objects.get(pk=pk)
    #             email = subscriber.email
    #             username = subscriber.username
    #
    #             html_content = render_to_string(
    #                 'news/reminder.html',
    #                 context=
    #                 {'post_title': post_title,
    #                  'post_text': post_text,
    #                  'username': username,
    #                  'news_pk': news_pk,
    #                  'domain_url': settings.DOMAIN,}
    #             )
    #
    #             msg = EmailMultiAlternatives(
    #                 subject=post_title,
    #                 from_email='django.testemail@yandex.ru',
    #                 to=[email,]
    #             )
    #
    #             msg.attach_alternative(html_content, "text/html")
    #             msg.send()


class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/news_add.html'
    form_class = NewsModelForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'news/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post',)


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(author=user)
    return redirect('/news/add')


@login_required
def subscribe_category(request, pk):
    user = [User.objects.get(pk=request.user.id)]
    # post_id = Post.objects.get(pk=pk).id
    # category_id = PostCategory.objects.get(post_id=post_id).category_id
    category = Category.objects.get(pk=pk)
    category.subscribers.set(user)
    return redirect('/news/')
