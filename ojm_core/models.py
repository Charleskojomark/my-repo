from django.db import models
from userauth.models import User
# Create your models here.
class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    service_description = models.TextField()
    additional_files = models.FileField(upload_to='additional_files/', blank=True, null=True)
    job_start = models.CharField(max_length=20, blank=True, null=True)
    readiness = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created_at',)
    def __str__(self):
        return self.query
    
class Quote(models.Model):
    PRICE_TYPE_CHOICES = [
        ('Negotiable', 'Negotiable'),
        ('Fixed Price', 'Fixed Price'),
        ('Starting Fee', 'Starting Fee'),
        ('Per hour', 'Per hour'),
    ]
    
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    electrician = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(max_length=50, choices=PRICE_TYPE_CHOICES)
    price_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quote by {self.electrician.username} for {self.request.query}"

    
class Notification(models.Model):
    TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('account', 'Account'),
        ('chat', 'Chat'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    class Meta:
        ordering = ('-created_at',)
    def __str__(self):
        return f"{self.get_notification_type_display()} Notification for {self.user}"