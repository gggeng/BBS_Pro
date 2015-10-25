from django.contrib import admin
from app01 import models

# Register your models here.
class BBS_admin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'author', 'view_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'author__user__username',)

    #def signature(self, obj):
    #    return obj.author.singature
    #signature.short_description = 'haha'

class Category_admin(admin.ModelAdmin):
    list_display = ('name')

admin.site.register(models.BBS, BBS_admin)
admin.site.register(models.Category)
admin.site.register(models.BBS_user)