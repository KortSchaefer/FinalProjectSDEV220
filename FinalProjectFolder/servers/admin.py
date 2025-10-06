from django.contrib import admin

from .models import Post, Server


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sectionAssigned", "timeIn", "hoursScheduled")
    search_fields = ("id", "name", "sectionAssigned")
    ordering = ("name",)


admin.site.register(Post)
