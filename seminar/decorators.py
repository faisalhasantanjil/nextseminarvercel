from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
import time


def is_organization(user):
    #print(user.id)
    authorize = Organization.objects.filter(user=user.id)
    #print(authorize)
    if authorize:
        return True
    return False


def is_user(user):
    authorize = UserInformation.objects.filter(user=user.id)
    print("authorize: ")
    print(authorize)
    if authorize:
        return True
    return False


def organization_access_only():
    def decorator(view):
        @wraps(view)
        def _wreapped_view(request, *args, **kwargs):
            if not is_organization(request.user):
                return HttpResponse("You are Not Allowed to access this page")
            return view(request, *args, **kwargs)
        return _wreapped_view
    return decorator


def user_access_only():
    def decorator(view):
        @wraps(view)
        def _wreapped_view(request, *args, **kwargs):
            if not is_user(request.user):
                return HttpResponse("You are Not Allowed to access this page")
            return view(request, *args, **kwargs)
        return _wreapped_view
    return decorator
