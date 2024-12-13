import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from djangoapp.models import CarMake, CarModel  # Adjust import paths as necessary

# Function to populate data
def initiate():
    car_make_data = [
        {"name": "Toyota", "description": "Reliable Japanese car brand"},
        {"name": "Ford", "description": "Popular American car brand"},
    ]

    car_model_data = [
        {"car_make": "Toyota", "name": "Corolla", "type": "SEDAN", "year": 2020},
        {"car_make": "Toyota", "name": "RAV4", "type": "SUV", "year": 2021},
        {"car_make": "Ford", "name": "Fiesta", "type": "WAGON", "year": 2019},
    ]

    for make in car_make_data:
        car_make, created = CarMake.objects.get_or_create(
            name=make['name'],
            defaults={'description': make['description']}
        )

    for model in car_model_data:
        car_make = CarMake.objects.get(name=model['car_make'])
        CarModel.objects.get_or_create(
            car_make=car_make,
            name=model['name'],
            defaults={'type': model['type'], 'year': model['year']}
        )


if __name__ == "__main__":
    initiate()
