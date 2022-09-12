from django.urls import path
from .views import NewsListView, NewDetailView, SearchListView, NewsCreateView, NewsDeleteView, NewsUpdateView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news'),
    path('news/<int:pk>', NewDetailView.as_view(), name='news-detail'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news-edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),
    path('news/add/', NewsCreateView.as_view(), name='news-create'),
    path('news/search', SearchListView.as_view(), name='news-search'),
]