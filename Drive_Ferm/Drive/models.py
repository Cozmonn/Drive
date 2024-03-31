import uuid
from uuid import UUID
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .functions import generate_initial_image
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
    founded_date = models.DateField(verbose_name="Date Founded")
    founders = models.CharField(max_length=255, help_text="Comma-separated list of founders' names")
    location = models.CharField(max_length=255, help_text="Location of the farm")
    number_of_employees = models.IntegerField(verbose_name="Number of Employees", help_text="How many people work at the farm")
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

    def __str__(self):
        return self.product_name

class ProductPricing(models.Model):
    product = models.ForeignKey(Product, related_name='pricing', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)  # You can use CharField to specify the quantity like '1kg', '3kg' etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)

# class Order(models.Model):
#     # Specify related names for easier reverse lookups
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
#     business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='orders')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')

#     quantity = models.PositiveIntegerField()
#     price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total price field
#     order_date = models.DateTimeField(auto_now_add=True)
#     order_status = models.CharField(max_length=50, default='Pending')

#     def __str__(self):
#         return f"Order {self.pk} - {self.customer} - {self.product}"


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} ({self.product.business_name})"

    def total_price(self):
        return self.quantity * self.product.pricing.get().price
    
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