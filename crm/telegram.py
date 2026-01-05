import requests
from datetime import date
from django.conf import settings
from .models import Customer


# ================== CẤU HÌNH TELEGRAM ==================
BOT_TOKEN = "8213846644:AAG_Mom7MRzH97Y_-c7KQocQ0VS9qqf3mIc"
CHAT_ID = "6663298744"

TELE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_telegram(text):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        requests.post(TELE_URL, data=payload, timeout=10)
    except Exception as e:
        print("Telegram error:", e)


# ================== CHECK & NOTIFY 6 THÁNG ==================
def check_and_notify_6_months():
    """
    - Chạy bằng cron lúc 08:00 mỗi ngày
    - Khách đủ >= 6 tháng
    - xsell_shb = True
    - notified_6m = False
    """

    today = date.today()

    customers = Customer.objects.filter(
        xsell_shb=True,
        disbursement_date__isnull=False,
        notified_6m=False,
    )

    for c in customers:
        months = (today - c.disbursement_date).days // 30

        if months >= 6:
            msg = (
                "🎯 <b>KHÁCH ĐỦ ĐIỀU KIỆN XSELL 6 THÁNG</b>\n\n"
                f"👤 Tên: {c.name}\n"
                f"📞 SĐT: {c.phone or '-'}\n"
                f"🪪 CCCD: {c.cccd or '-'}\n"
                f"📅 Ngày giải ngân: {c.disbursement_date.strftime('%d/%m/%Y')}\n\n"
                f"👉 Link CRM: https://baotincrm.onrender.com/dashboard/"
            )

            send_telegram(msg)

            # ✅ ĐÁNH DẤU ĐÃ GỬI (QUAN TRỌNG)
            c.notified_6m = True
            c.save(update_fields=["notified_6m"])
