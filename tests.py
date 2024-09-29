import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import InvestmentAccount, UserInvestmentAccount, Transaction
from .serializers import InvestmentAccountSerializer, TransactionSerializer

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_with_view_permissions(api_client):
    user = User.objects.create_user(username='test_user')
    investment_account = InvestmentAccount.objects.create(name='Test Investment Account')
    UserInvestmentAccount.objects.create(user=user, investment_account=investment_account, permission_level__name='VIEW')
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def user_with_crud_permissions(api_client):
    user = User.objects.create_user(username='test_user')
    investment_account = InvestmentAccount.objects.create(name='Test Investment Account')
    UserInvestmentAccount.objects.create(user=user, investment_account=investment_account, permission_level__name='CRUD')
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def user_with_post_permissions(api_client):
    user = User.objects.create_user(username='test_user')
    investment_account = InvestmentAccount.objects.create(name='Test Investment Account')
    UserInvestmentAccount.objects.create(user=user, investment_account=investment_account, permission_level__name='POST')
    api_client.force_authenticate(user=user)
    return api_client

@pytest.mark.django_db
def test_create_investment_account(api_client_with_crud_permissions):
    url = reverse('investment_account_list_create')
    data = {'name': 'Test Investment Account 2'}
    response = api_client_with_crud_permissions.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert InvestmentAccount.objects.count() == 2

@pytest.mark.django_db
def test_create_investment_account_with_view_permissions(api_client_with_view_permissions):
    url = reverse('investment_account_list_create')
    data = {'name': 'Test Investment Account 2'}
    response = api_client_with_view_permissions.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

# ... other test cases for CRUD operations, total balance calculation, date range filtering ...