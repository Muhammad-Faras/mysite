from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class ArticleModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article_title = models.CharField(max_length=255)
    article_body = RichTextUploadingField()
    
    
    def __str__(self):
        return self.article_title