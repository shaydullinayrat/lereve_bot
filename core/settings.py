"""
Django settings for lereve_bot project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1',
                 '0.0.0.0',
                 '195.161.68.242',
                 'localhost',
                 'lrv.davam.online',
                 'mindskills.fun',
                 'e23dd8c01b8f.vps.myjino.ru']
# ALLOWED_HOSTS = ['*']
# Application definition
ALLOWED_HOSTS = ['a5ce8a79a634.vps.myjino.ru', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.bot',
    'apps.management',
    'apps.clients',
    'apps.instructions',
    'apps.shops',
    'apps.bonuses',
    'django_celery_beat',
    'django_celery_results',
    'aiogram_bot',
    'django.contrib.postgres',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / f'{DB_NAME}db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'django_postgres_async.backend',
        # 'HOST': os.environ.get('DB_HOST'),
        'HOST': 'localhost',
        'USER': 'lereve_user',
        'NAME': 'lereve_db',
        'PASSWORD': 'MLl!8)co37Oo',
        'PORT': '5432',
        # 'NAME': os.environ.get('DB_NAME'),
        # 'USER': os.environ.get('DB_USER'),
        # 'NAME': os.environ.get('DB_HOST'),
        # 'NAME': f'{DB_NAME}',
        # 'USER': f'{DB_USER}',
        # 'PASSWORD': os.environ.get('DB_PASS'),
        # 'OPTIONS': {
        #     'unix_socket': '/var/run/postgresql'  # Убедитесь, что путь совпадает
        # },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

# Относительный путь для хранения собранных статических файлов
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Дополнительно: пользовательские директории со статическими файлами
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles/'),  # Например, директория для пользовательской статики
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

ASGI_APPLICATION = "core.asgi.application"

REDIS_HOST = 'localhost'

# Redis как бэкенд и брокер для Celery
# CELERY_BROKER_URL = 'redis://redis:6379/0'
# CELERY_RESULT_BACKEND = 'redis://redis:6379/0'


CELERY_BROKER_URL = f'redis://{REDIS_HOST}:6379/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:6379/0'

REDIS_PORT = 6379

CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# INSTALLED_APPS += [
#     'django_celery_results',
#     'django_celery_beat',
# ]

CELERY_IMPORTS = (
    'aiogram_bot.tasks',
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TOKEN_BOT = env.str('TOKEN_BOT')
TELEGRAM_MANAGER_ID = env.str('TELEGRAM_MANAGER_ID')
TELEGRAM_CARE_SERVICE_ID = env.str('TELEGRAM_CARE_SERVICE_ID')
TELEGRAM_CARE_SERVICE_USERNAME = env.str('TELEGRAM_CARE_SERVICE_USERNAME')
TELEGRAM_MANAGER_USERNAME = env.str('TELEGRAM_MANAGER_USERNAME')

WB_FEEDBACK_API_URL = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
WB_API_TOKEN = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQxMTE4djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc0Nzk4NDE3MiwiaWQiOiIwMTkzNTAyMS0zMDFiLTdmMTktOTIxZC04OTM1YTBkMjVlNmMiLCJpaWQiOjIzMDc5MDM0LCJvaWQiOjg1MTY4LCJzIjo3OTM0LCJzaWQiOiI5NzdjODVkZC04ZGZjLTU4MGQtODU5Mi0yMGM3ZmQ5ZGRlZWYiLCJ0IjpmYWxzZSwidWlkIjoyMzA3OTAzNH0.GuYZF4tq--_6TLXYR7S-gdueHWcvz3hWY6-s9fNctFgazbZsJykZWVpsiWrYfE3146jDODSjkDYLwC1UYSbjOg'

FEEDBACK_REVIEW_DATE_CHECK_MINUTES = 60
FEEDBACK_REVIEW_DATE_CHECK_DAYS = 30
