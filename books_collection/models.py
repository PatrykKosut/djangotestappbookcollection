from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    pub_date = models.CharField(max_length=255)
    isbn_num = models.DecimalField(max_digits=13, decimal_places=0)
    page_num = models.DecimalField(max_digits=5, decimal_places=0)
    link = models.CharField(max_length=255)
    language = models.CharField(max_length=255)

    def get_absolute_url(self):
        return f"books/{self.id}/"
