from rest_framework.viewsets import ModelViewSet
from datetime import date
from rest_framework.response import Response
from django.utils.text import slugify


from django.shortcuts import render

from mileage_tracker.models import Miles, Vehicle
from mileage_tracker.serializers import MilesSerializer, VehicleSerializer


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    lookup_field = "unit"

    def perform_create(self, serializer):
        super().perform_create(serializer)
        vehicles = self.get_queryset()
        vehicle = vehicles.get(unit=serializer.data["unit"])
        print(vehicle)
        new_mile = Miles(
            mileage=serializer.data["mileage"],
            vehicle=vehicle,
            date_created=(date.today()),
        )
        if not new_mile.slug:
            new_mile.slug = slugify(f"{date.today()} {vehicle.unit}")
        new_mile.save()
        return Response(serializer.data)

    def perform_update(self, serializer):
        vehicle = self.get_object()
        print(vehicle)
        entry: Miles = Miles.objects.filter(vehicle__unit=vehicle.unit).filter(
            date_created=date.today()
        )
        if entry:
            entry[0].mileage = vehicle.mileage
            entry[0].save
        else:
            # if `Miles` entry does not exits then create a new instance of `Miles`
            miles = Miles(
                mileage=vehicle.mileage, vehicle=vehicle, date_created=(date.today())
            )
            miles.difference = vehicle.mileage - miles.mileage
            miles.save()
            print("Miles", miles)
        return super().perform_update(serializer)


class MilesViewSet(ModelViewSet):
    queryset = Miles.objects.all()
    serializer_class = MilesSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        print("retrieving item")
        mile = self.get_object()
        print(mile.get_difference)
        if mile.difference != mile.get_difference:
            mile.difference = mile.get_difference
            mile.save()
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        print("getting list of miles")
        super().list(request, *args, **kwargs)
        queryset = self.get_queryset()
        serializer = MilesSerializer(queryset, many=True, context={"request": request})
        if queryset:
            for mile in queryset:
                mile.difference = mile.vehicle.mileage - mile.mileage
                mile.save()
        return Response(serializer.data)
