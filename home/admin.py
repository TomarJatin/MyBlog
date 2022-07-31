from django.contrib import admin
from .models import Blog, ContactModel, BlogComment

admin.site.register((Blog, ContactModel, BlogComment))