from django.db import models
from django.contrib.auth.models import User
from datetime import date

YEAR_CHOICES = [(y, y) for y in range(2000, date.today().year + 1)]

class Customer(models.Model):
    xsell_shb = models.BooleanField("Xsell SHB", default=False)

    disbursement_date = models.DateField("Ngày giải ngân", null=True, blank=True)

    name = models.CharField("Họ tên", max_length=100)
    phone = models.CharField("Số điện thoại", max_length=20)
    cccd = models.CharField("CCCD", max_length=20)
    date_of_birth = models.DateField(
    null=True,
    blank=True,
    verbose_name="Ngày sinh"
)
    address = models.CharField("Nơi ở", max_length=255)
    province = models.CharField("Tỉnh", max_length=100)

    bad_debt = models.BooleanField("Nợ xấu", default=False)
    bad_debt_year = models.IntegerField("Nợ xấu từ năm", choices=YEAR_CHOICES, null=True, blank=True)

    late_payment = models.BooleanField("Trả chậm", default=False)
    late_payment_year = models.IntegerField("Trả chậm từ năm", choices=YEAR_CHOICES, null=True, blank=True)

    company = models.CharField("Công ty", max_length=255, blank=True)
    created_at = models.DateField("Ngày nhập", auto_now_add=True)

    note = models.TextField("Ghi chú", blank=True, null=True)

    sales = models.ManyToManyField(User, blank=True, related_name="customers")

    def __str__(self):
        return self.name
