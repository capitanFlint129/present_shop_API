from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from my_api.models import Citizen
from my_api.serializers import CitizenSerializer#, CitizenPatchSerializer
from my_api.auxiliary_funcs import is_import_json_valid, generate_import_id, get_import_id, add_present, add_age
import numpy
import json

@csrf_exempt
def imports(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        if not is_import_json_valid(data):
            return HttpResponse(status=400)
        serializer = CitizenSerializer(data=data['citizens'], many=True)
        generate_import_id()
        ###print("!!!!!!!!!!" , serializer)excess here
        if serializer.is_valid():#ne peredayotsa v validate
            print('DATA', serializer)
            serializer.save()
            return JsonResponse({
                "data": {
                    "import_id": get_import_id()
                }
            }, status=201)    
        #print('ERRORS', serializer.errors, 'ERRORS')#############################################
        return HttpResponse(status=400)######
    else: return HttpResponse(status=405)

@csrf_exempt
def update_citizen(request, import_id, citizen_id):
    if request.method == "PATCH":
        data = JSONParser().parse(request)
        citizen = Citizen.objects.filter(citizen_id=citizen_id).get(import_id__exact=import_id)
        if not data or 'citizen_id' in data:
            return HttpResponse(status=400)######
        serializer = CitizenSerializer(citizen, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            #print(serializer)
            return JsonResponse({
                "data": serializer.data
            }, status=200)
    else: return HttpResponse(status=405)

@csrf_exempt
def show_citizens(request, import_id):
    if request.method == "GET":
        citizens = Citizen.objects.filter(import_id=import_id)
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
        for citizen in Citizen.objects.filter(import_id=import_id):
            for relative in citizen.get_relatives():
                add_present(months[str(citizen.birth_date.month)], relative)
        return JsonResponse({
            "data": months
        }, status=200)
    else: return HttpResponse(status=405)

@csrf_exempt
def percentile(request, import_id):
    if request.method == "GET":
        cities = dict()
        for citizen in Citizen.objects.filter(import_id=import_id):
            add_age(cities, citizen.town, citizen.birth_date)
        data = []
        for city in cities:
            percentiles = numpy.percentile(cities[city], [50, 75, 99], interpolation='linear')
            data.append({
                "town": city, 
                "p50": float('{0:.2f}'.format(percentiles[0])), 
                "p75": float('{0:.2f}'.format(percentiles[1])), 
                "p99": float('{0:.2f}'.format(percentiles[2]))
                })
        #encoder = json.JSONEncoder()
        #encoder.FLOAT_REPR = lambda o: format(o, '.2f')
        #, encoder=encoder
        return JsonResponse({
            "data": data
        }, status=200)
    else: return HttpResponse(status=405)