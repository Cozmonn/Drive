from django.urls import path

from DriveFerm import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    
    path('home', views.home, name="home"),
    path('contactUs/', views.contactUs, name="contactUs"),
    path("signin/", views.logform, name="login"),
    path("signup/", views.register, name="signup"),
    path("loout/", views.logoutt, name="logout"),
    path("eventing/", views.eventupload, name="Gallery"),
    path('pay/', views.pay, name="pay"),
    path('chack/', views.dashboard_view, name="chack"),
    path('feedback/', views.feedback, name='feedback'),
    path('ProductbyFarm/', views.products_by_farm, name="PFarm"),
    path('AddProduct/', views.add_product, name="Nproduct"),
    path('UpdateProduct/<int:pk>/', views.edit_product, name="Eproduct"),
    path('product-list/', views.products_view, name='product-list'),
    path('product-detail/<int:pk>/', views.product_detail, name='product-detail'),
    path('cart/', views.add_to_cart, name='cart'),
    path('gallery/', views.gallery, name='gallery'),
    path('shopping-cart/', views.cart_items_view, name='shopping-cart'),
    path('apply-coupon/', views.apply_coupon, name="apply-coupon"),
    path('create_coupon/', views.create_coupon, name="create_coupon"),
    path('coupon-update/<int:pk>/', views.coupon_update, name='coupon_update'),
    path('coupon-delete/<int:pk>/', views.coupon_delete, name='coupon_delete'),
    path('coupon-list/', views.coupons_by_farm, name='coupon-list'),
    path('Update/', views.update_user_information, name="UpdateProfile"),
    path('BUpdate/', views.update_business, name="Update_Business"),
    path('profile/', views.show_events, name='profile'),
    path('feedback-list/', views.display_feedback, name='feedback-list'),
    path('delete/<int:pk>/', views.delete_event, name='delete_event'),
    path('change/<int:pk>/', views.update_event, name='change'),
    path('change-farn/', views.update_farm, name='change-farn'),
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('createcheckoutsession/', views.createcheckoutsession, name='createcheckoutsession'),
    path('shopping-cart/bulk-update-cart-items/', views.bulk_update_cart_items, name='bulk-update-cart-items'),
    # path('cancel/', views.cancel, name='cancel'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)