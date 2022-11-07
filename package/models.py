from django.db import models


class Package(models.Model):
    TYPE_CPU = 1
    TYPE_GPU = 2

    TYPES = (
        (TYPE_CPU, "CPU"),
        (TYPE_GPU, "GPU")
    )

    type = models.PositiveIntegerField(default=TYPE_CPU, choices=TYPES)
    title = models.CharField(max_length=128)
    machine_limit = models.PositiveSmallIntegerField()
    pricing = models.DecimalField(max_digits=4, decimal_places=2)
    per_second = models.DecimalField(max_digits=12, decimal_places=10)
    priority = models.PositiveSmallIntegerField()
    ghz = models.PositiveIntegerField()
    sort_order = models.PositiveSmallIntegerField()
    users = models.TextField(blank=True)
    is_unlimited = models.BooleanField()
    black_list = models.CharField(max_length=256, null=True, blank=True)

    is_active = models.BooleanField()
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'package'

    def __str__(self):
        return self.title
