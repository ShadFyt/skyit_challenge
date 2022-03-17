from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from mileage_tracker.models import Vehicle, MileageAndDate
from mileage_tracker.serializers import VehicleSerializer, MileageAndDateSerializer

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
        # entry point into saving updated mileage
        # gets current vehicle the view is displaying
        vehicle: Vehicle = self.get_object()
        # gets `MileageAndDate`` entry by `date_created``
        entry: MileageAndDate = MileageAndDate.objects.filter(
            vehicle__unit=vehicle.unit
        ).filter(date_created=date.today())
        # checks if `MileageAndDate` entry exits
        if entry:
            # If entry for that date already exits then update the `mil` for that entry
            entry[0].mil = vehicle.mileage
            entry[0].save()
            print("entry", entry[0].mil, vehicle.mileage)

        else:
            # if `MileageAndDate` entry does not exits then create a new instance of `MileageAndDate`
            mileage_date = MileageAndDate(
                mil=vehicle.mileage, vehicle=vehicle, date_created=(date.today())
            )
            mileage_date.save()
            print("mileage_date", mileage_date)
        super().perform_update(serializer)

        print("done updating")


class VehicleMileageDetail(generics.ListAPIView):
    queryset = MileageAndDate.objects.all()
    serializer_class = MileageAndDateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("date_created", "vehicle__unit")

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        print(queryset)
        return queryset


class MileageAndDateList(generics.ListAPIView):
    """
    Get a list of `MileageAndDate`
    """

    queryset = MileageAndDate.objects.all()
    serializer_class = MileageAndDateSerializer

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        queryset = self.get_queryset()
        serializer = MileageAndDateSerializer(queryset, many=True)
        # update `MileageAndDate.diff`
        if queryset:
            for m in queryset:
                m.diff = m.vehicle.mileage - m.mil
                m.save()
        return Response(serializer.data)
