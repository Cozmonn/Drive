from django.core.management.base import BaseCommand
from django.utils import timezone
from Drive.models import Farm, Event
from datetime import datetime

class Command(BaseCommand):
    help = "Insère des événements liés aux fermes dans la base de données."

    def handle(self, *args, **options):
        farm1 = Farm.objects.get(name="Golden Spuds Shack")
        farm2 = Farm.objects.get(name="Golden Fields Oils")

        evenements_spuds_shack = [
        {
            "name": "Atelier de Cuisine des Frites",
            "description": "Apprenez les secrets de la préparation des frites parfaites dans notre atelier interactif.",
            "date": datetime(2023, 8, 5, 14, 0)
        },
        {
            "name": "Nuit du Film et Frites",
            "description": "Joignez-vous à nous pour une soirée cinéma en plein air, avec une sélection illimitée de frites.",
            "date": datetime(2023, 8, 20, 19, 0)
        },
        {
            "name": "Dégustation de Variétés de Pommes de Terre",
            "description": "Découvrez la diversité des pommes de terre et comment elles influencent le goût des frites.",
            "date": datetime(2023, 9, 1, 10, 0)
        },
        {
            "name": "Festival des Frites Gourmandes",
            "description": "Un festival célébrant les innovations culinaires dans l'art de faire des frites.",
            "date": datetime(2023, 10, 7, 11, 0)
        },
        {
            "name": "Concours du Meilleur Assaisonnement pour Frites",
            "description": "Mettez vos compétences culinaires à l'épreuve dans notre concours d'assaisonnements pour frites.",
            "date": datetime(2023, 11, 15, 12, 0)
        }
        ]

        for evenement in evenements_spuds_shack:
            Event.objects.get_or_create(farm=farm1, name=evenement["name"], defaults=evenement)

        # Autres événements pour Golden Fields Oils
        evenements_fields_oils = [
            {
                "name": "Séminaire sur les Bienfaits de l'Huile de Colza",
                "description": "Un séminaire éducatif sur les avantages de l'huile de colza pour la santé.",
                "date": datetime(2023, 9, 25, 15, 0)
            },
            {
                "name": "Atelier de Pressage d'Huile",
                "description": "Expérience pratique du processus de pressage de l'huile à partir de graines de colza.",
                "date": datetime(2023, 10, 5, 9, 0)
            },
            {
                "name": "Marché des Producteurs Locaux",
                "description": "Rencontrez les producteurs locaux et découvrez les produits dérivés de l'huile de colza.",
                "date": datetime(2023, 10, 20, 8, 0)
            },
            {
                "name": "Fête de la Récolte du Colza",
                "description": "Célébrez la fin de la saison de récolte du colza avec de la musique, de la nourriture et des festivités.",
                "date": datetime(2023, 11, 10, 13, 0)
            },
            {
                "name": "Conférence sur l'Agriculture Durable",
                "description": "Joignez-vous à des experts discutant des pratiques d'agriculture durable et de l'avenir de la production d'huile.",
                "date": datetime(2023, 12, 5, 10, 0)
            }
        ]

        for evenement in evenements_fields_oils:
            Event.objects.get_or_create(farm=farm2, name=evenement["name"], defaults=evenement)

        self.stdout.write(self.style.SUCCESS("Les données supplémentaires des événements ont été insérées avec succès."))
