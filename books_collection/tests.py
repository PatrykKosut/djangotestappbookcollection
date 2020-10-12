from datetime import datetime

from django.test import TestCase

from books_collection.models import Book


# Create your tests here.


class BookTestCase(TestCase):
    def setUp(self):
        num_of_books = 5
        for s in range(0, num_of_books):
            Book.objects.create(
                title="title" + str(s),
                author='author' + str(s),
                pub_date=datetime.now,
                isbn_num=str(s),
                page_num=str(s),
                link='http://exmaple.com/' + str(s),
                language='PL'
            )

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.get_absolute_url(), 'books/' + str(1))
        self.assertEquals(book.get_absolute_url() + str('/edit'), 'books/' + str(1) + '/edit')

        book = Book.objects.get(id=2)
        self.assertEquals(book.get_absolute_url(), 'books/' + str(2))
        self.assertEquals(book.get_absolute_url() + str('/edit'), 'books/' + str(2) + '/edit')

    def test_view_url_exists(self):
        res = self.client.get('/books/')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/books/api/')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/books/add/')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/books/search/')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/books/import/')
        self.assertEqual(res.status_code, 200)

    def test_view_uses_correct_template(self):
        res = self.client.get('/books/add/')
        self.assertTemplateUsed(res, 'add_book.html')

        res = self.client.get('/books/search/')
        self.assertTemplateUsed(res, 'search_book.html')

        res = self.client.get('/books/import/')
        self.assertTemplateUsed(res, 'import_book.html')
