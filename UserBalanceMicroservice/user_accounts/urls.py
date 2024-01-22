from django.urls import path
from UserBalanceMicroservice.user_accounts.views import DepositFunds

urlpatterns = [
    path('deposit/', DepositFunds.as_view(), name='deposit_funds'),
]
