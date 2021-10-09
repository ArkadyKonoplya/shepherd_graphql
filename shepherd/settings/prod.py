from .base import *

ALLOWED_HOSTS = ["www.shepherdfarming.com"] + os.getenv("DJANGO_ALLOWED_HOSTS", [])

DEBUG = os.getenv("DEBUG")
