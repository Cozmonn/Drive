# views.py

import json
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, render, redirect
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal

from .functions import generate_unique_username



#stripe_keys
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

def home(request):
    return render(request, "index.html")

def visiteVirtuelle(request):
    return render(request, "visite_virtuelle.html")

def contactUs(request):
    return render(request, "contactuS.html")

def show_events(request):
    # Fetch all events or use filters as needed
    profile = get_object_or_404(Business, username=request.user.username)
    profile_picture_url = request.build_absolute_uri(profile.profile_image.url) if profile.profile_image else None
    farm = profile.farm
    farm_picture_url = request.build_absolute_uri(farm.gallery.url) if farm.gallery else None
    events = Event.objects.filter(farm=farm).order_by('-created_at')
    return render(request, 'profile.html', {'events': events, 'farm': farm, 'profile':profile, 'profile_picture_url': profile_picture_url, 'farm_picture_url':farm_picture_url})

def delete_event(request, pk):
    if request.method == 'POST':  # Ensures this view can only be accessed via POST request
        print('hihihihii')
        event = Event.objects.get(id=pk)
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('events_list')  # Redirect to the view that shows the list of events
    else:
        messages.error(request, 'Invalid request.')
        return redirect('profile')
    
# Create your views here.
from distutils.log import error
import email

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse, reverse_lazy
from .form import SignInForm, EditProfileForm


# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from .models import Cart, CartItem, Coupon, Event, Gallery
from django.contrib import messages

@csrf_exempt
def update_event(request: HttpRequest, pk: int):
    event = get_object_or_404(Event, id=pk)
    
    if request.method == 'POST':
        name = request.POST.get('title')
        description = request.POST.get('description')
        
        # Update event details
        event.name = name
        event.description = description
        event.save()

        # Handle photo uploads
        images = request.FILES.getlist('files')  # Assuming the input field name is 'images'

        if images:
            # If new images are uploaded, delete old images
            event.galleries.all().delete()

            # Save new images
            for image in images:
                Gallery.objects.create(event=event, image=image)

            messages.success(request, 'Event and photos updated successfully!')
        else:
            messages.success(request, 'Event updated successfully!')
        
        return redirect('profile')
    
    # Render the event update form
    icons = Event.objects.all().distinct()
    return render(request, 'update-event.html', {'event': event, 'icons':icons})

#login_view

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def logform(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('UpdateProfile')  # Redirect to a home or another target page
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')  # Path to your login template


from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('First_name')
        last_name = request.POST.get('Last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        # Generate a unique username
        username = generate_unique_username(first_name, last_name)
        
        User = get_user_model()
        user = None
        
        # Create user instance based on user_type
        if user_type in ['Client', 'Business']:
            if user_type == 'Client':
                # Assuming Customer and Business models inherit from User model
                # and have a create_user method.
                user = Customer.objects.create_user(
                    username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name)
            elif user_type == 'Business':
                user = Business.objects.create_user(
                    username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name)
            
            # Common success message
            messages.success(request, f"{user_type} account created successfully!")
        else:
            messages.error(request, "Invalid user type selected.")
            return render(request, 'signup.html')
        
        # Send email confirmation if a user was created
        if user:
            send_mail(
                subject='Welcome to Our Site!',
                message=f'Hi {first_name}, your account has been successfully created. Your username is {username}.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
        
        return redirect('login')  # Redirect after successful account creation
    
    return render(request, 'signup.html')


def logoutt(request):
    logout(request)
    messages.success(request, ("Logging Out Successfully"))
    return redirect('login')

# def create_checkout_session(request):
#     # Récupérer les produits du panier de l'utilisateur
#     cart_items = Cart.objects.all()  # Adapt this according to your actual cart implementation
    
#     # Préparer les données pour la session de paiement
#     line_items = []
#     for cart_item in cart_items:
#         product = cart_item.product
#         line_items.append({
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': product.name,
#                     # Ajouter d'autres informations du produit si nécessaire
#                 },
#                 'unit_amount': int(product.price * 100),  # Le prix est en cents
#             },
#             'quantity': cart_item.quantity,
#         })

#     # Créer la session de paiement avec Stripe
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=line_items,
#         mode='payment',
#         success_url='/success/',
#         cancel_url='/cancel/',
#     )
    
#     return HttpResponseRedirect(session.url)



def create_checkout_session(request):
    if request.method == 'POST':
        pricing_id = request.POST.get('pricingQuantity')
        quantity = int(request.POST.get('directQuantity', 1))
        pricing = get_object_or_404(ProductPricing, id=pricing_id)
        product = pricing.product
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f'{product.product_name}, {product.farm}',
                                'images': [product.url],
                                'description': product.description,
                                'metadata': {'volume': str(pricing.quantity)},  # Convert to string if needed
                            },
                            'unit_amount': int(pricing.price * 100),  # Convert to cents
                        },
                        'quantity': quantity,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
                metadata={'volume': quantity, 'product_id': str(product.id)},
            )
            return redirect(checkout_session.url)
        except Exception as e:
            # Handle exceptions or errors
            return redirect('/error/')  # Redirect to an error handling page or similar








