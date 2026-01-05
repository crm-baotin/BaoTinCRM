from django.contrib import admin, messages
from django.utils.html import format_html
from django.contrib.auth.models import User
from django import forms
from django.template.response import TemplateResponse
from datetime import date
from import_export.admin import ImportExportModelAdmin
from .models import Customer


# ==================================================
# FORM CHỌN SALE
# ==================================================
class AssignSaleForm(forms.Form):
    sales = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_superuser=False, is_active=True),
        widget=forms.CheckboxSelectMultiple,
        label="Chọn sale"
    )


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):

    # ================= HIỂN THỊ =================
    list_display = (
        "name",
        "date_of_birth",
        "phone",
        "cccd",
        "xsell_display",
        "disbursement_display",
        "bad_debt_display",
        "late_payment_display",
        "province",
        "company",
        "created_at",
    )

    # ================= LỌC =================
    list_filter = (
        "province",
        "company",
        "xsell_shb",
        "bad_debt",
        "bad_debt_year",
        "late_payment",
        "late_payment_year",
        "date_of_birth",
        "disbursement_date",
        "sales",
        "created_at",
    )

    # ================= TÌM KIẾM =================
    search_fields = ("name", "phone", "cccd", "company")

    filter_horizontal = ("sales",)

    # ================= ACTION =================
    actions = ["assign_sales_bulk", "remove_sales_bulk"]

    # ==================================================
    # 🔐 PHÂN QUYỀN
    # ==================================================
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sales=request.user)

    # ==================================================
    # ACTION: GÁN SALE
    # ==================================================
    def assign_sales_bulk(self, request, queryset):
        return self._sale_bulk_handler(
            request, queryset, mode="add", title="GÁN SALE CHO KHÁCH ĐÃ CHỌN"
        )
    assign_sales_bulk.short_description = "Gán sale cho khách đã chọn (hàng loạt)"

    # ==================================================
    # ACTION: BỎ GÁN SALE
    # ==================================================
    def remove_sales_bulk(self, request, queryset):
        return self._sale_bulk_handler(
            request, queryset, mode="remove", title="BỎ GÁN SALE KHỎI KHÁCH ĐÃ CHỌN"
        )
    remove_sales_bulk.short_description = "Bỏ gán sale khỏi khách đã chọn (hàng loạt)"

    # ==================================================
    # CORE HANDLER
    # ==================================================
    def _sale_bulk_handler(self, request, queryset, mode, title):
        if request.method == "POST" and "apply" in request.POST:
            form = AssignSaleForm(request.POST)
            if form.is_valid():
                sales = form.cleaned_data["sales"]
                count = queryset.count()

                for customer in queryset:
                    if mode == "add":
                        customer.sales.add(*sales)
                    else:
                        customer.sales.remove(*sales)

                text = "gán" if mode == "add" else "bỏ gán"
                self.message_user(
                    request,
                    f"✅ Đã {text} {sales.count()} sale cho {count} khách hàng.",
                    messages.SUCCESS
                )
                return None

        form = AssignSaleForm()
        return TemplateResponse(
            request,
            "admin/assign_sales.html",
            {
                "customers": queryset,
                "form": form,
                "title": title,
            },
        )

    # ==================================================
    # TIỆN ÍCH
    # ==================================================
    def months_since(self, d):
        if not d:
            return None
        return (date.today() - d).days // 30

    # ==================================================
    # XSELL SHB
    # ==================================================
    def xsell_display(self, obj):
        if not obj.xsell_shb:
            return "-"
        m = self.months_since(obj.disbursement_date)
        if m is None:
            color = "black"
        elif m >= 6:
            color = "orange"
        elif m >= 4:
            color = "green"
        else:
            color = "black"
        return format_html('<b style="color:{}">SHB</b>', color)

    xsell_display.short_description = "Xsell SHB"
    xsell_display.admin_order_field = "xsell_shb"

    # ==================================================
    # NGÀY GIẢI NGÂN
    # ==================================================
    def disbursement_display(self, obj):
        if not obj.disbursement_date:
            return "-"
        m = self.months_since(obj.disbursement_date)
        if m >= 6:
            color = "orange"
        elif m >= 4:
            color = "green"
        else:
            color = "black"
        return format_html(
            '<b style="color:{}">{}</b>',
            color,
            obj.disbursement_date.strftime("%d/%m/%Y")
        )

    disbursement_display.short_description = "Ngày giải ngân"
    disbursement_display.admin_order_field = "disbursement_date"

    # ==================================================
    # NỢ XẤU
    # ==================================================
    def bad_debt_display(self, obj):
        if not obj.bad_debt:
            return format_html('<span style="color:green">Không</span>')
        diff = date.today().year - (obj.bad_debt_year or date.today().year)
        if diff >= 5:
            color = "green"
        elif diff >= 3:
            color = "orange"
        else:
            color = "red"
        return format_html('<b style="color:{}">Có ({})</b>', color, obj.bad_debt_year or "?")

    bad_debt_display.short_description = "Nợ xấu"
    bad_debt_display.admin_order_field = "bad_debt_year"

    # ==================================================
    # TRẢ CHẬM
    # ==================================================
    def late_payment_display(self, obj):
        if not obj.late_payment:
            return format_html('<span style="color:green">Không</span>')
        diff = date.today().year - (obj.late_payment_year or date.today().year)
        if diff >= 5:
            color = "green"
        elif diff >= 3:
            color = "orange"
        else:
            color = "red"
        return format_html('<b style="color:{}">Có ({})</b>', color, obj.late_payment_year or "?")

    late_payment_display.short_description = "Trả chậm"
    late_payment_display.admin_order_field = "late_payment_year"
