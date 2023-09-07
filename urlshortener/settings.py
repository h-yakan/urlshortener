"""
Django settings for urlshortener project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=$!+_km9d&-*j69-1otmx8%jpqva#pb2)n51v3&mfzys8fxo3c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','159.253.36.173']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',#allauth için gerekli
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',#allauth için gerekli
    'django.contrib.staticfiles',
    'django.contrib.sites',#allauth için gerekli
    #Benim uygulamalarım
    'shortenerapp',
    #3.Parti Uygulamalar
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap4',
    'django_celery_beat',
    'django_celery_results',
    'celery'
]
SITE_ID = 1
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urlshortener.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
    'templates',
    ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',#allauth için gerekli
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'urlshortener.wsgi.application'

AUTHENTICATION_BACKENDS = [#AllAuth
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    ]
    


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'urlshortener',
        'USER': 'urlshortener',
        'PASSWORD': 'mmoS689ahWkOR2z',
        'HOST': 'localhost',
        'PORT': '',
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

LANGUAGE_CODE = 'tr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'staticfiles'),
]
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_STORAGE_BUCKET_NAME = 'urlshortener-static'

AWS_ACCESS_KEY_ID = 'Rq4i6iwNzE3hmYmi6ODS'
AWS_SECRET_ACCESS_KEY = 'JLDXVXbrkSBRQRrqsN4BcRdpbQJkMr91PZ7yPfav'
AWS_S3_ENDPOINT_URL = 'http://159.253.36.173:9000'
#STATIC_ROOT=os.path.join(BASE_DIR,'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/accounts/login'

ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_CONFIRM_EMAIL_ON_GET = True

ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL

# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER",'redis://localhost:6379/0')

# CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER",'redis://localhost:6379/0')


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER",'redis://127.0.0.1:6379/0')

CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER",'redis://127.0.0.1:6379/0')

CELERY_ACCEPT_CONTENT = ['application/json']  

CELERY_TASK_SERIALIZER = 'json'  

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# CELERY_BEAT_SCHEDULE = { # scheduler configuration 
#      'countdown_schedule' : {  # whatever the name you want 
#          'task': 'urlshortener.tasks.countdown', # name of task with path
#          'schedule': crontab(minute=1,hour=0), # crontab() runs the tasks every minute
#      },
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

ACCOUNT_EMAIL_REQUIRED = True 
ACCOUNT_UNIQUE_EMAIL = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587 
EMAIL_HOST_USER = 'huseyin.yakan.sd@gmail.com'  #new
EMAIL_HOST_PASSWORD = "obhfymxexdlfidld" #new
EMAIL_USE_TLS = True #new   

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_FORMS = {
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
    'login': 'allauth.account.forms.LoginForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'signup': 'allauth.account.forms.SignupForm',
    'user_token': 'allauth.account.forms.UserTokenForm',
}
