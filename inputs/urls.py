from django.urls import path
from . import views

urlpatterns = [
    path("inputs", views.Inputs.as_view()),
]
