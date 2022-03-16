from rest_framework import serializers
from mileage_tracker.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["id", "mileage", "manufacturer", "status"]

    def update_mileage(self, instance, validated_data):
        """
        Update and return  an existing `Vehicle.mileage` instance, given the validated mileage.
        """

        instance.mileage = validated_data.get("mileage", instance.mileage)
        instance.save()
        return instance
