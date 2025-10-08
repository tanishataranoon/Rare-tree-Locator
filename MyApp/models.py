from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


#user model
class User(AbstractUser):
    USER_TYPES = [
        ('common', 'Common User'),
        ('contributor', 'Contributor'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='common')
    profession = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

# profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
    upload_to="profile_pics/",
    default="profile_pics/default_profile.png"
)

    profession = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    personal_website = models.URLField(blank=True, null=True)
    joined_date = models.DateTimeField(default=timezone.now)  # no auto_now_add for now

    def __str__(self):
        return self.user.username


# --- SIGNALS: auto-create Profile when a User is created ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, profession=instance.profession)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
