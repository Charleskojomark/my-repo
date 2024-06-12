from django.urls import path
from . import views
app_name='payment'

urlpatterns = [
    # path('', views.pay, name='pay'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
    path('initiate-payment/update/', views.paystack_webhook, name='webhook'),
    path('web/', views.web, name='web'),
    path('', views.pay, name='pay'),
    path('subscription/detail/', views.subscription_detail, name='subscription_detail'),
]
