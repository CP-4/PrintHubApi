from django.contrib import admin
from .models import Document, CustomUser, UrlAnalytics, GuestStudent

# Register your models here.

admin.site.register(Document)
admin.site.register(CustomUser)
admin.site.register(GuestStudent)
admin.site.register(UrlAnalytics)
