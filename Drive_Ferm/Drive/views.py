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

def logform(request):
    if request.method=='POST':
        username = request.POST['username']
        print(request.POST['username'])
        password = request.POST['password']
        print(request.POST['password'])
        user = authenticate(request, username=username, password=password)
        print('logged in')
        login(request, user)
        print('logged in')
        return redirect('profile')
    else:
        return render(request, 'login.html')

#sign_up_view
def register_user(request):
    if request.method=='POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.warning(request,("Please complete ur signing up"))
            return redirect('profile')
        else:
            messages.warning(request,("There was an error Logging In, Please try again!"))
    else:
        form=SignInForm()
    return render(request, 'signup.html', {
            'form':form,
    })


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

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if user_type == 'customer':
            # Create a new Customer object
            customer = Customer.objects.create_user(
                username=email,  # You can use email as the username
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            # Add any additional fields specific to the Customer model
            customer.shipping_address = request.POST.get('shipping_address')
            customer.save()
            # Redirect to the appropriate page after successful registration
            return redirect('customer_dashboard')
        elif user_type == 'business_owner':
            # Create a new Business object
            business = Business.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            # Add any additional fields specific to the Business model
            business.business_name = request.POST.get('business_name')
            business.business_id = request.POST.get('business_id')
            business.location = request.POST.get('location')
            business.business_phone_number = request.POST.get('business_phone_number')
            business.save()
            # Redirect to the appropriate page after successful registration
            return redirect('business_dashboard')

    return render(request, 'signup.html')
