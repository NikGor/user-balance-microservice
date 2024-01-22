from rest_framework import serializers


class DepositFundsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)


class WithdrawFundsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
