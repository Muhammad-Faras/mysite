from django.db import models
from accounts.models import Skill
# Create your models here.
class Books(models.Model):
    book_title = models.CharField(max_length=255)
    book_description = models.TextField()
    book_img = models.ImageField(upload_to='admin_books_images/')
    bookpdf = models.FileField(upload_to='admin_books/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class VideosLinks(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.DO_NOTHING)
    link_description = models.TextField()
    link = models.URLField()
    link_created_at = models.DateTimeField(auto_now_add=True)
    
    