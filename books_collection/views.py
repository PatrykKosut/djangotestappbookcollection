import requests
from django.shortcuts import render, get_object_or_404, redirect
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView

from books_collection.filters import BookFilter
from books_collection.forms import BookForm
from books_collection.models import Book
from books_collection.serializers import BookSerializer


def home_view(request):
    objects = Book.objects.all()
    context = {
        "form": objects
    }
    return render(request, "home.html", context=context)


def add_book_view(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = BookForm()  # clear form after save
    context = {
        'form': form
    }
    return render(request, "add_book.html", context=context)


def edit_book_view(request, id=id):
    obj = get_object_or_404(Book, id=id)
    form = BookForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/books/')
    context = {
        'form': form
    }
    return render(request, "edit_book.html", context=context)


def delete_book_view(request, id=id):
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
    if request.GET.get('title'):
        query = 'intitle:' + str(request.GET.get('title'))
        response = requests.get('https://www.googleapis.com/books/v1/volumes?q=%s' % query)

        data = response.json()
        book_list = []
        try:
            for s in data.get('items'):
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
        except Exception as e:
            # JSON parse error in isbn_num, at this stage wont be fixed :(
            return render(request, 'import_book.html', {})

        context = {
            "filter": book_list
        }
        return render(request, 'import_book.html', context=context)
    else:
        context = {
            "filter": {}
        }
        return render(request, 'import_book.html', context=context)
