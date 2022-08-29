from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.

class NewsListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create_post')


class NewDetailView(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'
