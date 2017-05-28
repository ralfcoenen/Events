"""
Django settings for Events project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*j=lr(u&o@alycr!gts!8n10vpo$0)6ebggg(3lpg-_vu1$7py'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['anmeldung.ekayana-institut.de']
ALLOWED_HOSTS = ['127.0.0.1']
USE_X_FORWARDED_HOST = True


# Application definition

INSTALLED_APPS = (
    'filebrowser',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Anmeldung.apps.AnmeldungConfig',
    'tinymce',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'Events.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'Events.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
'''
#Local Development-Server
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'ekayana_django',
        # 'USER': 'ekayana',
        # 'PASSWORD': 'ooCohj9Weing4too',
        # 'HOST': '127.0.0.1',
        # 'PORT': '',
        # 'OPTIONS': {
        #   'init_command': "SET sql_mode='STRICT_ALL_TABLES'"
        # },
    }
}
'''

# Production-Server
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ekayana_django',
        'USER': 'ekayana',
        'PASSWORD': 'ooCohj9Weing4too',
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {
          'init_command': "SET sql_mode='STRICT_ALL_TABLES'"
        },
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = [
    ('de', _('Deutsch')),
    ('en', _('Englisch')),
    ('fr', _('Französisch')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
#
#  Modeltranslation
#


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

ADMINS = [('Ralf', 'ralf@subuthi.de')]

#
#
#
GOOGLE_RECAPTCHA_SECRET_KEY = '6Lc4pxcUAAAAAJYwrpNAR5y__tVLJpBa6DPs3eUm'
#
#  Email
#
EMAIL_HOST = 'peacock.uberspace.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ralf@ekayana-institut.de'
EMAIL_HOST_PASSWORD = 'Paaf.3010'

#
# Production
# ###################
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/virtual/ekayana/anmeldung.ekayana-institut.de/static/'
MEDIA_ROOT = '/var/www/virtual/ekayana/anmeldung.ekayana-institut.de/media/'
MEDIA_URL = '/media/'
'''
#
#  Development
# #########################
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#
#   django-filebrowser
#
'''
FILEBROWSER_DIRECTORY = ''
DIRECTORY = ''

FILEBROWSER_SELECT_FORMATS = {
    # image is used when you click on "Insert/edit image" icon
    'image': ['Image'],
    # file is used when you click on "Insert/edit link" icon
    'file': ['Folder', 'Image', 'Video', 'Document', 'Audio', 'Code'],
    # media is probably used when you click on "Insert/edit media" icon
    'media': ['Video', 'Audio'],
}

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'modern',
    'plugins': 'link image preview codesample contextmenu table code lists advlist hr',
    'toolbar1': 'styleselect formatselect fontselect fontsizeselect | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | bullist numlist hr | outdent indent | table | link image | codesample | preview code',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'inline': False,
    'statusbar': True,
    'height': 460,
    # 'content_css': '/var/www/virtual/subuthi/django.subuthi.de/static/Anmeldung/bootstrap/css/bootstrap.css',
    'content_css': os.path.join(STATIC_ROOT,'bootstrap/css/bootstrap.css'),
}
