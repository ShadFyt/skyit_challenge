from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mileage_tracker.models import Vehicle
from mileage_tracker.serializers import VehicleSerializer

# Create your views here.
@api_view(["GET", "POST"])
def vehicle_list(request):
    """
    List all vehicles in table or create new vehicle
    """
    if request.method == "GET":
        vehicle = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicle, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def vehicle_details(request, pk):
    """
    Get, Update or Delete a `Vehicle`
    """

    try:
        vehicle = Vehicle.objects.get(pk=pk)
    except Vehicle.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
