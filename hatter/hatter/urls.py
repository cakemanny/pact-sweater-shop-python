from django.urls import path
from django.conf import settings

from hatter import views

urlpatterns = [
    path("healthz", views.healthz),
    path("hat/order", views.order_hat),
]

if settings.PACT_VERIFICATION:
    urlpatterns += [
        path("_/pact/provider-states", views.pact_provider_states),
    ]
