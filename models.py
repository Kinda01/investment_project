from django.db import models
from django.contrib.auth.models import User
from accounts.models import InvestmentAccount

class InvestmentAccount(models.Model):
    app_label = 'accounts'  # Add this line
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class InvestmentAccountPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    VIEW = 'VIEW'
    CREATE = 'CREATE'
    READ = 'READ'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    POST_TRANSACTION = 'POST_TRANSACTION'
    PERMISSION_CHOICES = (
        (VIEW, 'View'),
        (CREATE, 'Create'),
        (READ, 'Read'),
        (UPDATE, 'Update'),
        (DELETE, 'Delete'),
        (POST_TRANSACTION, 'Post Transaction'),
    )
    permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = (('user', 'account'),)

    def __str__(self):
        return f"{self.user.username} - {self.account.name} ({self.get_permission_display()})"

class Transaction(models.Model):
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.account.name} - Transaction: {self.amount} ({self.date})"