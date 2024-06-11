from django.contrib import admin

# Register your models here.
from .models import Wallet,Payment
admin.site.register(Wallet)
admin.site.register(Payment)