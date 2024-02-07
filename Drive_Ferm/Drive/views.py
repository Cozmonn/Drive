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