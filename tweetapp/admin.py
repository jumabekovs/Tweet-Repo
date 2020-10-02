from django.contrib import admin

from .models import *


class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    fields = ('author', 'text', 'image')
    readonly_fields = ['created_at', 'likes']
    inlines = [CommentInline, ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, Follow)
admin.site.register(Tag, Like)