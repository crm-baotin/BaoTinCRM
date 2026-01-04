from openpyxl import Workbook
from django.http import HttpResponse

def export_customers_excel(qs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Khach_hang"

    ws.append([
        "Tên","SĐT","CCCD","Tỉnh","Công ty",
        "Xsell","Nợ xấu","Nợ xấu từ năm",
        "Trả chậm","Trả chậm từ năm",
        "Ngày giải ngân","Ghi chú"
    ])

    for c in qs:
        ws.append([
            c.name,
            c.phone,
            c.cccd,
            c.province,
            c.company,
            "SHB" if c.xsell_shb else "",
            "Có" if c.bad_debt else "Không",
            c.bad_debt_year or "",
            "Có" if c.late_payment else "Không",
            c.late_payment_year or "",
            c.disbursement_date.strftime("%d/%m/%Y") if c.disbursement_date else "",
            c.note or "",
        ])

    res = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    res["Content-Disposition"] = "attachment; filename=khach_hang_sale.xlsx"
    wb.save(res)
    return res
