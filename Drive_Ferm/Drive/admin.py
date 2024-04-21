
from django.contrib.auth.admin import UserAdmin
from .models import CartItem, ContactMessage, Coupon, Event, Farm, Gallery, Ordering, PageVisit, UserAuth, WebContent
# Register your models here.
from django.contrib import admin
from .models import Business, Customer, ProductPricing, UserAuth, Product, Cart, Review



class ProductPricingAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price')

admin.site.register(UserAuth, UserAdmin)
admin.site.register(Customer)
admin.site.register(Business)
admin.site.register(ProductPricing,ProductPricingAdmin)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'created_at','farm')  # Add 'created_at' here

admin.site.register(Product, ProductAdmin)
admin.site.register(Farm)
admin.site.register(ContactMessage)
admin.site.register(Event)
admin.site.register(Ordering)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Coupon)
admin.site.register(Review)
admin.site.register(PageVisit)
admin.site.register(WebContent)
admin.site.register(Gallery)