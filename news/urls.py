from django.urls import path
from .views import NewsListView, NewDetailView

urlpatterns = [
    path('news/', NewsListView.as_view()),
    path('news/<int:pk>', NewDetailView.as_view(), name='news-detail'),
]