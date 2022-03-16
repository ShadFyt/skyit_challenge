from rest_framework import serializers
from mileage_tracker.models import Vehicle, MileageAndDate


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["unit", "mileage", "manufacturer", "status"]


class MileageAndDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MileageAndDate
        fields = ["id", "mil", "date_created"]
