from .base import *

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hirou_develop',
        'USER': 'hirou_admin',
        'PASSWORD': 'Jer7ko3V3cD',
        'HOST': 'hirou-develop.cvyp954hzdcd.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    },
}

REDIS_PUBLIC_DNS = "hirou-redis-develop-us-east-2c.jsgffk.0001.use2.cache.amazonaws.com"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_PUBLIC_DNS, 6379)],
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
