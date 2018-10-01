from django.contrib import admin

from .models import SearchKeyword, YTVideo


class YTVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')


admin.site.register(SearchKeyword)
admin.site.register(YTVideo, YTVideoAdmin)
