
import os
from pathlib import Path
from celery.schedules import crontab
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from datetime import timedelta
import dj_database_url

# Charger les variables d'environnement
load_dotenv()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


NEWS_API_KEY = os.getenv('NEWS_API_KEY')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') 

handler404 = 'home.views.custom_404' 
handler403 = 'home.views.custom_403'

ADMIN_SITE_HEADER = "InstaForum Administration"
ADMIN_SITE_TITLE = "InstaForum Admin Portal"
ADMIN_INDEX_TITLE = "Bienvenue sur le portail d'administration InstaForum"


ALLOWED_HOSTS = ["*"]



# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api',
    'modelUser',
    'home',
    'forum',
    'news',
    'events',
    'messaging',
    'resources',

    "anymail",
    'taggit',
    'channels',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django_filters',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# Configuration Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'


# Database
# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL')
#     )
# }

# # Redis
# REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
# # Celery
# CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL


CELERY_BEAT_SCHEDULE = {
    'fetch_and_store_news_every_5_minutes': {
        'task': 'news.tasks.fetch_and_store_news',
        'schedule': crontab(minute='*/30'),
        # 'args': (),  # Ajoutez des arguments si nécessaire
    },
    'fetch_and_active_suspended_user_2_min': {
        'task': 'modelUser.tasks.check_suspended_users',
        'schedule': crontab(minute=0, hour='*/7'),
        # 'args': (),  # Ajoutez des arguments si nécessaire
    },
}


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'x-csrftoken',
    'x-requested-with',
    
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
    'PATCH',
]

CORS_ALLOW_CREDENTIALS = True



SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
     'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
    
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]


ROOT_URLCONF = 'ForumInsta.urls'

ACCOUNT_ADAPTER = 'modelUser.adapter.MyAccountAdapter'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'forum.context_processors.notification_count',
            ],
        },
    },
]


DEFAULT_CHARSET = 'utf-8'

WSGI_APPLICATION = 'ForumInsta.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Ndjamena'
USE_I18N = True
USE_L10N = True
USE_TZ = True



LANGUAGES = [ 
    ('en', _('English')), 
    ('fr', _('Français')),
    ('ar', _('العربية')),  ]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL ='modelUser.User'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True 
ACCOUNT_USERNAME_REQUIRED = True  
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL ='/next'
ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL = 'account_profile' 

# Durée de session par défaut
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2  # 2 semaines
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# Durée de session prolongée pour "Se souvenir de moi"
ACCOUNT_SESSION_REMEMBER = True



# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
DEFAULT_FROM_EMAIL = "instaforum2025@gmail.com"

ANYMAIL = {
    "BREVO_API_KEY": os.getenv('BREVO_API_KEY'),
    "IGNORE_UNSUPPORTED_FEATURES": True,
}

AUTHENTICATION_BACKENDS = [
    'modelUser.authentication.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',  
    'allauth.account.auth_backends.AuthenticationBackend',]

ACCOUNT_FORMS = {
    'login': 'modelUser.forms.CustomLoginForm',
    'signup': 'modelUser.forms.CustomSignupForm',
    'reset_password': 'modelUser.forms.CustomResetPasswordForm',
    'change_password': 'modelUser.forms.CustomChangePasswordForm',
    'set_password': 'modelUser.forms.CustomSetPasswordForm',
}


ASGI_APPLICATION = 'ForumInsta.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)], 
        },
    },
}




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'encoding': 'utf-8', 
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'news': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'channels': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.channels': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}



INTERNAL_IPS = ['127.0.0.1']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}


