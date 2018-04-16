from django.urls import re_path
from .views import MyBotView

urlpatterns = [
    re_path(r'^callback/?$', MyBotView.as_view()),
]

