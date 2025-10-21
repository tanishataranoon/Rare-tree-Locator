from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from urllib.parse import urlparse, parse_qs
from django.contrib.auth import get_user_model

User = get_user_model()  # <-- safe cross-app reference

# Create your models here.
# Blog Post
class BlogPost(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField( null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    def get_embed_url(self):
        if not self.video_url:
            return None
        url = self.video_url.strip()
        # Standard YouTube URL
        if "youtube.com/watch" in url:
            query = parse_qs(urlparse(url).query)
            video_id = query.get("v", [None])[0]
        # Shortened youtu.be URL
        elif "youtu.be" in url:
            video_id = urlparse(url).path[1:]  # remove leading slash
        else:
            return None  # unsupported URL
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

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
    
# Notification
class Notification(models.Model):
    NOTIF_TYPES = [
        ('comment', 'Comment'),
        ('reply', 'Reply'),
    ]
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES)
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.recipient} ({self.notif_type})"
    

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="bookmarked_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"
