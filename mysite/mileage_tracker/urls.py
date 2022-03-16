from django.urls import URLPattern, path
from mileage_tracker import views

urlpatterns = [
    path("vehicle/", views.vehicle_list),
    path("vehicle/<int:pk>/", views.vehicle_details),
]
