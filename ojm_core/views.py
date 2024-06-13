from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from userauth.models import User, ElectricianProfile, CustomerProfile
from userauth.forms import ElectricianSignUpForm,CustomerSignUpForm,UpdatePicture,UpdateBusinessInfo,UpdateLocation,UpdatePrices,UpdateQualification,UserUpdateForm,UpdateCustomerLocation
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import Group

from django.http import JsonResponse
from .models import Request, Notification
from django.core.exceptions import ValidationError
from datetime import datetime
from payment.models import Wallet,Payment,Subscription

from django.conf import settings
from pusher import Pusher

pusher = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)

def index(request):
    unread_count = Notification.objects.filter(user=request.user, read=False).count()
    context={
        'unread_count':unread_count
    }
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
    subscription = Subscription.objects.filter(user=user).first()
    payments = Payment.objects.filter(user=user,verified=True)
    # wallet = get_object_or_404(Wallet, user=user)
    profile_pic_form = UpdatePicture(instance=profile)
    business_form = UpdateBusinessInfo(instance=profile)
    location_form = UpdateLocation(instance=profile)
    prices_form = UpdatePrices(instance=profile)
    qualification_form = UpdateQualification(instance=profile)
    form = UserUpdateForm(instance=user)
    
    
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
        'payments':payments
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
            'start_date': start_date
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
            'start_date': start_date
        }
        Request.objects.create(**request_data)

        messages.success(request, f"Your request has been posted,You will be contacted immediately")
        return redirect('ojm_core:index')

    return render(request, 'flow1.html')

@login_required
def post_job(request):
    return render(request, 'post_job.html')

def all_requests(request):
    requests = Request.objects.all()
    context = {
        'requests':requests
    }
    return render(request, 'request.html', context)


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

