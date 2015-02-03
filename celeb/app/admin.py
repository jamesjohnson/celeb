from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin

from .models import Publication, Article, Celebrity


admin.site.register(Publication, admin.ModelAdmin)
admin.site.register(Article, admin.ModelAdmin)
admin.site.register(Celebrity, admin.ModelAdmin)
