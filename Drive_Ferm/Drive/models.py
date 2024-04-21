import uuid
from uuid import UUID
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .functions import generate_initial_image
from django.utils import timezone
# Create your models here.

class UserAuth(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.IntegerField(default=0)
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

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)  # Save to get a primary key if creating
        
        if creating:
            content_file, file_name = generate_initial_image(self.username)
            self.profile_image.save(file_name, content_file, save=True)
    class Meta:
        verbose_name_plural = "Customer"
    # No need to redefine uuid or username since they're inherited from UserAuth


class Farm(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    gallery = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    founded_date = models.DateField(verbose_name="Date Founded", null=True, blank=True)
    founders = models.CharField(max_length=255, help_text="Comma-separated list of founders' names")
    location = models.CharField(max_length=255, help_text="Location of the farm")
    number_of_employees = models.IntegerField(verbose_name="Number of Employees", help_text="How many people work at the farm", null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phonen = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Farms"


    

class Business(UserAuth):
    location = models.CharField(max_length=255)
    business_phone_number = models.CharField(max_length=20)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)  # Save to get a primary key if creating
        
        if creating:
            content_file, file_name = generate_initial_image(self.username)
            self.profile_image.save(file_name, content_file, save=True)
    class Meta:
        verbose_name_plural = "Business"


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    quantity_in_stock = models.PositiveIntegerField()
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/',null=True, blank=True)  # Specify a path for image uploads
    url = models.CharField(max_length=255, null=True, blank=True)
    standard_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return self.product_name

class ProductPricing(models.Model):
    product = models.ForeignKey(Product, related_name='pricing', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)  # You can use CharField to specify the quantity like '1kg', '3kg' etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def hard_delete(self, *args, **kwargs):
        super(ProductPricing, self).delete(*args, **kwargs)


class Coupon(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(help_text="Percentage discount")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and (self.valid_from <= now <= self.valid_to)

class Ordering(models.Model):
    # Existing relationships
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_orders',)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_orders')

    # Existing fields
    quantity = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total might be redundant if you calculate it

    # Additional fields related to the payment session
    session_id = models.CharField(max_length=100)  # Stripe session ID
    payment_intent = models.CharField(max_length=100)  # Stripe payment intent ID
    payment_status = models.CharField(max_length=50, default='Pending')  # Payment status from Stripe

    # Additional transaction details
    currency = models.CharField(max_length=10)  # Currency of the transaction

    # Metadata
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.quantity * self.price_at_purchase
        super(Ordering, self).save(*args, **kwargs)

    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    review_text = models.TextField()
    rating = models.PositiveIntegerField(default = 0, 
        validators = [
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
    review_date = models.DateTimeField(auto_now_add=True)

class PageVisit(models.Model):
    path = models.CharField(max_length=200)
    day_offset = models.IntegerField(default=0)
    visit_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('path', 'day_offset')

    def __str__(self):
        return f"{self.path} - Day Offset: {self.day_offset} - {self.visit_count} Visits"
    
class WebContent(models.Model):
    title = models.CharField(max_length=1000)
    html_content = models.TextField("HTML Content")

    def __str__(self):
        return self.title
    
class Event(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=255)
    description = models.TextField()
    activity_icon = models.ForeignKey(WebContent, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Events"


class Gallery(models.Model):
    event = models.ForeignKey(Event, related_name='galleries', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/')



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_cost()
        if self.coupon and self.coupon.is_valid():
            total -= (total * self.coupon.discount / 100)
        return total

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    volume = models.CharField(max_length=255, default=1)

    def get_cost(self):
        # Attempt to find the product pricing that matches this cart item's volume
        try:
            product_pricing = self.product.pricing.get(quantity=self.volume)
            return self.quantity * product_pricing.price
        except ProductPricing.DoesNotExist:
            return 0
    
    def __str__(self):
        return f"Cart of {self.product}"


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"