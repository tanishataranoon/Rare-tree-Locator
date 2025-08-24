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
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('contributor', 'Contributor'),
        ('admin', 'Admin'),
    ]
    #By default, AbstractUser already includes name, email, password fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    @property
    def name(self):
        #Combine first_name and last_name 
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.username} ({self.role})"
# Tree Photo
class TreePhoto(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='photos')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_photos')
    photo = models.ImageField(upload_to='tree_photos/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.tree} by {self.uploaded_by}"
# Blog Post
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Comment
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"


