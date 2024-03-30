# views.py
import json
from django.core.files.storage import default_storage
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings



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




# Create your views here.
from distutils.log import error
import email

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse, reverse_lazy
from .form import SignInForm, EditProfileForm


# Create your views here.


#login_view

def logform(request):
    if request.method=='POST':
        username = request.POST['username']
        print(request.POST['username'])
        password = request.POST['password']
        print(request.POST['password'])
        user = authenticate(request, username=username, password=password)
        print('logged in')
        login(request, user)
        print('logged in')
        return redirect('profile')
    else:
        return render(request, 'login.html')

#sign_up_view
def register_user(request):
    if request.method=='POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.warning(request,("Please complete ur signing up"))
            return redirect('profile')
        else:
            messages.warning(request,("There was an error Logging In, Please try again!"))
    else:
        form=SignInForm()
    return render(request, 'signup.html', {
            'form':form,
    })


def logoutt(request):
    logout(request)
    messages.success(request, ("Logging Out Successfully"))
    return redirect('login')



from django.shortcuts import render
from .models import Business, Cart, Customer, PageVisit, ProductPricing, Review, UserAuth

def profile_view(request):
    print(request.user)
    profile = UserAuth.objects.get(username=request.user)
    print(profile.profile_image.url)
    context = {'profile': profile}
    return render(request, 'client-view.html', context)




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





################# -------UPDATE------- #################
@csrf_exempt
def update_user_information(request):
    print(request.user)
    profile = UserAuth.objects.get(username=request.user)
    profile_picture_url = request.build_absolute_uri(profile.profile_image.url)  # Construct absolute URL

    if request.method == 'POST':
        # Extract form data
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
            file_path = os.path.join(settings.MEDIA_ROOT, 'profile_images/', photo.name)
            with default_storage.open(file_path, 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)
            # Update user's profile picture URL
            request.user.profile_image = file_path

        # Update user information
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.shipping_address = shipping_address

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
            user.set_password(new_password1)
            update_session_auth_hash(request, user)  # Update session to prevent logout

        user.save()
        #messages.success(request, "Your information has been updated successfully.")
        return redirect('UpdateProfile')  # Redirect to user profile page or any other page

    return render(request, 'Cupdate.html', {'profile': profile, 'profile_picture_url': profile_picture_url})


def update_business(request):
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
        request.user.save()

        messages.success(request, "Business information updated successfully.")
        return redirect('profile')  # Redirect to profile or any other relevant page

    return render(request, 'update_business.html')  # Replace 'update_business.html' with your template path





################# -------New Product------- #################
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product  # Import your Product model


@csrf_exempt
def add_product(request):
    businesses = Business.objects.all()

    if request.method == 'POST':
        farm_name = request.POST['business']
        product_name = request.POST['product_name']
        quantity_in_stock = request.POST['quantity_in_stock']
        description = request.POST['description']
        image = request.FILES.get('image')
        print("Farm Name:", farm_name)
        print("Product Name:", product_name)
        print("Quantity in Stock:", quantity_in_stock)
        print("Description:", description)
        
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

                if image:
                    product.image.save(image.name, image, save=True)

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


# def feedback(request):
#     data = json.loads(request.body)
#     selected_option = data.get('selectedOption')
#     print(selected_option)
#     return render(request,'feedback.html',{})

from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import Business, Product  # Assuming Rating model exists
from django.db.models import Avg

@csrf_exempt  # Use with caution and make sure to properly manage CSRF
def feedback(request):
    businesses = Business.objects.all()
    print(request.user)
    # costumer = Customer.objects.get(user=request.user)
    if request.method == "POST":
        try:
            print(request.body)
            data = json.loads(request.body)
            
            # Handle fetching products for a farm
            farm_name = data.get('farmName')
            product_name = data.get('productName')
            new_rating = data.get('rating')
            feed = data.get('feed')

            if farm_name and not product_name:
                products = Product.objects.filter(
                    business_name__business_name=farm_name
                ).values_list('product_name', flat=True)
                return JsonResponse(list(products), safe=False)
            
            # Handle fetching average rating for a product
            if product_name and not farm_name:
                average_rating = Review.objects.filter(
                    product__product_name=product_name
                ).aggregate(Avg('rating'))['rating__avg']
                return JsonResponse({'average_rating': round(average_rating) if average_rating else 0})
            
            
            print(product_name,new_rating,feed, request.user)
                    # Retrieve the current business profile
            costumer = Customer.objects.get(username=request.user.username)
            print(product_name,new_rating,feed, costumer)
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
        return render(request, 'feedback.html', {'farms': businesses})



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
    