@csrf_exempt
def pay(request):
    return render(request, 'paiement.html')

# @csrf_exempt
# def create_checkout_session(request):

#     # Make sure the user has a cart with items in it
#     try:
#         cart = Cart.objects.get(user=request.user)
#         if not cart.items.exists():
#             return JsonResponse({'error': 'Your cart is empty.'}, status=400)
#     except Cart.DoesNotExist:
#         return JsonResponse({'error': 'No active cart found.'}, status=404)

    
#     roduct = get_object_or_404(Product, product=cart.product)
#     # Calculate the total price in the backend
#     total = cart.get_total_price()
    
#     # Prepare line items for the payment session
#     line_items = []
#     for item in cart.items.all():
#         line_items.append({
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'images': [item["image_url"]],
#                     'name': item["product_name"],
#                     'description': item["description"],
#                 },
#                 'unit_amount': int(item["price"] * 100),  # Price in cents
#             },
#             'quantity': item["quantity"],
#         })

#     # Create a payment session with Stripe
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=line_items,
#         mode='payment',
#         success_url='https://example.com/success',
#         cancel_url='https://example.com/cancel',
#     )

#     return HttpResponseRedirect(session.url)

# @csrf_exempt
# def Webhooking(request):
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse('Invalid payload', status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse('Invalid signature', status=400)

#     # Default response for unspecified events
#     response = HttpResponse('Unhandled event type', status=200)

#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = stripe.checkout.Session.retrieve(
#         event['data']['object']['id'],
#         expand=['line_items'],
#         )
#         if session.payment_status  == "paid":
#             # Assuming `session['metadata']['user_id']` correctly refers to a Client username.
#             # Adjust this to match your actual data structure and model field names.
#             pass
#         else:
#             # Handle payment failure or other cases here if needed
#             response = HttpResponse('Payment not successful', status=200)

#     return response


# def create_order(session):
#     order = Order.objects.create(
#         session_id = session['id'],
#         client = session['metadata']['user_id'],
#         customer_id=session['customer'],
#         payment_intent=session['payment_intent'],
#         payment_status=session['payment_status'],
#         total_amount=session['amount_total'] / 100,  # Stripe amounts are in cents
#         currency=session['currency'],
#         email=session['customer_details']['email'],  # Adjust according to actual session structure
#         fullname=session['customer_details']['name'],  # Adjust according to actual session structure
#         phone=session['customer_details']['phone'],  # Adjust according to actual session structure
#         tax_exempt=session['customer_details']['tax_exempt'],  # Adjust according to actual session structure
#     )
#     order.save()





################# -------UPDATE & DELETE IMAGE ------- #################
@csrf_exempt
def update_user_information(request):
    profile = Customer.objects.get(username=request.user.username)
    profile_picture_url = request.build_absolute_uri(profile.profile_image.url) if profile.profile_image else None  # Construct absolute URL

    if request.method == 'POST':
        first_name = request.POST.get('First_Name')
        last_name = request.POST.get('Last_Name')
        username = request.POST.get('Username')
        email = request.POST.get('email')
        shipping_address = request.POST.get('Shipping_adress')
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
       # Handle profile picture upload
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            print(photo)
            # Delete old image if it exists
            if profile.profile_image:
                profile.profile_image.delete(save=False)  # Deletes the file and not the model instance
                print('deletion complete')
            
            # Save new image
            profile.profile_image.save(photo.name, photo, save=False)
            print('done')

        # Update user information
        profile.first_name = first_name
        profile.last_name = last_name
        profile.username = username
        profile.email = email
        profile.shipping_address = shipping_address
        

        # Check if old password matches
        if old_password and not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('UpdateProfile')

        # Check if new passwords match
        if new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
            return redirect('UpdateProfile')

        # Change password if new password is provided
        if new_password1:
            profile.set_password(new_password1)
            update_session_auth_hash(request, profile)  # Update session to prevent logout

        profile.save()
        # user.save()
        messages.success(request, "Your information has been updated successfully.")
        return redirect('UpdateProfile')  # Redirect to user profile page or any other page

    return render(request, 'Cupdate.html', {'profile': profile, 'profile_picture_url': profile_picture_url})


def update_business(request):
    profile = Business.objects.get(username=request.user.username)
    profile_picture_url = request.build_absolute_uri(profile.profile_image.url) if profile.profile_image else None  # Construct absolute URL
    if request.method == 'POST':
        # Extract form data
        business_name = request.POST.get('Business_name')
        location = request.POST.get('Location')
        email = request.POST.get('email')
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Retrieve the current business profile
        business = Business.objects.get(user=request.user)

               # Handle profile picture upload
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            print(photo)
            # Delete old image if it exists
            if business.profile_image:
                business.profile_image.delete(save=False)  # Deletes the file and not the model instance
                print('deletion complete')
            
            # Save new image
            business.profile_image.save(photo.name, photo, save=False)
            print('done')

        # Update business information
        business.business_name = business_name
        business.location = location
        business.email = email

        # Check if passwords are provided and match
        if old_password and new_password1:
            if request.user.check_password(old_password):
                if new_password1 == new_password2:
                    request.user.set_password(new_password1)
                else:
                    messages.error(request, "New passwords do not match.")
                    return redirect('update_business')
            else:
                messages.error(request, "Old password is incorrect.")
                return redirect('update_business')

        # Save changes
        business.save()

        messages.success(request, "Business information updated successfully.")
        return redirect('profile')  # Redirect to profile or any other relevant page

    return render(request, 'settings.html', {'profile': profile, 'profile_picture_url': profile_picture_url})  # Replace 'update_business.html' with your template path

@csrf_exempt
def update_farm(request):

    profile = get_object_or_404(Business, username=request.user.username)
    farm = profile.farm
    profile_picture_url = request.build_absolute_uri(farm.gallery.url) if farm.gallery else None

    if request.method == 'POST':
        farm.name = request.POST.get('name')
        farm.description = request.POST.get('description')
        farm.founded_date = request.POST.get('founded_date')
        farm.founders = request.POST.get('founders')
        farm.location = request.POST.get('location')
        farm.number_of_employees = int(request.POST.get('number_of_employees'))
        farm.email = request.POST.get('email')
        farm.phonen = request.POST.get('phonen')

               # Handle profile picture upload
        if 'gallery' in request.FILES:
            photo = request.FILES['gallery']
            # Delete old image if it exists
            if farm.gallery:
                farm.gallery.delete(save=False)  # Deletes the file and not the model instance
            
            # Save new image
            farm.gallery.save(photo.name, photo, save=False)

        farm.save()
        messages.success(request, 'Farm updated successfully!')
        return redirect('profile')  # Redirect to a farm detail view or similar

    # Render the farm update form with farm instance
    return render(request, 'farm-update.html', {'farm': farm, 'profile_picture_url': profile_picture_url})











def delete_profile_picture(request):
    profile = Customer.objects.get(username=request.user.username)
    if request.method == 'POST':
        profile.profile_image.delete()  # Supprime l'image
        profile.profile_image = None
        profile.save()  # Sauvegarde le modèle sans l'image
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    





def products_by_farm(request):
    profile = get_object_or_404(Business, username=request.user.username)
    farm = profile.farm

    search_query = request.GET.get('search', '')
    products = Product.objects.filter(farm=farm)
    if search_query:
        products = products.filter(product_name__icontains=search_query)

    entries_per_page = request.GET.get('entries', 5)
    try:
        entries_per_page = int(entries_per_page)
    except ValueError:
        entries_per_page = 5

    paginator = Paginator(products, entries_per_page)
    page = request.GET.get('page')

    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    product_list = []
    for product in products_page:
        # Directly fetch pricing for each product
        pricings_for_product = ProductPricing.objects.filter(product=product)
        pricing_display = [f'{pricing.quantity}: ${pricing.price}' for pricing in pricings_for_product]

        product_list.append({
            'figuring': product.image.url if product.image else None,
            'farm': product.farm.name,
            'name': product.product_name,  # Adjust according to your actual field name
            'pricing': pricing_display,
            'id': product.id,
        })

    context = {
        'product_list': product_list,
        'products_page': products_page,
        'entries': entries_per_page,
        'search_query': search_query,
    }

    return render(request, 'all-productManagement.html', context)

################# -------New Product------- #################
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, Event, Farm, Gallery, PageVisit, Product, ProductPricing, Review, WebContent  # Import your Product model


@csrf_exempt
def add_product(request):
    businesses = Business.objects.all()

    if request.method == 'POST':
        farm_name = request.POST['business']
        product_name = request.POST['product_name']
        quantity_in_stock = request.POST['quantity_in_stock']
        description = request.POST['description']
        image = request.FILES.get('image')

        
        prices = request.POST.getlist('price[]')
        quantities = request.POST.getlist('quantity[]')
        volumes = request.POST.getlist('volume[]')
        print(prices,quantities,volumes)

        business_instance = Business.objects.get(uuid=farm_name)
        empty_fields = []  # List to store names of empty fields
        if not farm_name:
            empty_fields.append('Farm Name')
        if not product_name:
            empty_fields.append('Product Name')
        if not quantity_in_stock:
            empty_fields.append('Quantity in Stock')
        if not description:
            empty_fields.append('Description')

        if empty_fields:
            # Print the names of empty fields
            print("The following fields are empty:", ", ".join(empty_fields))
        else: 
            # Create a new Product object and save it to the database
            try:
                # Create the product


                product = Product.objects.create(
                    business_name=business_instance,
                    product_name=product_name,
                    quantity_in_stock=quantity_in_stock,
                    description=description
                )
                # Handle profile picture upload
                if 'photo' in request.FILES:
                    photo = request.FILES['photo']
                    print(photo)
                    # Delete old image if it exists
                    if product.image:
                        product.image.delete(save=False)  # Deletes the file and not the model instance
                        print('deletion complete')
                    
                    # Save new image
                    product.image.save(photo.name, photo, save=False)
                    print('done')

                product.save()

                # Save pricing data to the database
                for price, quantity, volume in zip(prices, quantities, volumes):
                    quantity_with_volume = f"{quantity}{volume}"
                    # Add the product instance to the ProductPricing creation
                    ProductPricing.objects.create(
                        product=product,
                        price=price,
                        quantity=quantity_with_volume,
                    )
            except Exception as e:
                print(f"Error when adding product: {e}")

            messages.success(request, 'Product added successfully!')
            return redirect('Nproduct')  # Redirect to the product list page

    
    return render(request, 'New-product.html',{'businesses': businesses})  # Render the template for the form

#>>>>>>>>>>>>>>>>>>>>>>>  UPDATE Product <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

from django.shortcuts import render, get_object_or_404
from django.core.serializers import serialize
from .models import Product, ProductPricing
import re
from decimal import Decimal

@csrf_exempt
def edit_product(request, pk):
    ing = Farm.objects.all()
    product = get_object_or_404(Product, pk=pk)
    pricings = ProductPricing.objects.filter(product=product)

    if request.method == 'POST':
        # Update the product details
        farm = request.POST.get('farm')  # assuming you have a select input for farm
        farm = get_object_or_404(Farm, pk=farm)
        product.farm = farm
        product.product_name = request.POST.get('product_name')
        product.quantity_in_stock = request.POST.get('quantity_in_stock')    
        product.standard_price = Decimal(request.POST.get('price').replace(',','.'))
        product.description =request.POST.get('description')

        prices = request.POST.getlist('price[]')
        quantities = request.POST.getlist('quantity[]')
        volumes = request.POST.getlist('volume[]')

        # Handle profile picture upload
        if 'image' in request.FILES:
            photo = request.FILES['image']
            # Delete old image if it exists
            if product.image:
                product.image.delete(save=False)  # Deletes the file and not the model instance
            
            # Save new image
            product.image.save(photo.name, photo, save=False)
        
            # Delete all existing pricings for the product
        ProductPricing.objects.filter(product=product).delete()
                # Save pricing data to the database
        for price, quantity, volume in zip(prices, quantities, volumes):
            quantity_with_volume = f"{quantity}{volume}"
            # Add the product instance to the ProductPricing creation
            ProductPricing.objects.create(
                product=product,
                price=price,
                quantity=quantity_with_volume,
            )


        product.save()
        messages.success(request, 'Product updated successfully!')
    
    pricing_data = []
    for pricing in pricings:
        quantity_string = str(pricing.quantity)
        match = re.match(r'(\d+\.?\d*)\s*(\w+)', quantity_string)
        if match:
            pricing_data.append({
                'quantity': match.group(1),
                'unit': match.group(2),
                'price': str(pricing.price)  # Convert Decimal to string
            })

    # Convert pricing_data to a JSON string
    pricings_json = json.dumps(pricing_data)

    context = {
        'product': product,
        'pricings_json': pricings_json,  # Now a JSON string of the pricing data
        'farm': ing
    }

    return render(request, 'update-product.html', context)


def products_view(request):
    products = Product.objects.all()  # Retrieve all products from the database

    # Capture the filter type from the query parameters
    filter_type = request.GET.get('filter')

    # Apply filters based on the filter_type
    if filter_type == 'Popular':
        products = products.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
    elif filter_type == 'Newest':
        products = products.order_by('-created_at')
    elif filter_type == 'Lowest_Price':
        products = products.order_by('standard_price')
    elif filter_type == 'Highest_Price':
        products = products.order_by('-standard_price')
    # Implement the logic for 'Featured' if you have a specific criteria for featured products

    # Pagination
    page_number = request.GET.get('page', 1)
    products_per_page = 5
    paginator = Paginator(products, products_per_page)
    page_obj = paginator.get_page(page_number)

    return render(request, 'product-list.html', {'page_obj': page_obj})



def product_detail(request, pk):
    # Assuming 'product_id' is passed to this view function
    product = Product.objects.filter(id=pk).annotate(average_rating=Avg('review__rating')).first()
    pricings = ProductPricing.objects.filter(product=product)
    # If the product does not exist, 'get_object_or_404' will raise a 404 error.
    if not product:
        product = get_object_or_404(Product, id=pk)
    
        # Exclude the current product and retrieve 4 random products from the same farm
    random_products = Product.objects.filter(farm=product.farm).order_by('?')[:4]
    context = {
        'product': product,
        'roducts': random_products,
        'pricings': pricings
    }

    # Now, 'product.average_rating' contains the average rating, which can be None if there are no reviews
    return render(request, 'product-detail.html', context)


















from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import Business, Product  # Assuming Rating model exists
from django.db.models import Avg

@csrf_exempt  # Use with caution and make sure to properly manage CSRF
def feedback(request):
    farming = Farm.objects.all()
    # costumer = Customer.objects.get(user=request.user)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Handle fetching products for a farm
            farm_name = data.get('farmName')
            product_name = data.get('productName')
            new_rating = data.get('rating')
            feed = data.get('feed')

            if farm_name and not product_name:
                products = Product.objects.filter(
                    farm__name=farm_name
                ).values_list('product_name', flat=True)
                return JsonResponse(list(products), safe=False)
            
            # Handle fetching average rating for a product
            if product_name and not farm_name:
                average_rating = Review.objects.filter(
                    product__product_name=product_name
                ).aggregate(Avg('rating'))['rating__avg']
                return JsonResponse({'average_rating': round(average_rating) if average_rating else 0})
            
            # Retrieve the current costumer profile
            costumer = Customer.objects.get(username=request.user.username)
            # Handle submitting a new rating and feedback
            if product_name and new_rating and feed:
                Review.objects.create(
                    product=Product.objects.get(product_name=product_name),
                    user=costumer,
                    review_text=feed,
                    rating=new_rating
                )
                messages.success(request, 'Successfully Sent The Message!')
                return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # GET request handling here
        return render(request, 'feedback.html', {'farms': farming})

    # Default response if none of the conditions are met
    return JsonResponse({'message': 'Your request was received, but no action was taken. Please check your request format and try again.'})



def dashboard_view(request):
    # Récupérer les données de visite
    visits_data = PageVisit.objects.all().order_by('path')
    paths = [visit.path for visit in visits_data]
    visits = [visit.visit_count for visit in visits_data]

    # Passer les données au template
    context = {
        'paths': paths,
        'visits': visits,
    }
    return render(request, 'testing.html', context)
    
@csrf_exempt
def eventupload(request):
    first_farm = Farm.objects.first()
    
    if request.method == 'POST':
        title = request.POST.get('Title')
        
        # Fetch the WebContent instance based on the title received from the form
        activity_icon_title = request.POST.get('activity_icon')
        try:
            activity_icon = WebContent.objects.get(title=activity_icon_title)
        except WebContent.DoesNotExist:
            activity_icon = None
            messages.error(request, 'Invalid activity icon selected.')
            return render(request, 'event.html')  # Assuming you want to stop processing and show the form again

        description = request.POST.get('feed')
        
        # IMPORTANT: Use getlist to handle multiple files
        images = request.FILES.getlist('files')  # Use 'files' without brackets and ensure this matches your form's input name
        
        # Validate form inputs
        if not title:
            messages.error(request, 'Title is required.')
        elif not activity_icon:
            messages.error(request, 'An icon must be selected.')
        elif not description:
            messages.error(request, 'Description is required.')
        elif not images:
            messages.error(request, 'At least one image is required.')
        else:
            # Create the event
            ev = Event.objects.create(
                farm=first_farm,
                name=title,
                description=description,
                activity_icon=activity_icon
            )
            
            # Associate uploaded images with the event
            for image in images:  # Now 'images' is correctly a list of UploadedFile objects
                Gallery.objects.create(event=ev, image=image)

            messages.success(request, 'Event created successfully!')
            return redirect('profile')  # Adjust the redirection as needed
    
    # Fetch icons for the select dropdown
    icons = Event.objects.all().distinct()# Assuming you want to list WebContent objects as icons
    return render(request, 'event.html', {'events': icons})



def display_feedback(request):
    # Fetch the farm associated with the current user
    try:
        profile = get_object_or_404(Business, username=request.user.username)
        farm = profile.farm
    except farm.DoesNotExist:
        farm = None
    
    feedback_list = []
    if farm:
        # Fetch all feedback for products of this farm
        feedback_list = Review.objects.filter(product__farm=farm).select_related('product').order_by('-review_date')
        feedback_user = Review.objects.select_related('user__userauth_ptr').all().order_by('-review_date')



        unique_users = set(feedback.user for feedback in feedback_user)
        user_profile_urls = {}

        for user in unique_users:
            if user.profile_image:
                user_profile_urls[user.uuid] = request.build_absolute_uri(user.profile_image.url)
            else:
                user_profile_urls[user.uuid] = None  # Or the URL to a default image
    
    return render(request, 'feedback_list.html', {'feedback_list': feedback_list, 'user_profile_urls': user_profile_urls,})



@csrf_exempt
def add_to_cart(request):
    # This assumes you're sending JSON data in the POST request
    data = json.loads(request.body)
    pricing_id = data.get('pricing_id')
    quantity = data.get('quantity', 1)
    volume = data.get('volume')
    
    pricing = get_object_or_404(ProductPricing, id=pricing_id)
    if not pricing.product:
        return JsonResponse({'success': False, 'error': 'Product not found'})
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        volume=volume,
        product=pricing.product,
        defaults={'quantity': quantity},
    )
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    
    return JsonResponse({'success': True})


