import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('V2RAYUI_SECRET_KEY', '&%up9@!s_$$4(qurnori=vit2#kg!bzs$_+m64^j$2-vzibx&p')

# 新用户默认等级
DEFAULT_LEVEL = 1

# 默认每个用户可生成的邀请码数量
INVITE_CODE_NUM = 5

# 邀请码默认过期时间（天）
INVITE_CODE_EXPIRE_DAYS = 3

# 默认用户每月总流量(GB)，0为不限制流量
DEFAULT_TRAFFIC = 0

# 客户端版本和名称以及iOS客户端的AppleID
CLIENTS = {
    "windows": {
        "client_name": "v2rayN",
        "version": "v1",
        "file_name": "v2rayN.zip"
    },
    "android": {
        "client_name": "v2rayNG",
        "version": "v1",
        "file_name": "v2rayNG.apk"
    },
    "macos": {
        "client_name": "v2rayU",
        "version": "v1",
        "file_name": "v2rayX.dmg"
    },
    "ios": {
        "client_name": "Shadowrocket",
        "apple_id": os.environ.get('V2RAYUI_APPLE_ID', 'Apple ID账号未设置'),
        "apple_id_pwd": os.environ.get('V2RAYUI_APPLE_ID_PWD', 'Apple ID密码未设置'),
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('V2RAYUI_DEBUG', True)

# 定时任务
CRONJOBS = [
    ('*/1 * * * *', 'v2rayui.cornjobs.demo')
]

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'v2rayui.apps.V2RayuiConfig',
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

ROOT_URLCONF = 'v2rayui.urls'

AUTH_USER_MODEL = 'v2rayui.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'v2rayui.db'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
