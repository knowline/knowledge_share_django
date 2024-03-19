"""
Django settings for knowledge_share_project project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import mimetypes
import os

from pathlib import Path
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticFiles')
STATIC_URL = '/static/'
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/html', '.js')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_6t8%4fh3aa%9p5$562y)922e(@2q(%&pjd61f$8&jj0-q)+qy'
SESSION_COOKIE_AGE = 3600  # 一小时后session失效，需要再次登陆
SESSION_SAVE_EVERY_REQUEST = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']

# Application definition
# django.contrib.auth.model.USER是django授权系统的核心。用户对象呈现着个人与一个djano程序的交互。
# 用户对象可以有以下授权的方面：访问限制、注册新用户、创建网站内容等。用户有5个关健属性：
# username\password\email address\first name\surname.用户也有其他属性如：
# is_active\is_staff\is_superuser。可查看官方文档进一步了解基本的用户模型base User model。
# 如果想添加自己的用户属性，需要在rango's model.py文件修改。
INSTALLED_APPS = [
	'django.contrib.admin',  # 添加管理员应用
	'django.contrib.auth',  # 认证系统
	'django.contrib.contenttypes',  # 内容类型框架
	'django.contrib.sessions',  # 会话管理
	'django.contrib.messages',  # 消息框架
	'django.contrib.staticfiles',  # 管理静态文件（CSS, JavaScript, 图片）
	'django_bootstrap5',  # Bootstrap 5 集成
	'registration',  # 用户注册
	'rango',  # 自定义应用 'rango'
]

# MIDDLEWARE_CLASSES = [
#     'django.middleware.security.SecurityMiddleware',   
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',  
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',

# ]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# 'django.middleware.csrf.CsrfResponseMiddleware'
]

ROOT_URLCONF = 'knowledge_share_project.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [TEMPLATE_DIR],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'django.template.context_processors.media',
			],
		},
	},
]

WSGI_APPLICATION = 'knowledge_share_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# Password hashing functions
# django自带的auth app默认存储用户密码的hash使用PBKDF2算法，为你的用户的数据提供好的安全级别的保护。
# 然而如果你想控制更多的密码的哈希值，可以使用setting.py模块来改变方式-通过增加到元组tuple来
# 指定PASSWORD_HASHERS。django认为指定哈希的顺序是重要的，并将选择并使用第一个密码的哈希值（在PASSWORD_HASHERS)
# 如，settings.PASSWORD_HASHERS[0]。他们是依次向下使用，如果第一个啥希失效则往下一个。
# 如果你想要使用更安全的哈希值，可以pip install bcrypt，然后设置它的哈希。
# https://docs.djangoproject.com/en/1.9/topics/auth/passwords/#how-django-stores-passwords
# 以下为元组
PASSWORD_HASHERS = [
	'django.contrib.auth.hashers.PBKDF2PasswordHasher',
	'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
# django有预制的密码验证用于普通的密码检测，如长度。
# 以下为嵌套的字典
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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# chap 11 user authentiation with ..redux..
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
# 用户登录后应该重定向的网址
LOGIN_REDIRECT_URL = '/rango/'
# 黑夜用户登录网址
# LOGIN_URL = '/accounts/login/'
LOGIN_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_CONTENT_TYPE_NOSNIFF = False
