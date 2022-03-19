from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from mileage_tracker.models import Vehicle, Miles
from mileage_tracker.serializers import VehicleSerializer, MilesSerializer

from datetime import date


# Create your views here.
class VehicleList(generics.ListCreateAPIView):
    """
    List all vehicles in table or create new vehicle
    """

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update or Delete a `Vehicle`
    """

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def perform_update(self, serializer):
        # entry point into saving updated Miles
        # gets current vehicle the view is displaying
        vehicle: Vehicle = self.get_object()
        # gets `Miles`` entry by `date_created``
        entry: Miles = Miles.objects.filter(vehicle__unit=vehicle.unit).filter(
            date_created=date.today()
        )
        # checks if `Miles` entry exits
        if entry:
            # If entry for that date already exits then update the `mil` for that entry
            entry[0].mil = vehicle.Miles
            entry[0].save()
            print("entry", entry[0].mil, vehicle.Miles)

        else:
            # if `Miles` entry does not exits then create a new instance of `Miles`
            Miles_date = Miles(
                mil=vehicle.Miles, vehicle=vehicle, date_created=(date.today())
            )
            Miles_date.save()
            print("Miles_date", Miles_date)
        super().perform_update(serializer)

        print("done updating")


class MilesDetail(generics.RetrieveAPIView):
    queryset = Miles.objects.all()
    serializer_class = MilesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("date_created", "vehicle__unit")

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        print(queryset)
        return queryset


class MilesList(generics.ListAPIView):
    """
    Get a list of `Miles`
    """

    queryset = Miles.objects.all()
    serializer_class = MilesSerializer

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        queryset = self.get_queryset()
        serializer = MilesSerializer(queryset, many=True)
        # update `Miles.difference`
        if queryset:
            for m in queryset:
                m.difference = m.vehicle.Miles - m.mil
                m.save()
        return Response(serializer.data)
