# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include,re_path # add this

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    re_path(r'^chaining/', include('smart_selects.urls')), # django-smart-selects
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),             # UI Kits Html files
    path('tinymce/', include('tinymce.urls')),
    path('api/', include('apps.api.urls')),  # API routes
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

