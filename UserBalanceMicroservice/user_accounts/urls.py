from django.urls import path
from UserBalanceMicroservice.user_accounts.views import DepositFunds, WithdrawFunds, GetBalance

urlpatterns = [
    path('deposit/', DepositFunds.as_view(), name='deposit_funds'),
    path('withdraw/', WithdrawFunds.as_view(), name='withdraw_funds'),
    path('balance/<int:user_id>/', GetBalance.as_view(), name='get_balance'),
]
