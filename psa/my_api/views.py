from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser, ParseError
from my_api.models import Citizen
from my_api.serializers import CitizenSerializer
from my_api.auxiliary_funcs import is_relative_ties_valid, generate_import_id, get_import_id, add_present, add_age
import numpy
import json

@csrf_exempt
def imports(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except ParseError:
            return HttpResponse(status=400)
        if not is_relative_ties_valid(data):
            return HttpResponse(status=400)
        try:
            serializer = CitizenSerializer(data=data['citizens'], many=True)
        except KeyError:
            return HttpResponse(status=400)
        generate_import_id()
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "data": {
                    "import_id": get_import_id()
                }
            }, status=201)    
        print('ERRORS', serializer.errors)
        return HttpResponse(status=400)
    else: 
        return HttpResponse(status=405)

@csrf_exempt
def update_citizen(request, import_id, citizen_id):
    if request.method == "PATCH":
        try:
            data = JSONParser().parse(request)
        except ParseError:
            return HttpResponse(status=400)
        try:
            citizen = Citizen.objects.filter(citizen_id=citizen_id).get(import_id__exact=import_id)
        except Citizen.DoesNotExist:
            return HttpResponse(status=404)
        try:
            if 'relatives' in data:
                for relative in data['relatives']:
                    Citizen.objects.filter(citizen_id=relative).get(import_id__exact=import_id)
        except Citizen.DoesNotExist:
            return HttpResponse(status=400) 
        if not data or 'citizen_id' in data:
            return HttpResponse(status=400)
        serializer = CitizenSerializer(citizen, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "data": serializer.data
            }, status=200)
        print('ERRORS', serializer.errors)
        return HttpResponse(status=400)        
    else: 
        return HttpResponse(status=405)

@csrf_exempt
def show_citizens(request, import_id):
    if request.method == "GET":
        try:
            citizens = Citizen.objects.filter(import_id=import_id)
        except Citizen.DoesNotExist:
            return HttpResponse(status=404)
        if not citizens:
            return HttpResponse(status=404)
        serializer = CitizenSerializer(citizens, many=True)
        return JsonResponse({
            "data": serializer.data
        }, status=200)
    else: return HttpResponse(status=405)

@csrf_exempt
def birthdays(request, import_id):
    if request.method == "GET":
        months = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], 
        "7": [], "8": [], "9": [], "10": [], "11": [], "12": []}
        try:
            citizens = Citizen.objects.filter(import_id=import_id)
            if not citizens:
                return HttpResponse(status=404)
            for citizen in citizens:
                for relative in citizen.get_relatives():
                    add_present(months[str(citizen.birth_date.month)], relative)
        except Citizen.DoesNotExist:
            return HttpResponse(status=404)
        return JsonResponse({
            "data": months
        }, status=200)
    else: return HttpResponse(status=405)

@csrf_exempt
def percentile(request, import_id):
    if request.method == "GET":
        cities = dict()
        try:
            citizens = Citizen.objects.filter(import_id=import_id)
            if not citizens:
                return HttpResponse(status=404)
            for citizen in citizens:
                add_age(cities, citizen.town, citizen.birth_date)
        except Citizen.DoesNotExist:
            return HttpResponse(status=404)
        data = []
        for city in cities:
            percentiles = numpy.percentile(cities[city], [50, 75, 99], interpolation='linear')
            data.append({
                "town": city, 
                "p50": float('{0:.2f}'.format(percentiles[0])), 
                "p75": float('{0:.2f}'.format(percentiles[1])), 
                "p99": float('{0:.2f}'.format(percentiles[2]))
                })
        return JsonResponse({
            "data": data
        }, status=200)
    else: return HttpResponse(status=405)