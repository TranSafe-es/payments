from django.test import TestCase
from rest_framework.test import APIClient
from .models import Card
import uuid
import json

user_id = str(uuid.uuid4())
card_id1 = str(uuid.uuid4())
card_id2 = str(uuid.uuid4())


class CardsTestCase(TestCase):
    def setUp(self):

        self.c1 = Card.objects.create(user_id=user_id, card_id=card_id1, number="1234567890123456", expire_month="9", expire_year="2017",
                                      cvv2="222", first_name="Rodrigo", last_name="Cunha")
        self.c2 = Card.objects.create(user_id=user_id, card_id=card_id2, number="2134567890123456", expire_month="9", expire_year="2017",
                                      cvv2="222", first_name="Rodrigo", last_name="Cunha")

    def test_cards(self):
        client = APIClient()

        url = "/api/v1/cards/"

        data = {'user_id': user_id, 'number': '1234567890123456', 'expire_month': '9', 'expire_year': '2017',
                'cvv2': '222', 'first_name': 'Rodrigo', 'last_name': 'Cunha'}

        response = client.post(path=url, data=data)
        self.assertEqual(response.status_code, 401)

        data = {'user_id': user_id, 'card_id': card_id1, 'expire_month': '10', 'expire_year': '2018'}

        response = client.put(path=url, data=data)
        self.assertEqual(response.status_code, 200)

        data = {'user_id': user_id, 'card_id': card_id1}

        response = client.delete(path=url, data=data)
        self.assertEqual(response.status_code, 200)

        data = {'user_id': user_id}

        response = client.get(path=url, data=data)
        self.assertEqual(response.status_code, 200)
