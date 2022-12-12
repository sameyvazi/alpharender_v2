from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Q, FloatField
from django.db.models.functions import Coalesce


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

    @classmethod
    def get_balance(cls, user):
        positive_transactions = Sum(
            'transactions__amount',
            filter=Q(transactions__transaction_type=Transaction.CHARGE),
            output_field=FloatField()
        )

        negative_transactions = Sum(
            'transactions__amount',
            filter=Q(transactions__transaction_type=Transaction.PURCHASE),
            output_field=FloatField()
        )

        balance = User.objects.all().filter(pk=user.id).aggregate(
            balance=Coalesce(positive_transactions, 0.00) - Coalesce(negative_transactions, 0.00)
        )

        return balance


# class TransactionArchive(models.Model):
#     CHARGE = 1
#     PURCHASE = 2
#
#     TRANSACTION_TYPE_CHOICES = (
#         (CHARGE, "Charge"),
#         (PURCHASE, "Purchase")
#     )
#
#     user = models.ForeignKey(User, related_name='transactions', on_delete=models.RESTRICT)
#     transaction_type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPE_CHOICES, default=CHARGE)
#     amount = models.DecimalField(max_digits=10, decimal_places=3)
#     create_time = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'transaction'
#
#     def __str__(self):
#         return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"


class UserBalance(models.Model):
    user = models.ForeignKey(User, related_name='balance_records', on_delete=models.RESTRICT)
    balance = models.DecimalField(max_digits=10, decimal_places=3)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_balance'

    def __str__(self):
        return f"{self.user} - {self.balance} - {self.create_time}"

    @classmethod
    def record_user_balance(cls, user):
        positive_transactions = Sum(
            'amount',
            filter=Q(transaction_type=Transaction.CHARGE),
            output_field=FloatField()
        )
        negative_transactions = Sum(
            'amount',
            filter=Q(transaction_type=Transaction.PURCHASE),
            output_field=FloatField()
        )

        user_balance = user.transactions.all().aggregate(
            balance=Coalesce(positive_transactions, 0.00) - Coalesce(negative_transactions, 0.00)
        )

        instance = cls.objects.create(user=user, balance=user_balance['balance'])
        return instance

    @classmethod
    def record_all_users_balance(cls):
        for user in User.objects.all():
            cls.record_user_balance(user)
