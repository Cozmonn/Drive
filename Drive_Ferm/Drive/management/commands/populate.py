from datetime import date
from django.core.management.base import BaseCommand
from Drive.models import Farm

class Command(BaseCommand):
    help = 'Insère les données initiales pour les fermes.'

    def handle(self, *args, **options):
        # Données pour Golden Spuds Shack
        Farm.objects.get_or_create(
            name="Golden Spuds Shack",
            defaults={
                'description': "Spécialisée dans la création artisanale de frites parfaites, Golden Spuds Shack valorise les pratiques agricoles durables pour cultiver des pommes de terre de qualité supérieure.",
                'founded_date': date(1856, 4, 9),
                'founders': "Alex Johnson, Jamie Smith",
                'location': "Springfield, États-Unis",
                'number_of_employees': 20
            }
        )

        # Données pour Golden Fields Oils
        Farm.objects.get_or_create(
            name="Golden Fields Oils",
            defaults={
                'description': "Golden Fields Oils produit une gamme de produits d'huile de haute qualité, incluant l'huile de colza, et une sélection de pâtes comme les fusilli et les coquillettes.",
                'founded_date': date(1986, 5, 15),
                'founders': "Casey Turner, Morgan Blake",
                'location': "Green Valley, États-Unis",
                'number_of_employees': 35
            }
        )

        self.stdout.write(self.style.SUCCESS('Les données des fermes ont été insérées avec succès.'))