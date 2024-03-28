from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User, auth

# Create your views here.

def home(request):
    return render(request, "index.html")

def visiteVirtuelle(request):
    return render(request, "visite_virtuelle.html")

def productListing(request):
    return render(request, "products.html")

def contactUs(request):
    return render(request, "contactuS.html")




# Create your views here.
from distutils.log import error
import email

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse, reverse_lazy
from .form import SignInForm, EditProfileForm


# Create your views here.


#login_view


#sign_up_view


def logoutt(request):
    logout(request)
    messages.success(request, ("Logging Out Successfully"))
    return redirect('login')



from django.shortcuts import render
from .models import Business, Customer, UserAuth

def profile_view(request):
    print(request.user)
    profile = UserAuth.objects.get(username=request.user)
    print(profile.profile_image.url)
    context = {'profile': profile}
    return render(request, 'client-view.html', context)

def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and isinstance(user, Customer):
            login(request, user)
            return redirect('customer_dashboard')  # Redirect to customer dashboard
        else:
            # Handle invalid login for customers
            pass
    return render(request, 'login.html')


def business_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and isinstance(user, Business):
            login(request, user)
            return redirect('business_dashboard')  # Redirect to business dashboard
        else:
            # Handle invalid login for businesses
            pass
    return render(request, 'business_login.html')
# views.py

from django.shortcuts import render, redirect
from django.urls import reverse
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if user_type == 'customer':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            shipping_address = request.POST.get('shipping_address')

            # Create a new Customer object
            new_customer = Customer.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                shipping_address=shipping_address
            )
            new_customer.save()
            
        elif user_type == 'business_owner':
            business_name = request.POST.get('business_name')
            phone_number = request.POST.get('phone_number')
            location = request.POST.get('location')

            # Create a new Business object
            new_business = Business.objects.create_user(
                email=email,
                password=password,
                business_name=business_name,
                phone_number=phone_number,
                location=location
            )
            new_business.save()

        return redirect(reverse('login'))  # Redirect to login page after successful signup

    return render(request, 'signup.html')  # Render the signup page template for GET requests