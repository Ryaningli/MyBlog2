from django.urls import path


def api_path(url, *args, **kwargs):
    return path('api/' + url, *args, **kwargs)