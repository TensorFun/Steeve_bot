"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from steevebot.views import Hello, text_CV, pdf_CV, recruit_post, random_job, all_job

urlpatterns = [
    path('api/admin/', admin.site.urls),
    re_path(r'^api/fb_mybot/', include('steevebot.urls')),
    path('api', Hello),
    path('api/CV/text', text_CV),
    path('api/CV/pdf', pdf_CV),
    path('api/Recruit', recruit_post),
    path('api/random', random_job),
    path('api/all', all_job),
]

