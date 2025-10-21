from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from MyApp.models import User, Profile
from django.contrib.auth import get_user_model
from django.db import migrations
from urllib.parse import urlparse, parse_qs


def fix_null_treeanswers(apps, schema_editor):
    TreeAnswer = apps.get_model("TreeApp", "TreeAnswer")
    User = apps.get_model("auth", "User")

    try:
        default_user = User.objects.get(username="admin")  # replace with a real user
    except User.DoesNotExist:
        return

    # Fill missing answered_by
    TreeAnswer.objects.filter(answered_by__isnull=True).update(answered_by=default_user)

    # Fill missing response_text
    TreeAnswer.objects.filter(response_text__isnull=True).update(response_text="No response provided")

class Migration(migrations.Migration):

    dependencies = [
        ('TreeApp', 'previous_migration_name'),  # replace with your last migration
    ]

    operations = [
        migrations.RunPython(fix_null_treeanswers),
    ]




#tree profile model
class TreeProfile(models.Model):
    # Basic info
    street_name = models.CharField(max_length=200)  # common/local name
    scientific_name = models.CharField(max_length=200, blank=True, null=True)
    habitat = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    map_embed = models.TextField(blank=True, null=True)  # For iframe embed code
    video_url = models.URLField(blank=True, null=True)

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

# tree photo model
class TreePhoto(models.Model):
    tree = models.ForeignKey(TreeProfile, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="tree_photos/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.tree.street_name}"

#request model

class TreeRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("answered", "Answered"),
    ]

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tree_requests")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="request_images/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return self.title

    
    
# Answer Model
class TreeAnswer(models.Model):
    tree_request = models.ForeignKey(
        "TreeRequest",
        on_delete=models.CASCADE,
        related_name="answers"
    )
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers_given"
    )
    response_text = models.TextField(default="", blank=False)  # ✅ Default avoids migration issues
    reference_image = models.ImageField(upload_to="answer_images/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    external_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # ✅ Automatically mark request as answered
        if self.tree_request.status != "answered":
            self.tree_request.status = "answered"
            self.tree_request.save()
    def get_embed_url(self):
        if not self.video_url:
            return None
        url = self.video_url.strip()
        if "youtube.com/watch" in url:
            query = parse_qs(urlparse(url).query)
            video_id = query.get("v", [None])[0]
        elif "youtu.be" in url:
            video_id = urlparse(url).path[1:]
        else:
            return None
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None
    def __str__(self):
        return f"Answer to {self.tree_request.title} by {self.answered_by.username}"