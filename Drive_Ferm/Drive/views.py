# views.py
import json
from django.core.files.storage import default_storage
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, render, redirect
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .functions import generate_unique_username



#stripe_keys
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

def home(request):
    return render(request, "index.html")

def visiteVirtuelle(request):
    return render(request, "visite_virtuelle.html")

def productListing(request):
    return render(request, "products.html")

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
from .models import Event, Gallery
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

@csrf_exempt
def pay(request):
    return render(request, 'paiement.html')

@csrf_exempt
def create_checkout_session(request):
    # Mocking cart items for testing
    mock_cart_items = [
        {"product_name": "HUILE DE COLZA", "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "price": 10.99, "quantity": 2, "image_url": 'https://picsum.photos/200'},
        {"product_name": "LES PÂTES COQUILLETTES", "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "price": 15.99, "quantity": 1, "image_url": 'https://picsum.photos/200'},
    ]
    
    # Prepare line items for the payment session
    line_items = []
    for item in mock_cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'images': [item["image_url"]],
                    'name': item["product_name"],
                    'description': item["description"],
                },
                'unit_amount': int(item["price"] * 100),  # Price in cents
            },
            'quantity': item["quantity"],
        })

    # Create a payment session with Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )

    return HttpResponseRedirect(session.url)

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
                    print(price,quantity_with_volume)
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
