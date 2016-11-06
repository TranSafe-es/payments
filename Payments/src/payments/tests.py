from django.test import TestCase
from django.test.client import Client
from rest_framework.test import APIClient
from .models import Card, Payment
from appManagement.models import App
import uuid

user_id = str(uuid.uuid4())
card_id1 = str(uuid.uuid4())
card_id2 = str(uuid.uuid4())
app = "token"


class CardsTestCase(TestCase):
    def setUp(self):
        self.c1 = Card.objects.create(user_id=user_id, card_id=card_id1, number="1234567890123456", expire_month="9", expire_year="2017",
                                      cvv2="222", first_name="Rodrigo", last_name="Cunha")
        self.c2 = Card.objects.create(user_id='ola', card_id=card_id2, number="2134567890123456", expire_month="9", expire_year="2017",
                                      cvv2="222", first_name="Paulo", last_name="Pedro")
        self.a1 = App.objects.create(token_id=app, name="Teste")

    def test_payment(self):
        client = APIClient()

        url = "/api/v1/payments/create/"

        data = {'user_id1': user_id, 'user_id2': "ola", 'transaction_id': 'teste', 'amount': '100',
                'description': 'teste', 'callback': 'www.google.pt'}
        response = client.post(path=url, data=data)
        self.assertEqual(response.status_code, 400)

        data = {'user_id1': user_id, 'user_id2': "ola", 'transaction_id': 'teste', 'amount': '100',
                'description': 'teste', 'callback': 'www.google.pt'}

        response = client.post(path=url, data=data, token_ID="teste")
        self.assertEqual(response.status_code, 404)
        print response

        response = client.post(path=url, data=data, token_ID=app)
        self.assertEqual(response.status_code, 302)
