from django.urls import path

from clothes_shop import views

app_name = "clothes_shop"

urlpatterns = [
    path("api/clothes/", views.clothes_list, name="list"),
    path("api/clothes/<int:pk>/", views.clothes_detail, name="detail"),
]
