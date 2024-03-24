from uuid import UUID
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserAuth(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # Uncomment and use the below line if you decide to use profile images
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
        # Overriding the groups and user_permissions fields to set a new related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="userauth_groups",  # Unique related name
        related_query_name="userauth",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="userauth_user_permissions",  # Unique related name
        related_query_name="userauth",
    )
    class Meta:
        verbose_name_plural = "UserAuths"

class Customer(UserAuth):
    shipping_address = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)
    last_login_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Customer"
    # No need to redefine uuid or username since they're inherited from UserAuth

class Business(UserAuth):
    business_name = models.CharField(max_length=255)
    business_id = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    # Consider not duplicating the email field; use the one from UserAuth
    # business_email = models.EmailField(unique=True)
    business_phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Business"
    
    def __str__(self):
        return self.business_name



class Drive(models.Model):
    Drive_name = models.CharField(max_length=100)


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    quantity_in_stock = models.PositiveIntegerField()
    business_name = models.ForeignKey(Business, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')  # Specify a path for image uploads

    def __str__(self):
        return self.product_name

class ProductPricing(models.Model):
    product = models.ForeignKey(Product, related_name='pricing', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)  # You can use CharField to specify the quantity like '1kg', '3kg' etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} - {self.price} Euros"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_method = models.CharField(max_length=100)
    order_status = models.CharField(max_length=50)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    review_date = models.DateTimeField(auto_now_add=True)

