from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from accounts.models import InvestmentAccount

from .models import InvestmentAccount, InvestmentAccountPermission, Transaction

class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = ('id', 'name', 'description')

class InvestmentAccountPermissionSerializer(serializers.ModelSerializer):
    account = InvestmentAccountSerializer(read_only=True)
    permission = serializers.ChoiceField(choices=InvestmentAccountPermission.PERMISSION_CHOICES)

    class Meta:
        model = InvestmentAccountPermission
        fields = ('id', 'user', 'account', 'permission')

    def validate(self, attrs):
        # Check user permission for the requested action based on context
        user = self.context.get('view').request.user
        account = attrs['account']
        permission = attrs['permission']

        # Allow only view permission for GET requests (unless POST_TRANSACTION)
        if self.context.get('view').action == 'retrieve' and permission not in ('VIEW', 'POST_TRANSACTION'):
            raise serializers.ValidationError(f"User '{user.username}' does not have view permission for account '{account.name}'")

        # For other actions (update, partial update, delete), require full CRUD permission
        elif self.context.get('view').action in ('update', 'partial_update', 'destroy') and permission != InvestmentAccountPermission.CREATE:
            raise serializers.ValidationError(f"User '{user.username}' does not have full CRUD permission for account '{account.name}'")

        return attrs

class TransactionSerializer(serializers.ModelSerializer):
    account = InvestmentAccountSerializer(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'user', 'amount', 'date', 'description')

    def validate(self, attrs):
        # Check user permission for creating transactions
        user = self.context.get('view').request.user
        account = attrs['account']

        # Only allow POST_TRANSACTION permission to create transactions
        if not InvestmentAccountPermission.objects.filter(user=user, account=account, permission=InvestmentAccountPermission.POST_TRANSACTION).exists():
            raise serializers.ValidationError(f"User '{user.username}' cannot create transactions for account '{account.name}'")

        return attrs

class UserInvestmentAccountSerializer(serializers.Serializer):
    investment_accounts = InvestmentAccountPermissionSerializer(many=True)

    def to_representation(self, instance):
        investment_accounts = InvestmentAccountPermission.objects.filter(user=instance)
        return {'investment_accounts': InvestmentAccountPermissionSerializer(investment_accounts, many=True).data}