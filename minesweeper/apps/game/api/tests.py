from minesweeper.apps.game.models import Game

from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler  = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class GameAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testUser', email='test@test.com')
        user_obj.set_password("Passtest")
        user_obj.save()
        game = Game.objects.create(
                user=user_obj,
                name='Test Game 1',
                rows=9,
                columns=9,
                mines=10,
                )

    def test_create_game_error_1(self):
        """ Test a succesfull create
        """
        data = {"name": "Test Create Game", "rows": 4, "columns": 10, "mines": 2}
        url = api_reverse("game-api:game-list-and-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_game_error_2(self):
        """ Test an erronoeus create
        """
        data = {"name": "Test Error Create Game", "rows": 4, "columns": 2, "mines": 20}
        url = api_reverse("game-api:game-list-and-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_game_ok(self):
        """ Test a succesfull create
        """
        url = api_reverse("game-api:game-list-and-create")

        # Add credentials
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        data = {"name": "Test Create Game",
                "rows": 4,
                "columns": 10,
                "mines": 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_make_move_error(self):
        game = Game.objects.first()
        url = game.get_api_url()

        data = {"row": 400, "column": 4}
        # Add credentials
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) # JWT <token>

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_make_move_ok(self):
        game = Game.objects.first()
        url = game.get_api_url()

        data = {"row": 4, "column": 4}
        # Add credentials
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) # JWT <token>

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_game_won(self):
        # TODO
        game = Game.objects.first()
        url = game.get_api_url()

        data = {"row": 4, "column": 4}
        # Add credentials
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) # JWT <token>

        response = self.client.post(url, data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_game_lost(self):
        # TODO
        game = Game.objects.first()
        url = game.get_api_url()

        data = {"row": 4, "column": 4}
        # Add credentials
        user_obj = User.objects.first()
        payload  = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) # JWT <token>

        response = self.client.post(url, data, format='json')
        #self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

