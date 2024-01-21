from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    ]

    TRANSACTION_STATUSES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(default=timezone.now)
    service_id = models.IntegerField(null=True, blank=True)  # Опционально
    order_id = models.IntegerField(null=True, blank=True)    # Опционально
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUSES, default='pending')
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.transaction_type} by {self.user.username}"
