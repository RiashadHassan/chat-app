from django.urls import path

from ..views.health import ConcurrencyAPIView, HealthCheckAPIView, GunicornHealthCheckAPIView

urlpatterns = [
    path("django/", HealthCheckAPIView.as_view(), name="health-check"),
    path("gunicorn/", GunicornHealthCheckAPIView.as_view(), name="gunicorn-check"),
    path("concurrency/", ConcurrencyAPIView.as_view(), name="concurrency-count")
]