from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    


class Skill(models.Model):
    skill_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.skill_name


class University(models.Model):
    university_name = models.CharField(max_length=150,unique=True)

    def __str__(self):
        return self.university_name

class Gender(models.Model):
    gender_cateory = models.CharField(max_length=150,unique=True)

    def __str__(self):
        return self.gender_cateory
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True)
    skill = models.ForeignKey(Skill,on_delete=models.SET_NULL, null=True)
    bio = models.TextField(blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    twitter_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    birthday = models.DateField(null=True)
    profile_img = models.ImageField(null=True, blank=True)

    def is_complete(self):
        # Check if all required fields are filled
        required_fields = [
            self.skill,
        ]
        if not all(required_fields):
            return False
        return True
        
    def __str__(self):
        if self.user.is_superuser:
            return f'{self.user.username} (Superuser) profile'
        else:
            return f'({self.user.username}) profile  ({self.user.email})'




class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.follower.username} is following {self.following.username}'

    