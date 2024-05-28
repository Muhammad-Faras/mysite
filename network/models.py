from django.db import models
from accounts.models import University,Skill
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.name