from django.urls import path
from mileage_tracker import views

urlpatterns = [
    path("vehicle/", views.VehicleList.as_view()),
    path("vehicle/<str:pk>/", views.VehicleDetails.as_view()),
    path(
        "mileage/diff",
        views.VehicleMileageDetail.as_view(),
    ),
    path("mileage/", views.MileageAndDateList.as_view()),
]
# mileage/diff?date_created=2022-03-18&vehicle__unit=DG42F41A
