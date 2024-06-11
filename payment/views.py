from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from userauth.models import User
from .models import Wallet,Payment
from django.conf import settings
from django.contrib import messages
import decimal
import requests,string,random
# Create your views here.


def pay(request):
    return render(request, 'pay.html')



def initiate_payment(request):
    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, user=request.user)
        payment.save()
        user = get_object_or_404(User, email=email) 
        wallet = get_object_or_404(Wallet, user=user)
        context = {
            'wallet':wallet,
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
        }
        return render(request, 'make_payment.html', context)

    return render(request, 'pay.html')


def verify_payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        user_wallet = Wallet.objects.get(user=request.user)
        user_wallet.balance += payment.amount
        user_wallet.save()
        messages(request, " funded wallet successfully")
        return render(request, "index.html")
    return render(request, "index.html")





@csrf_exempt
def paystack_webhook(request):
    
    user = request.user
    wallet = get_object_or_404(Wallet, user=user)
    context={
        'wallet':wallet
    }
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')
        wallet.balance += int(amount)
        wallet.save()
        
        response_data = {
            'message': 'Wallet balance updated successfully',
            'new_balance': wallet.balance  # Include the updated balance in the response
        }
        return JsonResponse(response_data, status=200)


def web(request):
    
    user = request.user
    wallet = get_object_or_404(Wallet, user=user)
    context={
        'wallet':wallet
    }
    return render(request, 'profdash.html', context)
