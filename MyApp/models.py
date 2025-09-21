from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Tree Model
class Tree(models.Model):
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('endangered', 'Endangered'),
    ]
    scientific_name = models.CharField(max_length=255)
    common_names = models.CharField(max_length=255, blank=True, null=True)
    rarity_status = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common')
    description = models.TextField(blank=True, null=True)
    #location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='trees')

    def __str__(self):
        return f"{self.common_names or self.scientific_name}"
    
# Custom User model
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
# Tree Photo
class TreePhoto(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='photos')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_photos')
    photo = models.ImageField(upload_to='tree_photos/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.tree} by {self.uploaded_by}"


