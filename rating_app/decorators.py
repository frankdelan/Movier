from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from functools import wraps
from typing import Callable


def rate_film_required(func: Callable):
    @wraps(func)
    def wrapper(request) -> HttpResponse | HttpResponseRedirect:
        if request.GET.get('title') or request.method == 'POST':
            return func(request)
        else:
            return HttpResponseRedirect(reverse('movies:create_page'))
    return wrapper

