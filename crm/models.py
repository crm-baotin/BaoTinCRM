from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=255)

    phone = models.CharField(max_length=20, blank=True)
    cccd = models.CharField(max_length=20, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    province = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=255, blank=True)

    xsell_shb = models.BooleanField(default=False)

    disbursement_date = models.DateField(null=True, blank=True)

    bad_debt = models.BooleanField(default=False)
    bad_debt_year = models.IntegerField(null=True, blank=True)

    late_payment = models.BooleanField(default=False)
    late_payment_year = models.IntegerField(null=True, blank=True)

    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # sale phụ trách
    sales = models.ManyToManyField(
        User,
        blank=True,
        related_name="customers"
    )

    # telegram
    notified_6m = models.BooleanField(default=False)

    def __str__(self):
        return self.name