def cart_items_view(request):
    if request.user.is_authenticated:
        # Attempt to retrieve the user's cart. Assumes one cart per user.
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Handling the POST request to update item quantities
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            new_quantity = request.POST.get('quantity')
            
            # Fetch the specific cart item and update its quantity
            try:
                cart_item = CartItem.objects.get(id=item_id, cart=cart)  # use cart from above
                cart_item.quantity = int(new_quantity)  # Ensure quantity is an integer
                cart_item.save()
                # Redirect back to the cart page to display the updated cart
                return HttpResponseRedirect(request.path_info)
            except CartItem.DoesNotExist:
                # Handle error or notify the user if the cart item does not exist
                pass

        # For GET requests or after POST request processing, fetch cart items again in case of updates
        cart_items = cart.items.all()  # Adjusted to use the cart instance directly
        total_price = cart.get_total_price()  # Calculate the total price including any discounts from coupons
        total_item_instances = cart.items.all().count()
        context = {
            'cart_items': cart_items,
            'total_item_instances':total_item_instances,
            # 'categorical_price' : categorical_price,
            'total_price': total_price,  # Add the total_price to the context
        }
        return render(request, 'shopping-cart.html', context)
    else:
        return redirect('product-detail')  # Adjust as per your login or desired redirect view
    

