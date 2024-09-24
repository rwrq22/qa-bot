from django.urls import path
from . import views

urlpatterns = [
    path("messages", views.Messages.as_view()),
]
