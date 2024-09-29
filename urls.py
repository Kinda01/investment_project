from django.urls import path
from .views import (
    InvestmentAccountListCreateAPIView,
    InvestmentAccountRetrieveUpdateDestroyAPIView,
    UserInvestmentAccountListCreateAPIView,
    UserInvestmentAccountRetrieveUpdateDestroyAPIView,
    TransactionListCreateAPIView,
    TransactionRetrieveUpdateDestroyAPIView,
    UserTransactionsAPIView,
)

urlpatterns = [
    path('investment-accounts/', InvestmentAccountListCreateAPIView.as_view(), name='investment_account_list_create'),
    path('investment-accounts/<int:pk>/', InvestmentAccountRetrieveUpdateDestroyAPIView.as_view(), name='investment_account_retrieve_update_destroy'),
    path('user-investment-accounts/', UserInvestmentAccountListCreateAPIView.as_view(), name='user_investment_account_list_create'),
    path('user-investment-accounts/<int:pk>/', UserInvestmentAccountRetrieveUpdateDestroyAPIView.as_view(), name='user_investment_account_retrieve_update_destroy'),
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transaction_list_create'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyAPIView.as_view(), name='transaction_retrieve_update_destroy'),
    path('user-transactions/', UserTransactionsAPIView.as_view(), name='user_transactions'),
]