from django.contrib import admin

from .models import Job, PL, User

# Register your models here.

admin.site.register(Job)
admin.site.register(PL)
admin.site.register(User)
