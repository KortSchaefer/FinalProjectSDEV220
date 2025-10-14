from django.contrib import admin
from .models import Server, Section, Outwork, Sidework, Host, Sa


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sectionAssigned", "timeIn", "hoursScheduled")
    search_fields = ("id", "name", "sectionAssigned")
    ordering = ("name",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("Section_ID", "Tables", "Guest_count", "Expected_in_time", "Section_score")
    search_fields = ("Section_ID", "Tables", "Guest_count")
    ordering = ("Section_ID",)


@admin.register(Outwork)
class OutworkAdmin(admin.ModelAdmin):
    list_display = ("Outwork_ID", "section", "Outwork_label", "Outwork_difficulty")
    search_fields = ("Outwork_ID", "Outwork_label")
    ordering = ("Outwork_ID",)


@admin.register(Sidework)
class SideworkAdmin(admin.ModelAdmin):
    list_display = ("Sidework_ID", "section", "Sidework_label", "Sidework_difficulty")
    search_fields = ("Sidework_ID", "Sidework_label")
    ordering = ("Sidework_ID",)

@admin.register(Host)
class hostAdmin(admin.ModelAdmin):
    list_display = ("Host_ID", "Host_name")
    search_fields = ("Host_ID", "Host_name")
    ordering = ("Host_ID",)

@admin.register(Sa)
class saAdmin(admin.ModelAdmin):
    list_display = ("sa_ID", "sa_name")
    search_fields = ("sa_ID", "sa_name")
    ordering = ("sa_ID",)


