from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ckeditor.fields import RichTextField
User = get_user_model()
# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    post_img = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    def number_of_likes(self):
        return self.likes.count()
  
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title
    
    
class Follow(models.Model):
    followers = models.ForeignKey(User, related_name="following",on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followers",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    