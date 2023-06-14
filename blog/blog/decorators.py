# https://stackoverflow.com/a/71002410

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.contrib.auth.decorators import login_required as django_login_required
from django.http import HttpResponse
from functools import wraps

from django.shortcuts import resolve_url

def login_required(function=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated and request.htmx:
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return HttpResponse(status=204, headers={'HX-Redirect': resolved_login_url})
        return django_login_required(
            function=function,
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )(request, *args, **kwargs)
    return wrapper