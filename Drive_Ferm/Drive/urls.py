from django.urls import path

from DriveFerm import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('home', views.home, name="mainview"),
    path('visiteVirtuelle/', views.visiteVirtuelle, name="visiteVirtuelle"),
    path('productListing/', views.productListing, name="productListing"),
    path('contactUs/', views.contactUs, name="contactUs"),
    path("signin/", views.logform, name="login"),
    path("signup/", views.register_user, name="signup"),
    path("loout/", views.logoutt, name="logout"),
    path("profile/", views.profile_view, name="profile"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)