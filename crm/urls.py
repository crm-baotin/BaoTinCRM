from django.urls import path
from .views import sale_login, sale_logout, sale_dashboard, save_note

urlpatterns = [
    path("login/", sale_login, name="sale_login"),
    path("logout/", sale_logout, name="sale_logout"),
    path("dashboard/", sale_dashboard, name="sale_dashboard"),
    path("note/<int:pk>/", save_note, name="save_note"),
]
