from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import TreeProfile, TreePhoto, TreeRequest
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

admin.site.register([TreeRequest])

@admin.register(TreeProfile)
class TreeProfileAdmin(ModelAdmin, ImportExportModelAdmin):
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
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(TreePhoto)
class TreePhotoAdmin(ModelAdmin):
    list_display = (
        "tree",
        "caption",
        "uploaded_at",
    )
    search_fields = ("tree__street_name", "caption")
    ordering = ("-uploaded_at",)

    
