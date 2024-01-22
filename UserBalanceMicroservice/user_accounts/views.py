from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AccountBalance
from django.contrib.auth.models import User
from .serializers import DepositFundsSerializer
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
