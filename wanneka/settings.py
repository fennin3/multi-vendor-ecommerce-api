import os
from corsheaders.defaults import default_headers
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

# load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# env = environ.Env(
#     DEBUG=(bool, False)
# )
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = "$nerdthejohn-=fz_7q70^d+dhu9pp_^tufaqw!#6y_67ht@2tnr)yru!ksid&@"
        
DEBUG = True

ALLOWED_HOSTS = ['*']




AUTH_USER_MODEL = 'vendor.CustomUser'

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': [
         'rest_framework.permissions.IsAuthenticated',
        ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    #  'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
     ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

INSTALLED_APPS = [
    "vendor",
    "customer",
    "administrator",
    "order",
    "product",
    "transactions",
    "blog",
    "coupons",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework",
    # External Libraries
    "storages",
    "solo",
    "django_filters",
    "corsheaders",
    # "import_export",

    # AUTH
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    

]


# JWT_AUTH = {
#   'JWT_PAYLOAD_HANDLER':
#   'rest_framework_jwt.utils.jwt_create_payload',
# #   'JWT_RESPONSE_PAYLOAD_HANDLER':
# #   'vendor.utils2.jwt_response_payload_handler',
#   'JWT_ENCODE_HANDLER':
#   'rest_framework_jwt.utils.jwt_encode_payload',
#   'JWT_DECODE_HANDLER':
#   'rest_framework_jwt.utils.jwt_decode_token',
# #   'JWT_PAYLOAD_HANDLER':
# #   'rest_framework_jwt.utils.jwt_payload_handler',
#   'JWT_PAYLOAD_GET_USERNAME_HANDLER':
#    'rest_framework_jwt.utils.jwt_get_username_from_payload_handler',
#   'JWT_PAYLOAD_GET_USER_ID_HANDLER':
#   'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
#   'JWT_RESPONSE_PAYLOAD_HANDLER':
#   'rest_framework_jwt.utils.jwt_response_payload_handler',
 
#   'JWT_SECRET_KEY': "$nerdthejohn*@querords_dmf8736fm284.!",
#   'JWT_GET_USER_SECRET_KEY': None,
#   'JWT_PUBLIC_KEY': None,
#   'JWT_PRIVATE_KEY': None,
#   'JWT_ALGORITHM': 'HS256',
#   'JWT_VERIFY': True,
#   'JWT_VERIFY_EXPIRATION': True,
#   'JWT_LEEWAY': 0,
#   'JWT_EXPIRATION_DELTA': timedelta(days=30),
#   'JWT_AUDIENCE': None,
#   'JWT_ISSUER': None,
#   'JWT_ALLOW_REFRESH': True,
#   'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),
#   'JWT_AUTH_HEADER_PREFIX': 'Bearer',
#   'JWT_AUTH_COOKIE': None,
# }

# JWT_AUTH = {
#     'JWT_SECRET_KEY': SECRET_KEY,
#     'JWT_GET_USER_SECRET_KEY': None,
#     'JWT_PRIVATE_KEY': None,
#     'JWT_PUBLIC_KEY': None,
#     'JWT_ALGORITHM': 'HS256',
#     'JWT_INSIST_ON_KID': False,
#     'JWT_TOKEN_ID': 'include',
#     'JWT_AUDIENCE': None,
#     'JWT_ISSUER': None,
#     'JWT_ENCODE_HANDLER':
#         'rest_framework_jwt.utils.jwt_encode_payload',
#     'JWT_DECODE_HANDLER':
#         'rest_framework_jwt.utils.jwt_decode_token',
#     'JWT_PAYLOAD_HANDLER':
#         'rest_framework_jwt.utils.jwt_create_payload',
#     'JWT_PAYLOAD_GET_USERNAME_HANDLER':
#         'rest_framework_jwt.utils.jwt_get_username_from_payload_handler',
#     'JWT_PAYLOAD_INCLUDE_USER_ID': True,
#     'JWT_VERIFY': True,
#     'JWT_VERIFY_EXPIRATION': True,
#     'JWT_LEEWAY': 0,
#     'JWT_EXPIRATION_DELTA': timedelta(days=365),
#     'JWT_ALLOW_REFRESH': True,
#     'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer',
#     'JWT_RESPONSE_PAYLOAD_HANDLER':
#         'rest_framework_jwt.utils.jwt_create_response_payload',
#     'JWT_AUTH_COOKIE': None,
#     'JWT_AUTH_COOKIE_DOMAIN': None,
#     'JWT_AUTH_COOKIE_PATH': '/',
#     'JWT_AUTH_COOKIE_SECURE': True,
#     'JWT_AUTH_COOKIE_SAMESITE': 'Lax',
#     'JWT_IMPERSONATION_COOKIE': None,
#     'JWT_DELETE_STALE_BLACKLISTED_TOKENS': False,
# }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=100),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=200),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'uid',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=100),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=200),
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wanneka.urls'

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
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wanneka.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Accra'



EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_PASSWORD = "xtioscgwkfkvqgpf"
EMAIL_HOST_USER="rennintech@gmail.com"
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST="smtp.gmail.com"
ACCOUNT_EMAIL_VERIFICATION = 'none'



AWS_ACCESS_KEY_ID = "AKIAWYU4GI3PAPB26JMB"  
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "wanneka-storage"
AWS_S3_FILE_OVERWRITE = False  
AWS_DEFAULT_ACL =  None
AWS_S3_REGION_NAME = "us-east-1"
AWS_QUERYSTRING_AUTH = True
AWS_S3_CUSTOM_DOMAIN = "cdn.wanneka.com"

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 

 

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Accra'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT  =   os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    '*',
] # If this is used, then not need to use 

CORS_ORIGIN_REGEX_WHITELIST = [
    "*"
]

CORS_ALLOWED_ORIGINS = ["https://*", "http://*"]

CORS_ORIGIN_ALLOW_ALL = True


if "DATABASE_URL" in os.environ:
    import dj_database_url

    DATABASES = {"default": dj_database_url.config()}


