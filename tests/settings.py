import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = "38dh*skf8sjfhs287dh&^hd8&3hdg*j2&sd"
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

INSTALLED_APPS = [

]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tests/templates')],
        'APP_DIRS': False,
    }
]
