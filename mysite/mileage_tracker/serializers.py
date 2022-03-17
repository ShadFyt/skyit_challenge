from cgitb import lookup
from rest_framework import serializers
from mileage_tracker.models import Vehicle, MileageAndDate


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["unit", "created", "mileage", "manufacturer", "status"]


class MileageAndDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MileageAndDate
        lookup_field = "date_created"

        fields = ["id", "mil", "date_created", "vehicle", "diff"]
