from books_collection.models import Book
from django_filters import rest_framework as filters


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains', field_name='title')
    author = filters.CharFilter(lookup_expr='icontains', field_name='author')
    language = filters.CharFilter(lookup_expr='exact', field_name='language')
    start_date = filters.DateFilter(lookup_expr='gte', field_name='pub_date')
    end_date = filters.DateFilter(lookup_expr='lte', field_name='pub_date')

    class Meta:
        model = Book
        fields = ['title', 'author', 'language', 'pub_date']
