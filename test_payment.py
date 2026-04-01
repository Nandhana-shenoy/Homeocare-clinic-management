import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeo.settings')
django.setup()

from django.test import Client
from homeo.models import user_tbl, add_medicine_tbl, Payment

print("Testing Payment Flow...")
user, created = user_tbl.objects.get_or_create(
    email='testuser@gmail.com',
    defaults={'name': 'Test User', 'password': 'password123', 'contact': '1234567890'}
)

medicine, med_created = add_medicine_tbl.objects.get_or_create(
    medicine_name='Test Med',
    defaults={'description': 'Test Desc', 'price': 100.00, 'stock': 10}
)

client = Client()

# Login fake
session = client.session
session['uid'] = user.id
session.save()

# Submit buy
response = client.post(f'/buy_medicine/{medicine.id}/', {
    'card_holder': 'Testing',
    'card_number': '1111222233334444',
    'cvv': '123',
    'card_type': 'credit',
    'bank_name': 'My Bank'
})
print("Buy status code:", response.status_code)

# Check view
response = client.get('/user_view_payment/')
print("View payment status:", response.status_code)
if response.status_code == 200:
    print(f"Number of payments rendered: {len(response.context['payments'])}")
