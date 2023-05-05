from django.contrib.auth.models import User
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter, ModelMultipleChoiceFilter
from .models import Post, Reply

from django.forms import DateInput


class PostFilter(FilterSet):
    title = CharFilter(
        'title',
        label='Заголовок содержит',
        lookup_expr='icontains'
    )

    author = ModelChoiceFilter(
        field_name='author',
        label="Автор",
        lookup_expr='exact',
        queryset=User.objects.all()
    )

    datetime = DateFilter(
        field_name='date_creation',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Дата позже'

    )

    class Meta:
        model = Post
        fields = []
