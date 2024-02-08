from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Drive, Product, Order, OrderItem, Payment, Cart, Review

admin.site.register(User)
admin.site.register(Drive)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(Review)