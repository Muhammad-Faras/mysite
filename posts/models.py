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

    likes = models.ManyToManyField(User, related_name='blogpost_like')


    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_comments(self):
        return self.comments.count()
    
    
    
    def __str__(self) -> str:
        return self.title
    
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    comment_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.created_at}'




class Report(models.Model):
    REPORT_CHOICES = [
        ('SPAM', 'Spam'),
        ('ABUSE', 'Abusive Content'),
        ('OTHER', 'Other'),
    ]

    post_ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=10, choices=REPORT_CHOICES)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='report_images/', blank=True, null=True)  # ImageField for report image
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report by {self.reported_by.username} on {self.post_ref.author.username}'s post {self.post_ref.title}"
    