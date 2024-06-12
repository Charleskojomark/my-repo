from django.contrib import admin

# Register your models here.
from .models import Wallet,Payment,Subscription
admin.site.register(Wallet)
admin.site.register(Payment)
admin.site.register(Subscription)