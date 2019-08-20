from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from my_api.models import Citizen
from my_api.serializers import CitizenSerializer#, CitizenPatchSerializer
from my_api.auxiliary_funcs import is_import_json_valid, generate_import_id, get_import_id
import MySQLdb
'''
def partition(import_id):
    db = MySQLdb.connect(host="localhost", user="psa_user", passwd="123", db="psa")
    cursor = db.cursor()
    cursor.execute("""
        PARTITION BY HASH(import_id)
        PARTITIONS %s;
    """, (import_id,))
    db.commit()
    db.close()
'''

@csrf_exempt
def imports(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        if not is_import_json_valid(data):
            return HttpResponse(status=400)
        serializer = CitizenSerializer(data=data['citizens'], many=True)
        generate_import_id()
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "data": {
                    "import_id": get_import_id()
                }
            }, status=201)    
        print('ERRORS', serializer.errors, 'ERRORS')#############################################
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
            print(serializer)
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