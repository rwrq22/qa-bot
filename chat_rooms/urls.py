from django.urls import path
from . import views

urlpatterns = [
    path("room", views.ChatRooms.as_view()),
    path("sentry-debug", views.trigger_error),
]
