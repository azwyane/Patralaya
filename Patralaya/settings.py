"""
Django settings for Patralaya project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# heroku-config package
import django_heroku

import json
import os

# open secrets file as a dictonary
with open("secrets.json") as f:
    secrets = json.load(f)

#get secrets from key value pair
def get_secret(settings,secrets=secrets):
    return secrets[settings]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("s_key",default="randomsecrectforProduction123$%^70001") 

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get("state"):
    DEBUG = False 
else:
    DEBUG = True 

ALLOWED_HOSTS = []

import sys
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    #local apps
    'events.apps.EventsConfig',
    'services.apps.ServicesConfig',
    'profiles.apps.ProfilesConfig',
    'activities.apps.ActivitiesConfig',
    'feedaggregate.apps.FeedAggregateConfig',

    #(3rd party)
    'ckeditor',
    'taggit',
    'widget_tweaks',
    'mathfilters'
]
#ckeditor configuration
CKEDITOR_CONFIGS = {
'default': {
    'height':'auto',
    'width': 'auto',

          },
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  #language select middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Patralaya.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'profiles.context_processors.profile_render', #custom context processor
                'events.context_processors.categories', 
            ],
        },
    },
]

WSGI_APPLICATION = 'Patralaya.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {

    # sqlite engiene 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

    #uncomment this if using postgres on production
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    #     'USER': get_secret('db_user'),
    #     'PASSWORD': get_secret('db_passwd'),
    #     'HOST': get_secret('db_host'),
    #     'PORT': get_secret('db_port'),
    # }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = [
    os.path.join(BASE_DIR,'locale')
]

LANGUAGES = [
    ('en','English'),
    ('ne', 'Nepali')
]

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] #bootstrap files sits here


# Activate Django-Heroku.
django_heroku.settings(locals())

# media root (holds media files)
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

#emailconfig
DEFAULT_FROM_EMAIL = 'noreply@Patralaya'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.sendgrid.net'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_TIMEOUT=21600
EMAIL_HOST_USER=get_secret('e_host')
EMAIL_HOST_PASSWORD = os.environ.get('e_pass')

LOGIN_URL ='login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
