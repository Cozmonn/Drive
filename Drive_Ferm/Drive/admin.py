
from django.contrib.auth.admin import UserAdmin
from .models import PageVisit, UserAuth
# Register your models here.
from django.contrib import admin
from .models import Business, Customer, ProductPricing, UserAuth, Drive, Product, Cart, Review



class ProductPricingAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price')

admin.site.register(UserAuth, UserAdmin)
admin.site.register(Customer)

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('username', 'business_name', 'business_id')
admin.site.register(Business,BusinessAdmin)

admin.site.register(Drive)
admin.site.register(ProductPricing,ProductPricingAdmin)
admin.site.register(Product)
# admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(PageVisit)