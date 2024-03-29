from django.urls import path

from DriveFerm import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('home', views.home, name="mainview"),
    path('visiteVirtuelle/', views.visiteVirtuelle, name="visiteVirtuelle"),
    path('productListing/', views.productListing, name="productListing"),
    path('contactUs/', views.contactUs, name="contactUs"),
    path("signin/", views.customer_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("loout/", views.logoutt, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path('customer/signin/', views.customer_login, name='customer_login'),
    path('business/signin/', views.business_login, name='business_login')
    # path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    # path('business/dashboard/', views.business_dashboard, name='business_dashboard')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)