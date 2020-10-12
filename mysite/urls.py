"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from books_collection.views import home_view, add_book_view, edit_book_view, delete_book_view,\
                                    search_book_view, import_book_view, BookViewRESTAPI

urlpatterns = [
    path('books/', home_view),
    path('books/add/', add_book_view),
    path('books/<int:id>/edit/', edit_book_view),
    path('books/<int:id>/delete/', delete_book_view),
    path('books/search/', search_book_view),
    path('books/api/', BookViewRESTAPI.as_view()),
    path('books/import/', import_book_view),
    path('admin/', admin.site.urls),
]
