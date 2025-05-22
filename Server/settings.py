from datetime import timedelta
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m0pemz_xbqu%v&b1l332_$_g11t+yek*z$5m63!ou+!c$r6n3a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Parties 
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',

    # Custom-Apps
    'Users.apps.UsersConfig',
    'Profiles.apps.ProfilesConfig',
    'Addresses.apps.AddressesConfig',
    'Companies.apps.CompaniesConfig',
    'Services.apps.ServicesConfig',
    'Industries.apps.IndustriesConfig',
    'Scores.apps.ScoresConfig',
    'Authentication.apps.AuthenticationConfig',
    'Invoices.apps.InvoicesConfig',
    'Payments.apps.PaymentsConfig',
    'Accounts.apps.AccountsConfig',
    'OneTimePasswords.apps.OnetimepasswordsConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'Server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

CORS_ALLOW_ALL_ORIGINS = True

# Auth user model
AUTH_USER_MODEL = "Users.User"

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


# Rest framework
REST_FRAMEWORK = {
    #  Authentications classes
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# JWT settings
SIMPLE_JWT = {
    #  Tokens life time
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    
    #  Refresh tokens
    'ROTATE_REFRESH_TOKENS': True,
    
    # Blacklist 
    'BLACKLIST_AFTER_ROTATION': True,
    
    # Last Login refreshing
    'UPDATE_LAST_LOGIN': True,
    
    # Algorithm
    'ALGORITHM': 'HS256',
    
    # Verifying key 
    'VERIFYING_KEY': None,
    
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    
    # Headers 
    'AUTH_HEADER_TYPES': ('Bearer',),     # Header type
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',   # Header name
    
    # User id setting
    'USER_ID_FIELD': 'id',         # Field
    'USER_ID_CLAIM': 'user_id',    # Claim
    
    #  Auth rules settings
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    # Auth token classes and settings
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    
    #  Sliding settings
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # Token sliding lifetime
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


# SANDBOX MODE
MERCHANT = "00000000-0000-0000-0000-000000000000"
SANDBOX = False

if SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

# URL for sending a payment request
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"

# URL for verifying the transaction
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"

# URL for starting the payment (we’ll append the authority as a query parameter)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8080/payments/zarinpal-verify//'  # Your callback URL



# settings.py

# Jazzmin configuration
JAZZMIN_SETTINGS = {
    # Site title appearing in the window/tab title
    "site_title": "Komak Resan | مدیریت",
    
    # Header text shown above the Django admin’s logo
    "site_header": "Komak Resan",
    
    # Brand name for the side menu – often the same as the site header
    "site_brand": "Komak Resan",
    
    # Welcome text on the login screen
    "welcome_sign": "خوش آمدید به Komak Resan",
    
    # Copyright string (usually includes the current year)
    "copyright": "© 2025 Komak Resan",
    
    # Whether to show the UI builder link in the admin header
    "show_ui_builder": True,
    
    # Controls how the change form lays out the fields. Options include "vertical", "horizontal_tabs" or "collapsible"
    "changeform_format": "horizontal_tabs",
    
    # The language code for the admin interface – "fa" for Persian
    "language_code": "fa",
    
    # Whether to load Google Fonts from a CDN. Set to False if you prefer local fonts
    "use_google_fonts_cdn": False,
    
    # Enable RTL (right-to-left) support for Persian
    "rtl": True,
    
    # Optional: You can also specify a theme URL to use your own custom CSS
    "theme_url": None,
    
    # Icon classes mapping (optional customization)
    "icons": {
        "auth": "fas fa-users",
        "Sites": "fas fa-globe",
        "Invoices": "fas fa-file-invoice-dollar",
        "Users": "fas fa-user",
    },
}

# Optional: UI tweaks allow you to fine-tune the appearance of various parts of Jazzmin
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_colour": "#3c8dbc",  # Blue shade for the brand area
    "accent_colour": "#d2d6de",  # Default accent colour
    "navbar_colour": "navbar-dark bg-primary",  # Navbar styling – dark navbar with primary background
    "no_padding": False,
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_animation_speed": 300,  # Speed of sidebar animations (in ms)
    "sidebar_nav_icon_style": "fa fa-fw",  # Icon style for the sidebar
}
