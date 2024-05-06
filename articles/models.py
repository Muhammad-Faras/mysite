from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class ArticleModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article_title = models.CharField(max_length=100)
    article_thumbnail_image = models.ImageField(null=True)
    article_description = models.TextField(max_length=400)
    article_body = RichTextUploadingField()
    article_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.article_title