from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mileage_tracker.models import Vehicle
from mileage_tracker.serializers import VehicleSerializer

# Create your views here.
@csrf_exempt
def vehicle_list(request):
    """
    List all vehicles in table or create new vehicle
    """
    if request.method == "GET":
        vehicle = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicle, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def vehicle_details(request, pk):
    """
    Get, Update or Delete a `Vehicle`
    """

    try:
        vehicle = Vehicle.objects.get(pk=pk)
    except Vehicle.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = VehicleSerializer(vehicle)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = VehicleSerializer(vehicle, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        vehicle.delete()
        return HttpResponse(status=204)
