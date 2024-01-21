import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UserBalanceMicroservice.settings')
django.setup()

from UserBalanceMicroservice.services.models import Service


def add_services():
    services_data = [
        {"name": "Premium Ad Placement",
         "description": "Get your ad featured at the top of the listings for maximum visibility."},
        {"name": "Extended Ad Duration", "description": "Keep your ad active for an extended period."},
        {"name": "Ad Boost", "description": "Boost your ad to reach more potential buyers."},
        {"name": "Professional Ad Design", "description": "Let our team design your ad for a professional look."},
        {"name": "Ad Analytics", "description": "Receive detailed analytics on your ad's performance."}
    ]

    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults={'description': service_data['description']}
        )
        if created:
            print(f"Created new service: {service.name}")
        else:
            print(f"Service already exists: {service.name}")


if __name__ == "__main__":
    add_services()