JAZZMIN_SETTINGS = {
    # Titre et identité
    "site_title": "Insta pour nous",
    "site_header": "Administration",
    "site_brand": "InstaForum",
    "site_logo": None,  # Pas de logo
    "welcome_sign": "Bienvenue sur le portail d'administration InstaForum",
    "copyright": "abakarix4dev",
    
    # Thème Minty personnalisé
    "theme": "minty",
    "dark_mode_theme": None,
    
    # Couleurs et styles
    "theme_colors": {
        "primary": "#78c2ad",  # Vert Minty principal
        "secondary": "#f3969a",
        "info": "#6cc3d5",
        "warning": "#ffce67",
        "danger": "#ff7851",
        "success": "#56cc9d"
    },
    
    # Personnalisation de la sidebar (noire)
    "sidebar_navbar_color": "navbar-dark",
    "sidebar_navbar_style": "navbar-dark",
    "sidebar_bg_color": "#343a40",  # Fond noir
    "sidebar_text_color": "#ffffff",  # Texte blanc
    "sidebar_link_color": "#ffffff",
    "sidebar_link_hover_color": "#78c2ad",  # Vert Minty au survol
    
    # En-tête personnalisé
    "header_bg_color": "#78c2ad",  # Vert Minty
    "header_text_color": "#ffffff",  # Texte blanc
    
    # Boutons
    "button_classes": {
        "primary": "btn btn-primary bg-primary text-white",
        "secondary": "btn btn-secondary bg-secondary text-white",
        "info": "btn btn-info bg-info text-white",
        "warning": "btn btn-warning bg-warning text-dark",
        "danger": "btn btn-danger bg-danger text-white",
        "success": "btn btn-success bg-success text-white"
    },
    
    # Page d'accueil personnalisée (conservée)
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Voir le site", "url": "/", "new_window": True},
        {"app": "auth", "name": "Utilisateurs"},
        {"model": "auth.User"},
    ],
    
    # Organisation des modèles (conservée)
    "order_with_respect_to": ["auth", "blog", "media", "comments"],
    "icons": {
        "allauth.Account": "fas fa-user-circle",
        "allauth.EmailAddress": "fas fa-envelope",
        "allauth.SocialAccount": "fas fa-share-alt",
        "django_celery_beat.PeriodicTask": "fas fa-tasks",
        "django_celery_beat.IntervalSchedule": "fas fa-clock",
        "django_celery_beat.CrontabSchedule": "fas fa-calendar-alt",
        "taggit.Tag": "fas fa-tag",
        "taggit.TaggedItem": "fas fa-tags",
        "sites.Site": "fas fa-globe",
        "redirects.Redirect": "fas fa-forward",
        "flatpages.FlatPage": "fas fa-file",
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "forum.Category": "fas fa-folder",
        "forum.Subforum": "fas fa-comments", 
        "forum.Thread": "fas fa-comment-dots",
        "forum.Post": "fas fa-comment", 
        "forum.Report": "fas fa-flag", 
        "forum.Notification": "fas fa-bell", 
        "forum.UserBadge": "fas fa-award",  
        "modelUser.User": "fas fa-user-tie",  
        "resources.Resource": "fas fa-file-alt", 
        "messaging.Message": "fas fa-envelope",
        "events.Event": "fas fa-calendar-alt",
        "events.Attendee": "fas fa-user-check", 
    },
    
    # Menus personnalisés (conservés)
    "menu": [
        {
            "name": "Utilisateurs",
            "icon": "fas fa-users",
            "models": [
                "auth.User",
                "auth.Group",
                "accounts.Profile",
            ]
        },
        {
            "name": "Contenu",
            "icon": "fas fa-newspaper",
            "models": [
                "blog.Post", 
                "blog.Category"
            ]
        },
        {
            "name": "Médias",
            "icon": "fas fa-photo-video",
            "models": [
                "media.Image",
                "media.Video"
            ]
        },
        {
            "name": "Interactions",
            "icon": "fas fa-comments",
            "models": [
                "comments.Comment",
                "likes.Like"
            ]
        },
        {
            "name": "Statistiques",
            "url": "admin:stats_dashboard",
            "icon": "fas fa-chart-line",
        },
    ],
    
    # Tableau de bord (conservé)
    "dashboard_widgets": [
        {
            "type": "recent_actions",
            "limit": 10,
            "title": "Actions récentes"
        },
        {
            "type": "model_list",
            "title": "Création rapide",
            "models": ["blog.Post", "media.Image", "comments.Comment"]
        },
        {
            "type": "chart",
            "title": "Activité du site",
            "url": "admin:site_activity_chart"
        },
        {
            "type": "html",
            "title": "Infos & Documentation",
            "content": """
            <p>Bienvenue sur le panneau d'administration InstaForum.</p>
            <ul>
                <li><a href="/docs/admin/" target="_blank">Documentation</a></li>
                <li><a href="https://github.com/abakarix4dev/instaforum" target="_blank">Code source</a></li>
            </ul>
            """
        },
    ],
    
    # Autres paramètres (conservés)
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["authtoken", "token_blacklist"],
    "related_modal_active": True,
    "actions_sticky_top": True,
    "custom_buttons": [
        {
            "name": "Exporter en CSV",
            "action": "export_as_csv",
            "classes": "btn btn-success bg-success text-white",
            "icon": "fas fa-file-csv",
        }
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "minty",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-success"
    }
}