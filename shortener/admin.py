from django.contrib import admin
from .models import UrlMap, UrlProfile


class UrlMapAdmin(admin.ModelAdmin):
    model = UrlMap
    raw_id_fields = (
        "user",
    )
    list_display = (
        "short_url",
        "user",
        "usage_count",
        "max_count",
        "lifespan",
        "date_created",
        "date_expired",
        "full_url",
    )
    search_fields = (
        "short_url",
        "full_url",
        "user__username",
    )


class UrlProfileAdmin(admin.ModelAdmin):
    model = UrlProfile
    raw_id_fields = (
        "user",
    )
    list_display = (
        "user",
        "enabled",
        "max_urls",
        "max_concurrent_urls",
        "default_lifespan",
        "default_max_uses",
    )
    list_filter = (
        "enabled",
    )
    search_fields = (
        "user__username",
    )


# Register your models here.
admin.site.register(UrlMap, UrlMapAdmin)
admin.site.register(UrlProfile, UrlProfileAdmin)
