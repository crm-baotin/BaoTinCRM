from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # ROOT /
    path("", lambda request: redirect("/login/"), name="root"),

    # ADMIN
    path("admin/", admin.site.urls),

    # CRM APP
    path("", include("crm.urls")),
]
