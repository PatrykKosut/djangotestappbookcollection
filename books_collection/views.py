from urllib import response

import requests
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from books_collection.models import Book
from books_collection.forms import BookForm
from books_collection.filters import BookFilter
from books_collection.serializers import BookSerializer


def home_view(request, *args, **kwargs):
    objects = Book.objects.all()
    context = {
        "form": objects
    }
    return render(request, "home.html", context=context)


def add_book_view(request, *args, **kwargs):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = BookForm()  # clear form after save
    context = {
        'form': form
    }
    return render(request, "add_book.html", context=context)


def edit_book_view(request, id=id, *args, **kwargs, ):
    obj = get_object_or_404(Book, id=id)
    form = BookForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/books/')
    context = {
        'form': form
    }
    return render(request, "edit_book.html", context=context)


def delete_book_view(request, id=id, *args, **kwargs, ):
    obj = get_object_or_404(Book, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('/books/')
    context = {
        "data": obj
    }
    return render(request, "delete_book.html", context=context)


def search_book_view(request):
    book_list = Book.objects.all()
    book_filter = BookFilter(request.GET, queryset=book_list)
    context = {
        "filter": book_filter
    }
    return render(request, 'search_book.html', context=context)


class BookViewRESTAPI(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter


def import_book_view(request):
    query = None
    context = {
        "filter": {}
    }
    print(request.GET)
    if request.GET.get('title'):
        query = 'intitle:' + str(request.GET.get('title'))
        response = requests.get('https://www.googleapis.com/books/v1/volumes?q=%s' % (query))

        data = response.json()
        book_list = []
        for s in data.get('items'):
            try:
                book_list.append(
                    Book(title=s.get('volumeInfo').get('title'),
                         author=s.get('volumeInfo').get('authors'),
                         pub_date=s.get('volumeInfo').get('publishedDate'),
                         isbn_num=s.get('volumeInfo').get('industryIdentifiers')[0].get('identifier'),
                         page_num=s.get('volumeInfo').get('pageCount'),
                         link=s.get('volumeInfo').get('infoLink'),
                         language=s.get('volumeInfo').get('language')
                         )
                )
            except Exception as ex:
                raise ValidationError(ex)

        context = {
            "filter": book_list
        }

        return render(request, 'import_book.html', context=context)
    else:
        return render(request, 'import_book.html', context=context)
