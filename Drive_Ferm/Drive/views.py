from django.shortcuts import render

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
from django.contrib import messages, auth
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
from .models import UserAuth

def profile_view(request):
    print(request.user)
    profile = UserAuth.objects.get(username=request.user)
    print(profile.profile_image.url)
    context = {'profile': profile}
    return render(request, 'client-view.html', context)