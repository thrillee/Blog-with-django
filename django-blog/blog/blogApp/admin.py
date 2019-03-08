from django.contrib import admin
from .models import *

admin.site.register(Comment)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','category','slug','author','status','created_at')
    list_filter = ('created_at','status', 'publish', 'author')
    search_fields = ('title','author')
    prepopulated_fields = {'slug':('title',)}
    #raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)
