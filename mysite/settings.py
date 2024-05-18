"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r3fsi)#lzcs7l93sm-mxxxxp1h+-&95=!jqu-jyv3y1o4_rv+c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False


ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition



INSTALLED_APPS = [
    'daphne',
    'fontawesomefree',     # app for fontawasome
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',
    'home',
    'feed',
    'network',
    'resources',
    'projects',
    'posts',
    'articles',
    'chat',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    
    'ckeditor',  
    'ckeditor_uploader' ,
    
    
    
    'tailwind', 
    'theme',
    'django_browser_reload',
]

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
        'toolbar': 'Custom',
        # Specify Custom Shit - GPL License -
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', '-', 'Image', 'Link', 'CodeSnippet', '-', 'NumberedList', 'BulletedList', 'HorizontalRule', '-', 'Undo', 'Redo'],
        ], 'extraPlugins': 'codesnippet'
    }
}


SITE_ID = 2

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE' : [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type':'online',
        },
         'APP': {
            'client_id': '50230916815-vmvmecg0i8gu6vtb4ng03vj6hb39dgpe.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    },
    'github': {
        'SCOPE' : [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type':'online',
        },
         'APP': {
            'client_id': 'bf149d46d4e934221c8b',
            'secret': '4e187906abc77106d54e4c7ed04f0a9162017558',
            'key': ''
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware", # tailwind auto reload
    # 'accounts.middlewares.ProfileCompletionMiddleware',
    
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                (os.path.join(BASE_DIR, 'templates')),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'mysite.wsgi.application'
ASGI_APPLICATION = 'mysite.asgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    (os.path.join(BASE_DIR, 'static')),
    (os.path.join(BASE_DIR, 'home','static')),
    (os.path.join(BASE_DIR, 'feed','static')),
    (os.path.join(BASE_DIR, 'network','static')),
    (os.path.join(BASE_DIR, 'articles','static')),
    (os.path.join(BASE_DIR, 'accounts','static')),
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'




AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'django.core.mail.backends.console.EmailBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# ACCOUNT_EMAIL_VERIFICATION = 'none'

# ACCOUNT_USER_MODEL_USERNAME_FIELD = True
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = True
# ACCOUNT_AUTHENTICATION_METHOD = 'email'


# ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'


# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
# settings.py

LOGIN_REDIRECT_URL = 'accounts:custom_login_redirect'

# LOGIN_REDIRECT_URL = 'feed:feed'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'

# ACCOUNT_LOGOUT_REDIRECT_URL = 'home'

ACCOUNT_SESSION_REMEMBER = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 432000   # 5 days session

ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

ACCOUNT_FORMS = {
    'signup': 'accounts.forms.SignupFormExtended',
    # You can define other custom forms here if needed
}


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}




handler404 = 'home.views.custom_404_view_name'