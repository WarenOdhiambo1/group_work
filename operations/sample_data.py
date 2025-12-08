from operations.models import Activity

SAMPLE_ACTIVITIES = [
    {
        'name': 'Kayak Adventure',
        'type': 'RENTAL',
        'price': 45.00,
        'description': 'Single kayak rental for 2 hours',
        'image_url': 'https://i.pinimg.com/564x/35/60/66/356066532997261490e1e0e1e1e1e1e1.jpg'
    },
    {
        'name': 'Paddleboard Experience',
        'type': 'RENTAL',
        'price': 35.00,
        'description': 'Stand-up paddleboard rental',
        'image_url': 'https://i.pinimg.com/564x/10/11/33/101133966006618589300e1e0e1e1e1e.jpg'
    },
    {
        'name': 'River Guided Tour',
        'type': 'TOUR',
        'price': 75.00,
        'description': 'Guided tour through scenic waterways',
        'image_url': 'https://i.pinimg.com/564x/50/03/22/500322458542650860e1e0e1e1e1e1e1.jpg'
    },
    {
        'name': 'Sunset Kayaking',
        'type': 'TOUR',
        'price': 85.00,
        'description': 'Evening kayak tour at sunset',
        'image_url': 'https://i.pinimg.com/564x/67/86/36/678636237640439590e1e0e1e1e1e1e1.jpg'
    },
    {
        'name': 'Family Water Adventure',
        'type': 'TOUR',
        'price': 120.00,
        'description': 'Family-friendly water activities',
        'image_url': 'https://i.pinimg.com/564x/11/62/49/116249234130017624e1e0e1e1e1e1e1.jpg'
    },
    {
        'name': 'Fishing Expedition',
        'type': 'TOUR',
        'price': 95.00,
        'description': 'Guided fishing tour with equipment',
        'image_url': 'https://i.pinimg.com/564x/30/75/11/307511480823438540e1e0e1e1e1e1e1.jpg'
    }
]

def populate_activities():
    for data in SAMPLE_ACTIVITIES:
        Activity.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
    print(f"✓ Created {len(SAMPLE_ACTIVITIES)} activities")
