from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    CHARGE = 1
    PURCHASE = 2

    TRANSACTION_TYPE_CHOICES = (
        (CHARGE, "Charge"),
        (PURCHASE, "Purchase")
    )

    user = models.ForeignKey(User, related_name='transactions', on_delete=models.RESTRICT)
    transaction_type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPE_CHOICES, default=CHARGE)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction'

    def __str__(self):
        return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"


class UserBalance(models.Model):
    user = models.ForeignKey(User, related_name='balance_records', on_delete=models.RESTRICT)
    balance = models.DecimalField(max_digits=10, decimal_places=3)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.balance} - {self.create_time}"
