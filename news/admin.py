from django.contrib import admin
from .models import Post, Author, Comment, Category, PostCategory
# Register your models here.

admin.site.register(
    (Post,
     Author,
     Comment,
     Category,
     PostCategory
     )
)