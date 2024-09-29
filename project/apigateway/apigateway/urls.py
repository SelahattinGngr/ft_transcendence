from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<path>.*)$', views.proxy_request),
]
