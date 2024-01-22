from UserBalanceMicroservice.user_accounts.models import AccountBalance
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal


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


class WithdrawFundsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.account = AccountBalance.objects.create(user=self.user, balance=150)
        self.withdraw_url = reverse('withdraw_funds')

    def test_withdraw_funds(self):
        data = {'user_id': self.user.id, 'amount': '50.00'}
        response = self.client.post(self.withdraw_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что баланс уменьшился
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 100)

    def test_withdraw_insufficient_funds(self):
        data = {'user_id': self.user.id, 'amount': '200.00'}
        response = self.client.post(self.withdraw_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetBalanceTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.account = AccountBalance.objects.create(user=self.user, balance=100)
        self.balance_url = reverse('get_balance', kwargs={'user_id': self.user.id})

    def test_get_balance(self):
        response = self.client.get(self.balance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['balance']), Decimal('100.00'))

    def test_get_balance_no_account(self):
        wrong_url = reverse('get_balance', kwargs={'user_id': 99999})
        response = self.client.get(wrong_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
