from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    title = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    STATUS_OPEN = 1
    STATUS_CLOSE = 2
    STATUS_ANSWERED = 3
    STATUS_PENDING = 4

    STATUS_TYPES = (
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSE, "Close"),
        (STATUS_ANSWERED, "Answered"),
        (STATUS_PENDING, "Pending"),
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tickets')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='tickets')
    subject = models.CharField(max_length=256)
    message = models.TextField(blank=True)
    file = models.CharField(max_length=256, blank=True, null=True)

    status = models.PositiveIntegerField(default=STATUS_OPEN, choices=STATUS_TYPES)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ticket'

    def __str__(self):
        return self.subject


class Reply(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tickets_replies')
    message = models.TextField(blank=True)
    file = models.CharField(max_length=256)
