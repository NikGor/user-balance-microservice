from UserBalanceMicroservice.user_accounts.models import AccountBalance
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal


class DepositFundsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.url = reverse('deposit_funds')

    def test_deposit_funds(self):
        data = {'user_id': self.user.id, 'amount': 100.0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        account = AccountBalance.objects.get(user=self.user)
        account.refresh_from_db()

        self.assertEqual(account.balance, 100.0)


class DepositFundsTests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # URL для эндпойнта deposit
        self.deposit_url = reverse('deposit_funds')

    def test_deposit_funds(self):
        # Создаем данные для POST-запроса
        data = {
            'user_id': self.user.id,
            'amount': '50.00'  # Используем строку для представления десятичных значений
        }
        # Отправляем POST-запрос
        response = self.client.post(self.deposit_url, data, format='json')

        # Проверяем, что ответ имеет статус HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что баланс пользователя увеличился
        account = AccountBalance.objects.get(user=self.user)
        self.assertEqual(account.balance, Decimal(data['amount']))

    def test_deposit_with_invalid_user(self):
        # Создаем данные для POST-запроса с некорректным ID пользователя
        data = {
            'user_id': 999,
            'amount': '50.00'
        }
        # Отправляем POST-запрос
        response = self.client.post(self.deposit_url, data, format='json')

        # Проверяем, что ответ имеет статус HTTP 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
