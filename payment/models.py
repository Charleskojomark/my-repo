from django.db import models
from userauth.models import User
import secrets
from .paystack  import  Paystack
from django.utils import timezone
from datetime import timedelta

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user.username}\'s Wallet'

class Payment(models.Model):
    PAYMENT_TYPES = [
        ('subscription', 'Subscription'),
        ('payg', 'Pay-as-you-go'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return int(self.amount) * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False    
    
class Subscription(models.Model):
    STATUS_CHOICES = [
        ('Inactive', 'Inactive'),
        ('Active', 'Active'),
        ('Expired', 'Expired'),
    ]
    
    DURATION_CHOICES = [
        ("1 month", "1 month"),
        ("3 months", "3 months"),
        ("6 months", "6 months"),
    ]

    name = models.CharField(max_length=20, choices=DURATION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    expiry = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    remaining_quotes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only update expiry if it's a new subscription
            self.expiry = self.calculate_expiry()
            self.status = 'Inactive'  # Set status to active when creating a new subscription
        super().save(*args, **kwargs)

    def calculate_expiry(self):
        # logic to calculate expiry based on the subscription name
        if self.name == "1 month":
            return self.created_at + timedelta(days=30)
        elif self.name == "3 months":
            return self.created_at + timedelta(days=90)
        elif self.name == "6 months":
            return self.created_at + timedelta(days=180)
        return self.created_at
    
    def check_and_update_expiry(self):
        if timezone.now() > self.expiry:
            self.status = 'expired'
            self.save()
            return True
        return False

    def get_discount_percentage(self):
        old_price = self.get_old_price()
        if old_price > 0:
            return ((old_price - self.get_price()) / old_price) * 100
        return 0

    def get_price(self):
        price_mapping = {
            "1 month": 10500.00,
            "3 months": 29500.00,
            "6 months": 59500.00,
        }
        return price_mapping.get(self.name, 0)

    def get_old_price(self):
        old_price_mapping = {
            "1 month": 15000.00,
            "3 months": 45000.00,
            "6 months": 80000.00,
        }
        return old_price_mapping.get(self.name, 0)

    def __str__(self):
        return f"{self.name} Subscription for {self.user}"