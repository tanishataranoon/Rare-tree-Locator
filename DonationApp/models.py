from django.db import models
from django.conf import settings  # <-- important

# Create your models here.
class Donation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # use this instead of auth.User
        on_delete=models.CASCADE
    )
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default='BDT')
    status = models.CharField(max_length=20, default='PENDING')  # PENDING, PAID, FAILED
    val_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.status})"