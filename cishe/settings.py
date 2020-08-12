"""
Django settings for cishe project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from datetime import timedelta

import environ


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# with `env_file is not None` `os.environ._data.PWD` is BASE_DIR
env.read_env(env.str("ENV_PATH", default=".env"))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

# environ.Path()() is the folder where `os.environ._data.PWD` is
BASE_DIR = environ.Path()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "phonenumber_field",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "cishe.account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cishe.api.middleware.VersionSwitch",
]

ROOT_URLCONF = "cishe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cishe.wsgi.application"

# monkey patch for pymysql as db level
try:
    import pymysql

    pymysql.version_info = (1, 4, 6, "final", 0)  # change mysqlclient version
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # BASE_DIR('db.sqlite3') => /path/to/BASE_DIR/db.sqlite3
    # we need `four slashes` as sqlite scheme to work
    # so `three slashes` ahead
    "default": env.db_url(
        "DATABASE_URL", default="sqlite:///" + BASE_DIR("db.sqlite3")
    ),
}

CACHES = {
    "default": env.cache_url(
        "CACHE_URL", default="locmemcache://snow-flake?timeout=300&max_entries=1000"
    )
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

TEST_RUNNER = "cishe.tests.runner.PytestTestRunner"

# refer to
#   https://medium.com/frochu/libphonenumber-example-app-f60680faa599
# E164 : +886920123456
# INTERNATIONAL : +886 920 123 456
# NATIONAL : 0920 123 456
# RFC3966 : 920 123 456

# using `E164` will be more db efficient
PHONENUMBER_DB_FORMAT = "E164"
# https://46elks.com/kb/country-codes
PHONENUMBER_DEFAULT_REGION = "CN"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
        "rest_framework_simplejwt.tokens.SlidingToken",
    ),
    "TOKEN_TYPE_CLAIM": "token_type",
    # The "jti" (JWT ID) claim provides a unique identifier for the JWT
    # for blacklist app mostly, for revoking issued JWT
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}
