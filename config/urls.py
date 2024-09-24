from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("ad/", admin.site.urls),
    path("api/v1/", include("chat_messages.urls")),
    path("api/v1/", include("inputs.urls")),
]
