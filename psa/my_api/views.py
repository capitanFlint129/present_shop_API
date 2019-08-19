from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from my_api.models import Citizen
from my_api.serializers import CitizenSerializer
from my_api.auxiliary_funcs import is_import_json_valid, generate_import_id, get_import_id
import MySQLdb

def partition(import_id):
    db = MySQLdb.connect(host="localhost", user="psa_user", passwd="123", db="psa")
    cursor = db.cursor()
    cursor.execute("""
        PARTITION BY HASH(import_id)
        PARTITIONS %s;
    """, (import_id,))
    db.commit()
    db.close()


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
            partition(get_import_id())
            return JsonResponse({
                "data": {
                    "import_id": get_import_id()
                }
            }, status=201)    
        print('ERRORS', serializer.errors, 'ERRORS')#############################################
        return HttpResponse(status=400)######
    #data['import_id'] = next(import_id_generator())
    


'''
@csrf_exempt
def imports(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        for citizen in data['citizens']:
            one_import(citizen)
            #partition(serializer.import_id)
        return JsonResponse({
            "data": {
                #"import_id": serializer.import_id
            }
        }, status=201)#####    
        

def one_import(data):
    data['import_id'] = next(import_id_generator())
    serializer = CitizenSerializer(data=data)
    if serializer.is_valid():
        print('AAA/n', serializer.validated_data, 'AAA/n')
        serializer.save()
    else:
        print('ERRORS', serializer.errors)
        return HttpResponse(status=400)######
'''