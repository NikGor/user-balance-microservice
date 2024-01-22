from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AccountBalance
from django.contrib.auth.models import User
from .serializers import DepositFundsSerializer, WithdrawFundsSerializer
from drf_yasg.utils import swagger_auto_schema
from django.db.models import F


class DepositFunds(APIView):
    @swagger_auto_schema(request_body=DepositFundsSerializer)
    def post(self, request):
        serializer = DepositFundsSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            amount = serializer.validated_data.get('amount')

            try:
                user = User.objects.get(id=user_id)
                account, created = AccountBalance.objects.get_or_create(
                    user=user,
                    defaults={'balance': 0}
                )

                # Используем F() для избежания гонки условий и обеспечения правильного обновления баланса
                account.balance = F('balance') + amount
                account.save()
                account.refresh_from_db()

                return Response({'message': 'Funds successfully deposited.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            except (TypeError, ValueError):
                return Response({'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)


class WithdrawFunds(APIView):
    @swagger_auto_schema(request_body=WithdrawFundsSerializer)
    def post(self, request):
        serializer = WithdrawFundsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data['user_id']
        amount = serializer.validated_data['amount']

        # Выделяем проверку пользователя в отдельный метод
        user, user_error_response = self.get_user(user_id)
        if user_error_response:
            return user_error_response

        # Выделяем проверку и обновление баланса в отдельный метод
        balance_update_response = self.update_balance(user, amount)
        return balance_update_response

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id), None
        except User.DoesNotExist:
            return None, Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update_balance(self, user, amount):
        account = AccountBalance.objects.filter(user=user).first()
        if not account or account.balance < amount:
            return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

        account.balance = F('balance') - amount
        account.save()
        account.refresh_from_db()

        return Response({'message': 'Funds successfully withdrawn.'}, status=status.HTTP_200_OK)


class GetBalance(APIView):
    @swagger_auto_schema(responses={200: 'balance: decimal'})
    def get(self, request, user_id):
        try:
            account = AccountBalance.objects.get(user_id=user_id)
            return Response({'balance': account.balance}, status=status.HTTP_200_OK)
        except AccountBalance.DoesNotExist:
            return Response({'error': 'Account balance not found.'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
