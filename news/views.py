from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post
from .filters import NewsFilter
from .forms import NewsModelForm


# Create your views here.

class NewsListView(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create_post')
    paginate_by = 10

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

class NewsCreateView(CreateView):
    template_name = 'news/news_add.html'
    form_class = NewsModelForm


class NewsUpdateView(UpdateView):
    template_name = 'news/news_add.html'
    form_class = NewsModelForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewsDeleteView(DeleteView):
    template_name = 'news/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

