from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from userauth.models import User, ElectricianProfile, CustomerProfile,Identity
from userauth.forms import ElectricianSignUpForm,CustomerSignUpForm,UpdatePicture,UpdateBusinessInfo,UpdateLocation,UpdatePrices,UpdateQualification,UserUpdateForm,UpdateCustomerLocation,IdentityForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from .models import Request, Notification, Quote
from django.core.exceptions import ValidationError
from datetime import datetime
from payment.models import Wallet,Payment,Subscription
import json
from django.utils import timezone
import logging
from chatapp.models import Conversation, Message

from django.conf import settings
from pusher import Pusher

pusher = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)

SUBSCRIPTION_TOTAL_QUOTES = {
    "1 month": 100,
    "3 months": 350,
    "6 months": 1000,
}

def index(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        unread_count = notifications.filter(read=False).count()
        read_count = notifications.filter(read=True).count()

        context = {
            'notifications': notifications,
            'unread_count': unread_count,
            'read_count': read_count
        }
    else:
        context = {}
    
    return render(request, 'index.html', context)

def dashboard(request):
    if request.user.groups.filter(name='customers').exists():
        return redirect('ojm_core:user_dashboard')
    elif request.user.groups.filter(name='electricians').exists():
        return redirect('ojm_core:prof_dashboard')
    

@login_required
def user_dashboard(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    user = request.user
    form = UserUpdateForm(instance=user)
    location_form = UpdateCustomerLocation(instance=profile)
    
    
    context = {
        'profile': profile,
        'location_form':location_form,
        'form':form,
    }
    return render(request, 'userdash.html',context)



@login_required
def prof_dashboard(request):
    profile = get_object_or_404(ElectricianProfile, user=request.user)
    user = request.user
    wallet, created = Wallet.objects.get_or_create(user=user)
    # subscription = Subscription.objects.filter(user=user).first()
    payments = Payment.objects.filter(user=user,verified=True)
    # wallet = get_object_or_404(Wallet, user=user)
    profile_pic_form = UpdatePicture(instance=profile)
    business_form = UpdateBusinessInfo(instance=profile)
    location_form = UpdateLocation(instance=profile)
    prices_form = UpdatePrices(instance=profile)
    qualification_form = UpdateQualification(instance=profile)
    form = UserUpdateForm(instance=user)
    notifications = Notification.objects.filter(user=user)
    electrician = ElectricianProfile.objects.filter(user=user)
    user_profile = ElectricianProfile.objects.get(user=request.user)
    id_form = IdentityForm(instance=user)
    subscription, created = Subscription.objects.get_or_create(user=user)
    # subscription = get_object_or_404(Subscription, user=request.user)
    if subscription.name:
        total_quotes = SUBSCRIPTION_TOTAL_QUOTES.get(subscription.name, 0)
        remaining_quotes = subscription.remaining_quotes
        used_quotes = total_quotes - remaining_quotes
        subscribed = subscription.status == "Active"
        context = {
        'profile': profile,
        'profile_pic_form':profile_pic_form,
        'business_form':business_form,
        'location_form':location_form,
        'prices_form':prices_form,
        'qualification_form':qualification_form,
        'form':form,
        'wallet':wallet,
        'subscription':subscription,
        'payments':payments,
        'notifications': notifications,
        'electrician':electrician,
        'user_profile': user_profile,
        'id_form':id_form,
        'total_quotes': total_quotes,
        'remaining_quotes': remaining_quotes,
        'used_quotes': used_quotes,
        'subscribed':subscribed
        }
        return render(request, 'profdash.html',context)
        
    context = {
        'profile': profile,
        'profile_pic_form':profile_pic_form,
        'business_form':business_form,
        'location_form':location_form,
        'prices_form':prices_form,
        'qualification_form':qualification_form,
        'form':form,
        'wallet':wallet,
        'subscription':subscription,
        'payments':payments,
        'notifications': notifications,
        'electrician':electrician,
        'user_profile': user_profile,
        'id_form':id_form,
        
    }
    return render(request, 'profdash.html',context)

def all_users(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render(request,'users.html',context)

def single_user(request, pk):
    user = get_object_or_404(User,pk=pk)
    context = {
        'user':user
    }
    return render(request,'user.html',context)



def search_view(request):
    query = request.GET.get('query', '')
    context = {
        'query': query,
    }
    if query:
        if request.user.is_authenticated:
            return render(request, 'flow1.html', context)
        else:
            return render(request, 'flow.html', context)
    else:
        return render(request, 'index.html')
    
def categories(request):
    return render(request,'services.html')

def services(request):
    return render(request,'service.html')
def service_detail(request):
    return render(request,'single.html')



def post_request(request):
    if request.method == "POST":
        query = request.POST.get('query', '')
        country = request.POST.get('country', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')
        address = request.POST.get('address', '')
        service_description = request.POST.get('serviceDescription', '')
        additional_files = request.FILES.get('additionalFiles', None)
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('confirmPassword', '')
        terms = request.POST.get('terms', False) == 'on'
        job_start = request.POST.get('jobStart', '')
        start_date_str = request.POST.get('startDate', None)
        readiness = request.POST.get('readiness', None)
        
        start_date = None
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Invalid date format. Please use YYYY-MM-DD.")
        
        
        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1, phone_number=phone)
        user.is_active = False  # Deactivate account until it is confirmed
        user.save()

        # Create customer profile
        customer_profile = CustomerProfile.objects.create(
            user=user,
            country=country,
            state=state,
            city =city,
            address =address,
            terms=terms
        )

        # Save customer profile
        customer_profile.save()

        # Add user to 'customers' group
        customers, created = Group.objects.get_or_create(name='customers')
        user.groups.add(customers)

        # Send email confirmation
        current_site = get_current_site(request)
        mail_subject = 'Activate your OJM account.'
        message = render_to_string('verify_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        send_mail(mail_subject, message, 'Ojm Electrical', [to_email])

        # Create request
        request_data = {
            'user': user,
            'query': query,
            'service_description': service_description,
            'additional_files': additional_files,
            'job_start': job_start,
            'start_date': start_date,
            'readiness':readiness
        }
        Request.objects.create(**request_data)

        # Display success message
        messages.success(request, f"Welcome {username}, Your request was posted, Check your mail to activate your account")
        return redirect('ojm_core:index')

    return render(request, 'flow.html')



def user_post(request):
    user = request.user
    if request.method == "POST":
        query = request.POST['query']
        service_description = request.POST['serviceDescription']
        additional_files = request.FILES.get('additionalFiles', None)
        job_start = request.POST.get('jobStart', None)
        start_date_str = request.POST.get('startDate', None)
        readiness = request.POST.get('readiness', None)
        
        start_date = None
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Invalid date format. Please use YYYY-MM-DD.")

        # Create request
        request_data = {
            'user': user,
            'query': query,
            'service_description': service_description,
            'additional_files': additional_files,
            'job_start': job_start,
            'start_date': start_date,
            'readiness':readiness
        }
        Request.objects.create(**request_data)

        messages.success(request, f"Your request has been posted,You will be contacted immediately")
        return redirect('ojm_core:index')

    return render(request, 'flow1.html')

@login_required
def post_job(request):
    return render(request, 'post_job.html')


def all_requests(request):
    customers_group = Group.objects.get(name="customers")
    # requests = Request.objects.filter(user__groups=customers_group)
    requests = Request.objects.all()
    context = {
        'requests':requests,
    }
    return render(request, 'requests.html', context)


@login_required
def request_detail(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    
    # Get the appropriate profile
    user_profile = None
    if hasattr(req.user, 'customerprofile'):
        user_profile = req.user.customerprofile
    elif hasattr(req.user, 'electricianprofile'):
        user_profile = req.user.electricianprofile

    # Get the subscription details
    subscription = get_object_or_404(Subscription, user=request.user)
    total_quotes = SUBSCRIPTION_TOTAL_QUOTES.get(subscription.name, 0)
    remaining_quotes = subscription.remaining_quotes
    used_quotes = total_quotes - remaining_quotes
    subscribed = subscription.status == "Active"
    context = {
        'req': req,
        'user_profile': user_profile,
        'total_quotes': total_quotes,
        'used_quotes': used_quotes,
        'remaining_quotes': remaining_quotes,
        'subscribed':subscribed
    }

    return render(request, 'request_detail.html', context)


@login_required
def customer_info(request,request_id):
    req = get_object_or_404(Request, id=request_id)
    
    user_profile = None
    if hasattr(req.user, 'customerprofile'):
        user_profile = req.user.customerprofile
    elif hasattr(req.user, 'electricianprofile'):
        user_profile = req.user.electricianprofile
    context = {
        'req': req,
        'user_profile': user_profile,
    }

    return render(request, 'customer_info.html', context)



@login_required
@csrf_exempt
def send_quote(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    electrician_profile = get_object_or_404(ElectricianProfile, user=request.user)

    if not electrician_profile.id_verified:
        messages.error(request, "You cannot send a quote without verifying your ID. Visit settings to verify your ID.")
        return JsonResponse({'status': 'error', 'message': 'ID not verified', 'redirect_url': reverse('ojm_core:settings')})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            price = data.get('price')
            price_type = data.get('price_type')
            price_details = data.get('price_details')

            user = request.user

            # Check subscription or wallet balance
            subscription = Subscription.objects.filter(user=user, status='Active', expiry__gt=timezone.now()).first()
            wallet = Wallet.objects.filter(user=user).first()

            if subscription and subscription.remaining_quotes > 0:
                # Deduct from subscription
                subscription.remaining_quotes -= 1
                subscription.save()
            elif wallet and wallet.balance >= int(500):
                # Deduct from wallet
                wallet.balance -= int(500)
                wallet.save()
            else:
                messages.error(request, "Insufficient funds or no active subscription")
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds or no active subscription', 'redirect_url': reverse('ojm_core:dashboard')})

            # Create the quote
            quote = Quote.objects.create(
                request=request_obj,
                electrician=user,
                price=price,
                price_type=price_type,
                price_details=price_details,
                created_at=timezone.now()
            )

            # Prepare the message content
            message_content = (
                f"New Quote from {quote.electrician.username}:\n"
                f"Price: ₦{quote.price}\n"
                f"Price Type: {quote.get_price_type_display()}\n"
                f"Details: {quote.price_details}"
            )

            # Send notification and message to the request owner
            recipient_user = request_obj.user
            Notification.objects.create(
                user=recipient_user,
                message=f"New quote from {user.username}",
                notification_type='quote'
            )

            # Find or create a conversation between the users
            conversation = Conversation.objects.filter(participants=user).filter(participants=recipient_user).first()
            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.set([user, recipient_user])

            # Create a new message in the conversation
            Message.objects.create(
                sender=user,
                content=message_content,
                conversation=conversation
            )

            # Trigger pusher event
            pusher.trigger(f'private-user-{recipient_user.id}', 'new-notification', {
                'message': f"New quote from {user.username}",
                'notification_type': 'quote'
            })

            messages.success(request, "Your quote was successfully sent. Check your messages to follow up with the customer.")
            return JsonResponse({'status': 'success', 'message': 'Quote sent', 'redirect_url': reverse('ojm_core:customer_info',kwargs={'request_id': request_obj.id})})

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e), 'redirect_url': reverse('ojm_core:dashboard')})

    messages.error(request, "Invalid request method.")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method', 'redirect_url': reverse('ojm_core:dashboard')})



@login_required
def get_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user)
    count = Notification.objects.filter(user=user).count()

    # Update notifications to read=True
    notifications.update(read=True)

    context = {
        'notifications': notifications,
        'count':count
    }
    return render(request, 'notifications.html', context)

