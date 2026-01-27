from django.urls import path
from . import views

urlpatterns = [
    path("check/", views.HealthCheckView.as_view(), name="health-check"),
    path("live/", views.LivenessProbeView.as_view(), name="liveness-probe"),
    path("ready/", views.ReadinessProbeView.as_view(), name="readiness-probe"),
]
