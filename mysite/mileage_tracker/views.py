from rest_framework import generics
from mileage_tracker.models import Vehicle
from mileage_tracker.serializers import VehicleSerializer

# Create your views here.
class VehicleList(generics.ListCreateAPIView):
    """
    List all vehicles in table or create new vehicle
    """

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class Vehicle_Details(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update or Delete a `Vehicle`
    """

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def perform_update(self, serializer):
        # entry point into saving updated mileage
        super().perform_update(serializer)
        print("updating", self.get_object().mileage)
