
from .models import Product, ProductPricing

def create_products_and_pricing(product_data):
    products = []
    pricings = []

    for data in product_data:
        product = Product(
            product_name=data['product_name'],
            description=data['description'],
            quantity_in_stock=data['quantity_in_stock'],
            business_name=data['business_name'],
            image=data['image_path']
        )
        products.append(product)

        for pricing_data in data['pricing_data']:
            pricing = ProductPricing(
                product=product,
                quantity=pricing_data['quantity'],
                price=pricing_data['price']
            )
            pricings.append(pricing)

    Product.objects.bulk_create(products)
    ProductPricing.objects.bulk_create(pricings)

product_data = [
    {
        "product_name": "La Frite d'Opale",
            "description": "Fresh fries made on the Opal Coast in Rixens from local potatoes. Potato variety: Artémis. Shelf life (DLC): 7 days. Caliber: 10 mm. Fry length 7 to 8 cm. Artisanal quality product.",
            "quantity_in_stock": 100,
        "business_name": "",
        "pricing_data": [
            {
            "quantity": "1kg",
            "price": 1.80
            },
            {
            "quantity": "2.5kg",
            "price": 4.10
            },
            {
            "quantity": "10kg",
            "price": 15.00
                }
        ] 
    },
    {
        "product_name": "Huile de Colza",
        "description": "Huile de Colza pressed  from rapeseed.  It is  cold pressed to preserve all the flavors and nutrients such as proteins, carbohydrates and lipids.  This vegetable oil cannot be heated and is therefore reserved for seasoning your dishes/salads. It is recommended to store it away from air and light.  This rapeseed vegetable oil is rich in Omega 3 and antioxidants which helps protect your cells. It is also excellent for cardiovascular health and helps regulate cholesterol.",
        "quantity_in_stock": 100,
        "business_name": "",
        "pricing_data": [
            {
            "quantity": "50 cl",
            "price": 4.50
            },
            {
            "quantity": "1 L",
            "price": 7.50
            },
            {
            "quantity": "5 L",
            "price": 30.00
            }
        ]
    },
    {
            "product_name": "Huile de Lin",
            "description": "Huile de Lin (Flaxseed oil) is sold in 50cl bottles. It is pressed cold to preserve all the goodness and the nutritional elements.  Like rapeseed oil, it cannot be heated and is for seasoning salads.  It is fragile and should be stored in a cool, dark place.  Huile de Lin is known for its medicinal properties.  Its high concentration of Omega 3 and 9 helps with cardiovascular disease. Omega 3 and 9 reduce blood pressure and bad cholesterol.",
            "quantity_in_stock": 100,
            "pricing_data": [
                {
                "quantity": "50cl",
                "price": 6.50
                }
            ]
    },
    {
            "product_name": "Huile de Tournesol",
            "description": "Sunflower oil. It is available in 50cl and 100cl bottles. It can be heated and used for frying, sauteing and baking.  It is rich in Vitamin E and Omega 6 which are good for your body.  Omega 6 helps prevent cholesterol, strengthens the immune system and slows down aging.",
            "quantity_in_stock": 100, 
            "business_name": "Business 1",
            "pricing_data": [
                {
                "quantity": "50cl",
                "price": 4.50
                },
                {
                "quantity": "100cl",
                "price": 7.50
                }
            ]
    },
    {
            "product_name": "Les Pâtes Fusilli",
            "description": "These Fusilli shaped pastas are made with durum wheat flour and water only. They cook in 5 to 9 minutes, depending on your preference.  They are available in 300g, 600g bags and bulk by the kilo.  The bulk price is 6€ per kilo.",
            "quantity_in_stock": 100,
            "business_name": "",
            "pricing_data": [
                {
                "quantity": "300g",
                "price": "2.30€"
                },
                {
                "quantity": "600g",
                "price": "4.40€"
                },
                {
                "quantity": "1kg",
                "price": "6.00€"
                }
            ]
    },
    {
            "product_name": "Les Pâtes Penne",
            "description": "Les Penne are shaped like tubes. They are made from wheat flour and water only. The cooking time is between 12 to 14 minutes according to your preference. They are available in 400g and 700g packets.",
            "quantity_in_stock": 100,
            "business_name": "",
            "pricing_data": [
                {
                "quantity": "400g",
                "price": "3.10€"
                },
                {
                "quantity": "700g",
                "price": "5.20€"
                },
                {
                "quantity": "1kg",
                "price": "6.00€"  
                }
            ]
    },
    {
            "product_name": "Les Pâtes Coquillettes",
            "description": "Les pâtes coquillettes se cuisent en 4 et 7 minutes selon vos goûts. Elles sont composées à base de farines et d'eau seulement. Nous les proposons en sachets de 600 grammes, 1 kg et en vrac. Elles sont parfaites pour les petits et grands enfants et pour une cuisine rapide!",
            "quantity_in_stock": 100,
            "business_name": "Ferme du Bois de Cosset",
            "pricing_data": [
                {
                "quantity": "600g",
                "price": "4.30€"
                },
                {
                "quantity": "1kg",
                "price": "6.80€"
                },
                {
                "quantity": "1kg",
                "price": "6.00€" 
                }
            ]
    },
    {
            "product_name": "La Farine",
            "description": "La farine est souvent la plus connue des ménagères. Elle peut s'utiliser pour faire tous types de recettes salées ou sucrées. Elle est moulue sur meule de pierre, ce qui conserve tous ses nutriments et saveurs.  Our flours are crushed on a grindstone millstone, which means your flour loses none of its flavor and retains all the nutrients of the wheat.",
            "quantity_in_stock": 100, 
            "business_name": "",
            "pricing_data": [
                {
                "quantity": "700g",
                "price": "2.00€"
                },
                {
                "quantity": "1.3kg",
                "price": "3.30€"
                },
                {
                "quantity": "5kg",
                "price": "11.50€"
                }
            ]
    }

        # Add more product data as needed
]
create_products_and_pricing(product_data)

print("Products and pricing created successfully!")
