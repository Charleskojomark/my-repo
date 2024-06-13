from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from userauth.models import User
from .models import Wallet,Payment,Subscription
from django.conf import settings
from django.contrib import messages
import decimal
import requests,string,random
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from ojm_core.models import Notification
from django.conf import settings
from pusher import Pusher

pusher = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)


def pay(request):
    plan1 = Subscription.objects.filter(name="1 month")
    plan2 = Subscription.objects.filter(name="2 months")
    plan3 = Subscription.objects.filter(name="3 months")
    
    for p in plan1:
        p.calc = p.get_old_price() - p.get_price()  
    for p in plan2:
        p.calc = p.get_old_price() - p.get_price()  
    for p in plan3:
        p.calc = p.get_old_price() - p.get_price()  
    
    context = {
        'plan1': plan1,
        'plan2': plan2,
        'plan3': plan3,
        'initial_amount1': plan1.first().get_price() if plan1.exists() else 0,
        'initial_amount2': plan2.first().get_price() if plan2.exists() else 0,
        'initial_amount3': plan3.first().get_price() if plan3.exists() else 0,
        'initial_price1': plan1.first().get_price() if plan1.exists() else 0,
        'initial_price2': plan2.first().get_price() if plan2.exists() else 0,
        'initial_price3': plan3.first().get_price() if plan3.exists() else 0,
    }
    
    return render(request, 'pay.html', context)


def initiate_payment(request):
    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']
        payment_type = request.POST['payment_type']

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, user=request.user, payment_type=payment_type)
        payment.save()
        
        user = get_object_or_404(User, email=email)
        wallet, created = Wallet.objects.get_or_create(user=user)
        
        context = {
            'wallet': wallet,
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
        }
        return render(request, 'make_payment.html', context)

    return render(request, 'pay.html')

def verify_payment(request, ref):
    payment, created = Payment.objects.get_or_create(ref=ref)
    payment.verified = True
    payment.save()
    messages.success(request, "Successful transaction")
    return redirect('ojm_core:dashboard')



@csrf_exempt
def paystack_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_type = data.get('payment_type')
        amount = data.get('amount')
        user = request.user
        if payment_type == 'payg':
            wallet = get_object_or_404(Wallet, user=user)
            wallet.balance += int(amount)
            wallet.save()
            Notification.objects.create(
                user=user,
                message=f'Wallet balance updated by {amount}',
                notification_type='payment'
            )
            pusher.trigger(f'private-user-{user.id}', 'new-notification', {
                'message': f'Wallet balance updated by {amount}',
                'notification_type': 'payment'
            })
            response_data = {
                'message': 'Wallet balance updated successfully',
                'new_balance': wallet.balance
            }
            
        elif payment_type == 'subscription':
            subscription, created = Subscription.objects.get_or_create(user=user, defaults={'status': 'Inactive'})

            if created or subscription.status != 'Active' or subscription.status == 'Active'  :
                # Activate the subscription based on the price paid
                price_ranges = {
                    1000: "1 month",
                    2000: "2 months",
                    3000: "3 months",
                }
                subscription_name = price_ranges.get(int(amount))

                if subscription_name:
                    subscription.name = subscription_name
                    subscription.status = 'Active'
                    subscription.created_at = timezone.now()
                    subscription.expiry = subscription.calculate_expiry()
                    subscription.save()
                    Notification.objects.create(
                        user=user,
                        message=f'Subscription activated for {subscription_name}',
                        notification_type='account'
                    )
                    pusher.trigger(f'private-user-{user.id}', 'new-notification', {
                        'message': f'Subscription activated for {subscription_name}',
                        'notification_type': 'account'
                    })
                    response_data = {
                        'message': 'Subscription activated successfully',
                        'subscription_status': subscription.status
                    }
                    return JsonResponse(response_data, status=200)
        return JsonResponse(response_data, status=200)


@login_required
def subscription_detail(request):
    user = request.user
    subscription = Subscription.objects.filter(user=user).first()

    context = {'subscription': subscription}
    return render(request, 'subscription_detail.html', context)




def web(request):
    
    user = request.user
    wallet = get_object_or_404(Wallet, user=user)
    context={
        'wallet':wallet
    }
    return render(request, 'profdash.html', context)
