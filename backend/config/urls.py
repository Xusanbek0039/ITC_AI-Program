"""
URL configuration for ITC AI Program project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path("api/chat/", include("apps.chat.urls")),
    path("api/openai/", include("apps.openai_service.urls")),
]
