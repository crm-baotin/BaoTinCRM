from django.contrib import admin
from django.urls import path, include
from crm.views import sale_login, sale_dashboard, sale_logout

urlpatterns = [
    path("login/", sale_login),
    path("logout/", sale_logout),
    path("dashboard/", sale_dashboard),
    path("admin/", admin.site.urls),
    path("", include("crm.urls")),   # 👈 BẮT BUỘC PHẢI CÓ
]
