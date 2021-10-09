from .base import *

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
] + os.getenv("DJANGO_ALLOWED_HOSTS", [])


DEBUG = os.getenv("DEBUG")

if DEBUG:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        INSTALLED_APPS.append("debug_toolbar")
        INTERNAL_IPS = ["127.0.0.1"]
        MIDDLEWARE.insert(
            MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        )
