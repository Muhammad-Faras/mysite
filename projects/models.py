from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()

class ProjcetShowcase(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    project_description = RichTextUploadingField()
    