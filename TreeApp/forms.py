from django.http import JsonResponse
from .models import *
from django import forms
from .models import TreeRequest, TreeAnswer

def add_tree_ajax(request):
    if request.method == "POST":
        street_name = request.POST.get('street_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if street_name and latitude and longitude:
            tree = TreeProfile.objects.create(
                street_name=street_name,
                scientific_name=request.POST.get('scientific_name'),
                habitat=request.POST.get('habitat'),
                description=request.POST.get('description'),
                rarity_status=request.POST.get('rarity_status'),
                height_m=request.POST.get('height_m') or None,
                age_estimate=request.POST.get('age_estimate') or None,
                latitude=latitude,
                longitude=longitude,
                submitted_by=request.user
            )
            return JsonResponse({
                "success": True,
                "street_name": tree.street_name,
                "description": tree.description or "",
                "latitude": tree.latitude,
                "longitude": tree.longitude
            })
        return JsonResponse({"success": False, "error": "Missing required fields"})
    return JsonResponse({"success": False, "error": "Invalid request"})

# Common user request form
class TreeRequestForm(forms.ModelForm):
    class Meta:
        model = TreeRequest
        fields = ["title", "description", "location", "image"]


# Contributor answer form
class TreeAnswerForm(forms.ModelForm):
    class Meta:
        model = TreeAnswer
        fields = ["response_text", "reference_image", "video_url", "external_url"]
        widgets = {
            "response_text": forms.Textarea(attrs={"placeholder": "Provide your expert identification and any additional information..."}),
        }