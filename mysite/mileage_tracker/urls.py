from rest_framework.routers import DefaultRouter
from django.urls import path, include
from mileage_tracker import views
from mileage_tracker import viewsets

# app_name = "vehicles"

router = DefaultRouter()
router.register(
    r"miles",
    viewsets.MilesViewSet,
)
router.register(r"vehicle", viewsets.VehicleViewSet)


urlpatterns = [path("", include(router.urls))]


# urlpatterns = [
#     path("vehicle/", views.VehicleList.as_view()),
#     path("vehicle/<str:pk>/", views.VehicleDetails.as_view()),
#     path(
#         "mileage/diff",
#         views.MileageDetail.as_view(),
#     ),
#     path("mileage/", views.MileageList.as_view()),
# ]
