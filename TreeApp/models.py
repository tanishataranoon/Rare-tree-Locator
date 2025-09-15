from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class TreeProfile(models.Model):
    # Basic info
    street_name = models.CharField(max_length=200)  # common/local name
    scientific_name = models.CharField(max_length=200, blank=True, null=True)
    habitat = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6)   # e.g., 23.810331
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # e.g., 90.412521

    # Extra attributes
    rarity_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="e.g., Common, Rare, Endangered"
    )
    height_m = models.DecimalField(
        max_digits=5, decimal_places=2,
        blank=True, null=True,
        help_text="Approximate height in meters"
    )
    age_estimate = models.PositiveIntegerField(
        blank=True, null=True,
        help_text="Estimated age in years"
    )
    verified = models.BooleanField(default=False)

    # Relations
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="trees_submitted"
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trees_approved"
    )

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street_name} ({self.scientific_name or 'Unknown'})"


class TreePhoto(models.Model):
    tree = models.ForeignKey(TreeProfile, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="tree_photos/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.tree.street_name}"
