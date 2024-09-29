from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import InvestmentAccount
from django.db.models import Sum

from .models import InvestmentAccount, InvestmentAccountPermission, Transaction
from .serializers import (
    InvestmentAccountSerializer,
    InvestmentAccountPermissionSerializer,
    TransactionSerializer,
    UserInvestmentAccountSerializer,
)


class InvestmentAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        if pk:
            # Retrieve specific investment account
            try:
                account = InvestmentAccount.objects.get(pk=pk)
                # Check user permission before returning details
                if not InvestmentAccountPermission.objects.filter(user=user, account=account).exists():
                    return Response({"error": "You do not have permission to view this account"}, status=status.HTTP_403_FORBIDDEN)
                serializer = InvestmentAccountSerializer(account)
                return Response(serializer.data)
            except InvestmentAccount.DoesNotExist:
                return Response({"error": "Investment account not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all investment accounts for the user
            accounts = InvestmentAccount.objects.filter(investmentaccountpermission__user=user)
            serializer = InvestmentAccountSerializer(accounts, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = InvestmentAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Grant full CRUD permission to the user who created the account
            InvestmentAccountPermission.objects.create(
                user=request.user, account=serializer.saved_object, permission=InvestmentAccountPermission.CREATE
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            account = InvestmentAccount.objects.get(pk=pk)
            # Check user permission before updating
            if not InvestmentAccountPermission.objects.filter(user=request.user, account=account, permission=InvestmentAccountPermission.CREATE).exists():
                return Response({"error": "You do not have permission to update this account"}, status=status.HTTP_403_FORBIDDEN)
            serializer = InvestmentAccountSerializer(account, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvestmentAccount.DoesNotExist:
            return Response({"error": "Investment account not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            account = InvestmentAccount.objects.get(pk=pk)
            # Check user permission before deleting
            if not InvestmentAccountPermission.objects.filter(user=request.user, account=account, permission=InvestmentAccountPermission.CREATE).exists():
                return Response({"error": "You do not have permission to delete this account"}, status=status.HTTP_403_FORBIDDEN)
            account.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvestmentAccount.DoesNotExist:
            return Response({"error": "Investment account not found"}, status=status.HTTP_404_NOT_FOUND)


class InvestmentAccountPermissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        try:
            permission = InvestmentAccountPermission.objects.get(pk=pk)
            # Check user ownership of the permission
            if permission.user != user:
                return Response({"error": "You do not have permission to view this permission"}, status=status.HTTP_403_FORBIDDEN)
            serializer = InvestmentAccountPermissionSerializer(permission)
            return Response(serializer.data)
        except InvestmentAccountPermission.DoesNotExist:
            return Response({"error": "Investment account permission not found"}, status=status.HTTP_404_NOT_FOUND)


class TransactionView():
    from rest_framework import status
from rest_framework.response import Response

from .models import Transaction


class TransactionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user

        if pk:
            # Retrieve transactions for a specific investment account
            try:
                account = InvestmentAccount.objects.get(pk=pk)
                # Check user permission to view transactions
                if not InvestmentAccountPermission.objects.filter(user=user, account=account, permission__in=['VIEW', 'POST_TRANSACTION']).exists():
                    return Response({"error": "You do not have permission to view transactions for this account"}, status=status.HTTP_403_FORBIDDEN)

                transactions = Transaction.objects.filter(account=account)
                serializer = TransactionSerializer(transactions, many=True)
                return Response(serializer.data)
            except InvestmentAccount.DoesNotExist:
                return Response({"error": "Investment account not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all transactions for the user
            transactions = Transaction.objects.filter(user=user)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            # Check user permission to update transaction
            if not InvestmentAccountPermission.objects.filter(user=request.user, account=transaction.account, permission=InvestmentAccountPermission.CREATE).exists():
                return Response({"error": "You do not have permission to update this transaction"}, status=status.HTTP_403_FORBIDDEN)

            serializer = TransactionSerializer(transaction, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            # Check user permission to delete transaction
            if not InvestmentAccountPermission.objects.filter(user=request.user, account=transaction.account, permission=InvestmentAccountPermission.CREATE).exists():
                return Response({"error": "You do not have permission to delete this transaction"}, status=status.HTTP_403_FORBIDDEN)

            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)