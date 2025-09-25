from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



class User(AbstractUser):
    USER_TYPES = [
        ('common', 'Common User'),
        ('contributor', 'Contributor'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='common')
    profession = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pics/",
        default="default_profile.png"  )# store this inside /media/profile_pics/ or /static/images/
    profession = models.CharField(max_length=100, blank=True, null=True)
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
