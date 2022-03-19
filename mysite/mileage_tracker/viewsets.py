from rest_framework.viewsets import ModelViewSet
from datetime import date
from rest_framework.response import Response
from django.utils.text import slugify


from django.shortcuts import render

from mileage_tracker.models import Miles, Vehicle
from mileage_tracker.serializers import MilesSerializer, VehicleSerializer


class VehicleViewSet(ModelViewSet):
    """
    This viewset automactically provides all `CRUD` actions.

    """

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    lookup_field = "unit"

    def perform_create(self, serializer):
        """Added some additionally functionality to the `create` method.  When a new `Vehicle` is created we also create a new `Miles`

        Args:
            serializer: data from end user

        Returns:
            Vehicle: if the data is valid we return the serialized data
        """
        super().perform_create(serializer)
        vehicles = self.get_queryset()
        vehicle = vehicles.get(unit=serializer.data["unit"])
        print(vehicle)
        new_mile = Miles(
            mileage=serializer.data["mileage"],
            vehicle=vehicle,
            date_created=(date.today()),
        )

        new_mile.save()
        return Response(serializer.data)

    def perform_update(self, serializer):
        """ "Added some additionally functionality to the `update` method.

        when the `Vehicle.mileage` get updated, we also want to create a new `Miles` entry if one doesn't exits for that day.

        Args:
            serializer: data to be updated that was supplied by user

        Returns:
            Vehicle: returns `Vehicle` object that was being updated
        """
        vehicle = self.get_object()
        print(vehicle)
        if entry := Miles.objects.filter(vehicle__unit=vehicle.unit).filter(
            date_created=date.today()
        ):
            entry[0].mileage = vehicle.mileage
            entry[0].save()
        else:
            # if `Miles` entry does not exits then create a new instance of `Miles`
            mile = Miles(
                mileage=vehicle.mileage, vehicle=vehicle, date_created=(date.today())
            )
            mile.difference = mile.get_difference
            mile.save()
            print("Miles", mile)
        return super().perform_update(serializer)


class MilesViewSet(ModelViewSet):
    """
    This viewset automactically provides all `CRUD` actions.

    """

    queryset = Miles.objects.all()
    serializer_class = MilesSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        """Added some additionally functionality to the `update` method.

        Checks if `Miles.difference` is up to date if not then update it

        """
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
                mile.difference = mile.get_difference
                mile.save()
        return Response(serializer.data)
