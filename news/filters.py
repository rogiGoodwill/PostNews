from django_filters import FilterSet, DateFilter, CharFilter
from django.forms import DateInput
from .models import Post



class NewsFilter(FilterSet):
    '''
    Реализована возможность пользователю искать новости по определённым критериям.
    Критерии должны быть следующие:
    - позже какой-либо даты;
    - по названию;
    - по имени пользователя автора;
    - всё вместе.
    '''
    post_date = DateFilter(field_name='time_create_post',
                           lookup_expr='gt',
                           label='Опубликовано после даты:',
                           widget = DateInput(format='%d.%m.%Y', attrs={'type': 'date'})
                           )

    title = CharFilter(field_name='title', lookup_expr='contains', label='Название:')
    class Meta:
        model = Post
        fields = ['post_date', 'title', 'author']

