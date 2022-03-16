from django.urls import URLPattern, path
from mileage_tracker import views

urlpatterns = [
    path("vehicle/", views.VehicleList.as_view()),
    path("vehicle/<str:pk>/", views.Vehicle_Details.as_view()),
]
