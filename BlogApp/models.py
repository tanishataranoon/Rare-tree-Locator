from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from MyApp.models import User
# Create your models here.
# Blog Post
class BlogPost(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField( null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

# Comment
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # latest first

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"