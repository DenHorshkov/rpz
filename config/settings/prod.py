"""Production settings: HTTPS-ready, hardened."""
from .base import *  # noqa: F401,F403
from .base import env

DEBUG = False

# HTTPS-ready: умикається через DJANGO_ENABLE_HTTPS=1, коли проєкт стоїть за HTTPS-проксі.
# Локальний docker-compose використовує HTTP, тому за замовчуванням флаги вимкнено.
ENABLE_HTTPS = env.bool("DJANGO_ENABLE_HTTPS", default=False)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = ENABLE_HTTPS
SESSION_COOKIE_SECURE = ENABLE_HTTPS
CSRF_COOKIE_SECURE = ENABLE_HTTPS
SECURE_HSTS_SECONDS = 31_536_000 if ENABLE_HTTPS else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = ENABLE_HTTPS
SECURE_HSTS_PRELOAD = ENABLE_HTTPS
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
