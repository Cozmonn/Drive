from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name="mainview"),
    path('visiteVirtuelle/', views.visiteVirtuelle, name="visiteVirtuelle"),
    path('productListing/', views.productListing, name="productListing"),
    path('contactUs/', views.contactUs, name="contactUs"),
]