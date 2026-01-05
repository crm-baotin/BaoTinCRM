def check_and_notify_6_months():
    """
    Báo Telegram khi khách đủ 6 tháng XSELL (chỉ 1 lần)
    """
    from datetime import date
    from django.conf import settings
    from .models import Customer

    today = date.today()

    customers = Customer.objects.filter(
        xsell_shb=True,
        disbursement_date__isnull=False,
        notified_6m=False,
    )

    for c in customers:
        months = (today - c.disbursement_date).days // 30
        if months >= 6:
            # link CRM (lọc theo tên hoặc sdt)
            crm_link = (
                "https://baotincrm.onrender.com/dashboard/"
                f"?company={c.company or ''}"
            )

            msg = (
                "🔥🔥 <b>KHÁCH ĐỦ 6 THÁNG XSELL</b> 🔥🔥\n\n"
                f"👤 <b>Tên:</b> {c.name}\n"
                f"📞 <b>SĐT:</b> {c.phone or 'Ẩn'}\n"
                f"🪪 <b>CCCD:</b> {c.cccd or 'Ẩn'}\n"
                f"🏢 <b>Công ty:</b> {c.company or '-'}\n"
                f"📍 <b>Tỉnh:</b> {c.province or '-'}\n"
                f"📅 <b>Ngày giải ngân:</b> {c.disbursement_date.strftime('%d/%m/%Y')}\n"
                f"⏱ <b>Đủ:</b> {months} tháng\n\n"
                f"👉 <a href='{crm_link}'>MỞ CRM NGAY</a>"
            )

            send_telegram_message(msg)

            # đánh dấu đã gửi (1 lần duy nhất)
            c.notified_6m = True
            c.save(update_fields=["notified_6m"])
