from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import TreeProfile, TreePhoto


@admin.register(TreeProfile)
class TreeProfileAdmin(ModelAdmin):
    list_display = (
        "street_name",
        "scientific_name",
        "habitat",
        "verified",
        "submitted_by",
        "created_at",
    )
    list_filter = ("verified", "rarity_status", "habitat")
    search_fields = ("street_name", "scientific_name", "habitat")
    ordering = ("-created_at",)


@admin.register(TreePhoto)
class TreePhotoAdmin(ModelAdmin):
    list_display = (
        "tree",
        "caption",
        "uploaded_at",
    )
    search_fields = ("tree__street_name", "caption")
    ordering = ("-uploaded_at",)
