from django.urls import path

from hatter import views

urlpatterns = [
    path("healthz", views.healthz),
    path("hat/order", views.order_hat),
]
