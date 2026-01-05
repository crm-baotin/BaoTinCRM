from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import date
from .models import Customer
from .exports import export_customers_excel
from .telegram import check_and_notify_6_months


# ================= LOGIN =================
def sale_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user and user.is_active and not user.is_superuser:
            login(request, user)
            return redirect("/dashboard/")

        return render(request, "login.html", {"error": "Sai tài khoản hoặc mật khẩu"})

    return render(request, "login.html")


# ================= LOGOUT =================
def sale_logout(request):
    logout(request)
    return redirect("/login/")


# ================= DASHBOARD =================
@login_required(login_url="/login/")
def sale_dashboard(request):
    if request.user.is_superuser:
        check_and_notify_6_months()

        return redirect("/admin/")
    check_and_notify_6_months()


    qs = Customer.objects.all().distinct()
    f = request.GET

    # ===== FILTER =====
    if f.get("province"):
        qs = qs.filter(province=f["province"])

    if f.get("company"):
        qs = qs.filter(company__icontains=f["company"])

    if f.get("xsell") in ["0", "1"]:
        qs = qs.filter(xsell_shb=bool(int(f["xsell"])) )

    if f.get("bad_debt") in ["0", "1"]:
        qs = qs.filter(bad_debt=bool(int(f["bad_debt"])) )

    if f.get("bad_from"):
        qs = qs.filter(bad_debt_year__gte=int(f["bad_from"]))

    if f.get("bad_to"):
        qs = qs.filter(bad_debt_year__lte=int(f["bad_to"]))

    if f.get("late") in ["0", "1"]:
        qs = qs.filter(late_payment=bool(int(f["late"])) )

    if f.get("late_from"):
        qs = qs.filter(late_payment_year__gte=int(f["late_from"]))

    if f.get("late_to"):
        qs = qs.filter(late_payment_year__lte=int(f["late_to"]))

    # ===== GIẢI NGÂN =====
    if f.get("dis_from"):
        qs = qs.filter(disbursement_date__gte=f["dis_from"])

    if f.get("dis_to"):
        qs = qs.filter(disbursement_date__lte=f["dis_to"])

    # ===== NGÀY NHẬP =====
    if f.get("created_from"):
        qs = qs.filter(created_at__gte=f["created_from"])

    if f.get("created_to"):
        qs = qs.filter(created_at__lte=f["created_to"])

    # ===== SORT =====
    ALLOW_ORDER = [
        "name",
        "phone",
        "cccd",
        "date_of_birth",
        "xsell_shb",
        "disbursement_date",
        "bad_debt_year",
        "late_payment_year",
        "province",
        "company",
        "created_at",
    ]

    order = f.get("order")
    if order and order.lstrip("-") in ALLOW_ORDER:
        qs = qs.order_by(order)

    # ===== LOGIC MÀU + TELE SAFE =====
    today = date.today()
    customers = list(qs)

    for c in customers:
        c.disbursement_months = (
            (today - c.disbursement_date).days // 30
            if c.disbursement_date else None
        )
        c.bad_diff = (
            today.year - c.bad_debt_year
            if c.bad_debt and c.bad_debt_year else None
        )
        c.late_diff = (
            today.year - c.late_payment_year
            if c.late_payment and c.late_payment_year else None
        )

    # ===== EXPORT =====
    if "export" in f:
        return export_customers_excel(customers)

    provinces = Customer.objects.values_list("province", flat=True).distinct()
    years = range(today.year, today.year - 15, -1)

    return render(
        request,
        "sale/dashboard.html",
        {
            "customers": customers,
            "provinces": provinces,
            "years": years,
            "request": request,
        },
    )


# ================= SAVE NOTE =================
@login_required(login_url="/login/")
@require_POST
def save_note(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    # ❗ chỉ cho sale được gán mới sửa
    if request.user not in customer.sales.all():
        return redirect("/dashboard/")

    customer.note = request.POST.get("note", "")
    customer.save()
    return redirect("/dashboard/")
