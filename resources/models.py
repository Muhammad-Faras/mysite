from django.db import models

# Create your models here.
class Books(models.Model):
    book_title = models.CharField(max_length=255)
    book_description = models.TextField()
    book_img = models.ImageField(upload_to='admin_books_images/')
    bookpdf = models.FileField(upload_to='admin_books/')
    created_at = models.DateTimeField(auto_now_add=True)
    