def bulk_update_cart_items(request):
    data = json.loads(request.body)
    updates = data.get('updates')  # Expecting a list of {id, quantity}
    for update in updates:
        cart_item_id = update.get('id')
        new_quantity = update.get('quantity')
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

        try:
            new_quantity = int(new_quantity)
            if new_quantity < 1:
                cart_item.delete()  # Optionally remove the item if the quantity is less than 1
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
        except (ValueError, TypeError):
            # Handle the error as needed
            pass
    
    return JsonResponse({'status': 'success'})

def apply_coupon(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    data = json.loads(request.body)
    coupon_code = data.get('code')
    discount = 0
    if coupon_code:
        coupon = Coupon.objects.get(code=coupon_code)
        discount = coupon.discount
        print(discount)

    # Assume get_cart_from_request is a hypothetical function you've defined to retrieve the user's cart 
    total = cart.get_total_price()
    if discount > 0:
        total -= (total * discount / 100)
    cart.price=total
    cart.save()
    return JsonResponse({'total': total})



@csrf_exempt
def createcheckoutsession(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    stripe_items = []
    print(stripe_items)

    # Check if a discount code is provided
    discount_code = request.POST.get('coupon-code', None)
    discount = None
    if discount_code:
        try:
            coupon = Coupon.objects.get(code=discount_code, active=True)
            discount = (100 - coupon.discount) / 100  # Convert discount percentage to a multiplier
        except Coupon.DoesNotExist:
            discount = None

    for item in cart_items:
        product = item.product
        product_pricing = product.pricing.get(quantity=item.volume)
        
        # Calculate the unit amount, apply discount if available
        unit_amount = product_pricing.price
        if discount:
            unit_amount *= Decimal(discount)  # Apply discount if there is one

        # Prepare the Stripe line item
        stripe_item = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'images': [product.url],  # Make sure image URLs are absolute
                    'name': product.product_name,
                    'description': product.description,
                },
                'unit_amount': int(unit_amount * 100),  # Convert to cents
            },
            'quantity': item.quantity,
        }
        stripe_items.append(stripe_item)

    # Create the Stripe checkout session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=stripe_items,
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),  # Provide your success URL
            cancel_url=request.build_absolute_uri('/cancel/'),  # Provide your cancel URL
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)})
