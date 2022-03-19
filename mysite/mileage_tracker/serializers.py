from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
)
from mileage_tracker.models import Vehicle, Miles


class VehicleSerializer(HyperlinkedModelSerializer):
    miles = HyperlinkedRelatedField(
        view_name="miles-detail", lookup_field="slug", read_only=True, many=True
    )

    class Meta:
        model = Vehicle
        fields = [
            "url",
            "unit",
            "created",
            "mileage",
            "manufacturer",
            "status",
            "miles",
        ]

        extra_kwargs = {
            "url": {"view_name": "vehicle-detail", "lookup_field": "unit"},
        }


class MilesSerializer(HyperlinkedModelSerializer):
    vehicle = HyperlinkedRelatedField(
        view_name="vehicle-detail", read_only=True, many=False, lookup_field="unit"
    )

    class Meta:
        model = Miles

        fields = [
            "url",
            "mileage",
            "date_created",
            "difference",
            "slug",
            "vehicle",
        ]

        extra_kwargs = {
            "url": {"view_name": "miles-detail", "lookup_field": "slug"},
        }
