from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from my_api.models import Citizen
from my_api.auxiliary_funcs import get_import_id
from my_api.serializers import CitizenSerializer
import random
import datetime
import json
import time

class ImportsTests(APITestCase):
    def test_imports(self):
        url = reverse('imports')
        last_count = Citizen.objects.count()
        count = 10000
        data = generate_import(count)
        start_time = time.time()
        response = self.client.post(url, data, format='json')
        lead_time = time.time() - start_time
        self.assertTrue(lead_time < 10)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(response.content, {
            "data": {
                "import_id": get_import_id()
            }
        })
        self.assertEqual(Citizen.objects.count(), count + last_count)
    
    def test_id_imports(self):
        self.invalid_data_import_test(negative_generate, "citizen_id")
        self.invalid_data_import_test(not_unique_generate, "citizen_id")
        self.invalid_data_import_test(null_generate, "citizen_id")

    def test_town_imports(self):
        self.invalid_data_import_test(string_without_alpha_and_digit_generate, "town")
        self.invalid_data_import_test(empty_string_generate, "town")
        self.invalid_data_import_test(null_generate, "town")

    def test_building_imports(self):
        self.invalid_data_import_test(string_without_alpha_and_digit_generate, "building")
        self.invalid_data_import_test(empty_string_generate, "building")
        self.invalid_data_import_test(null_generate, "building")

    def test_street_imports(self):
        self.invalid_data_import_test(string_without_alpha_and_digit_generate, "street")
        self.invalid_data_import_test(empty_string_generate, "street")
        self.invalid_data_import_test(null_generate, "street")

    def test_apartment_imports(self):
        self.invalid_data_import_test(negative_generate, "apartment")
        self.invalid_data_import_test(null_generate, "apartment")

    def test_name_imports(self):
        self.invalid_data_import_test(empty_string_generate, "name")
        self.invalid_data_import_test(null_generate, "name")

    def test_birth_date_imports(self):
        self.invalid_data_import_test(wrong_date_format_generate, "birth_date")
        self.invalid_data_import_test(wrong_date_generate, "birth_date")        
        self.invalid_data_import_test(null_generate, "birth_date")

    def test_gender_imports(self):
        self.invalid_data_import_test(string_without_alpha_and_digit_generate, "gender")
        self.invalid_data_import_test(null_generate, "gender")

    def test_relatives_imports(self):
        self.invalid_data_import_test(invalid_relative_ties_generate, "relatives")
        self.invalid_data_import_test(unexist_relative_ties_generate, "relatives")
        self.invalid_data_import_test(null_generate, "relatives")

    def test_fields_imports(self):
        self.invalid_data_import_test(missing_field_generate, "citizen_id")
        self.invalid_data_import_test(missing_field_generate, "town")
        self.invalid_data_import_test(missing_field_generate, "street")
        self.invalid_data_import_test(missing_field_generate, "building")
        self.invalid_data_import_test(missing_field_generate, "apartment")
        self.invalid_data_import_test(missing_field_generate, "name")
        self.invalid_data_import_test(missing_field_generate, "birth_date")
        self.invalid_data_import_test(missing_field_generate, "relatives")
        self.invalid_data_import_test(missing_field_generate, "gender")
        self.invalid_data_import_test(excess_field_generate, "excess")

    def invalid_data_import_test(self, generate_invalid_data, field):
        url = reverse('imports')
        count = random.randint(0, 10000)
        data = generate_invalid_data(count - 1, field)
        last_count = Citizen.objects.count()
        response = self.client.post(url, data, format='json')

        start_time = time.time()
        lead_time = time.time() - start_time
        self.assertTrue(lead_time < 10)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Citizen.objects.count(), last_count)


class UpdateTests(APITestCase):
    def test_update_citizen(self):
        url = reverse('imports')
        last_count = Citizen.objects.count()
        count = 10000
        data = generate_import(count)
        response = self.client.post(url, data, format='json')
        
        citizen_id = random.randint(0, count - 1)
        url = reverse('update-citizen', kwargs={'citizen_id': citizen_id, "import_id": get_import_id()})
        last_data = CitizenSerializer(Citizen.objects.filter(citizen_id=citizen_id).get(import_id__exact=get_import_id())).data
        last_realtives = last_data['relatives']
        data = generate_update(citizen_id, count)
        start_time = time.time()
        response = self.client.patch(url, data, format='json')
        lead_time = time.time() - start_time
        for field in data:
            last_data[field] = data[field]
        self.assertTrue(lead_time < 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, '{"data":' + json.dumps(last_data) + '}')
        self.assertEqual(Citizen.objects.count(), count + last_count)
        for relative in last_data['relatives']:
            self.assertTrue(citizen_id in Citizen.objects.filter(citizen_id=relative).get(import_id__exact=get_import_id()).get_relatives())
        for relative in last_realtives:
            self.assertTrue(citizen_id not in Citizen.objects.filter(citizen_id=relative).get(import_id__exact=get_import_id()).get_relatives())

    
    def test_citizen_id_update(self):
        url = reverse('imports')
        last_count = Citizen.objects.count()
        count = 10000
        data = generate_import(count)
        response = self.client.post(url, data, format='json')
        
        citizen_id = random.randint(0, count - 1)
        url = reverse('update-citizen', kwargs={'citizen_id': citizen_id, "import_id": get_import_id()})
        last_data = CitizenSerializer(Citizen.objects.filter(citizen_id=citizen_id).get(import_id__exact=get_import_id())).data
        last_realtives = last_data['relatives']
        data = generate_update(citizen_id, count)
        data['citizen_id'] = citizen_id + 1
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Citizen.objects.count(), count + last_count)

    def test_relatives_imports(self):
        url = reverse('imports')
        last_count = Citizen.objects.count()
        count = 10000
        data = generate_import(count)
        response = self.client.post(url, data, format='json')
        
        citizen_id = random.randint(0, count - 1)
        url = reverse('update-citizen', kwargs={'citizen_id': citizen_id, "import_id": get_import_id()})
        last_data = CitizenSerializer(Citizen.objects.filter(citizen_id=citizen_id).get(import_id__exact=get_import_id())).data
        last_realtives = last_data['relatives']
        data = {"relatives": count + 1000}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Citizen.objects.count(), count + last_count)

    def test_no_fields_update(self):
        url = reverse('imports')
        last_count = Citizen.objects.count()
        count = 10000
        data = generate_import(count)
        response = self.client.post(url, data, format='json')
        
        citizen_id = random.randint(0, count - 1)
        url = reverse('update-citizen', kwargs={'citizen_id': citizen_id, "import_id": get_import_id()})
        last_data = CitizenSerializer(Citizen.objects.filter(citizen_id=citizen_id).get(import_id__exact=get_import_id())).data
        last_realtives = last_data['relatives']
        data = dict()
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Citizen.objects.count(), count + last_count)

    def test_excess_fields_update(self):
        url = reverse('imports')
        last_count = Citizen.objects.count()
        count = 10000
        data = generate_import(count)
        response = self.client.post(url, data, format='json')
        
        citizen_id = random.randint(0, count - 1)
        url = reverse('update-citizen', kwargs={'citizen_id': citizen_id, "import_id": get_import_id()})
        last_data = CitizenSerializer(Citizen.objects.filter(citizen_id=citizen_id).get(import_id__exact=get_import_id())).data
        last_realtives = last_data['relatives']
        data = generate_update(citizen_id, count)
        data['excess'] = 'value'
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Citizen.objects.count(), count + last_count)
    

class GetCitizensTests(APITestCase):
    def test_get_citizens(self):
        url = reverse('imports')
        last_count = Citizen.objects.count()
        count = 10000
        data = generate_import(count)
        response = self.client.post(url, data, format='json')
        url = reverse('show-all', kwargs={"import_id": get_import_id()})
        start_time = time.time()
        response = self.client.get(url)
        lead_time = time.time() - start_time
        self.assertTrue(lead_time < 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Citizen.objects.count(), count + last_count)


class BirthdaysTests(APITestCase):
    def test_percentiles(self):
        url = reverse('imports')
        last_count = Citizen.objects.count()
        count = 10000
        data = generate_import(count)
        response = self.client.post(url, data, format='json')
        
        url = reverse('birthdays', kwargs={"import_id": get_import_id()})
        start_time = time.time()
        response = self.client.get(url)
        lead_time = time.time() - start_time

        self.assertTrue(lead_time < 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Citizen.objects.count(), count + last_count)

class PercentilesTests(APITestCase):
    def test_percentiles(self):
        url = reverse('imports')
        last_count = Citizen.objects.count()
        count = 10000
        data = generate_import(count)
        response = self.client.post(url, data, format='json')
        
        url = reverse('percentiles', kwargs={"import_id": get_import_id()})
        start_time = time.time()
        response = self.client.get(url)
        lead_time = time.time() - start_time

        self.assertTrue(lead_time < 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Citizen.objects.count(), count + last_count)

def generate_update(citizen_id, count, dont_change=[]):
    date = str(random.randint(10, 28)) + '.' + str(random.randint(10, 12)) + '.' + str(random.randint(1900, datetime.datetime.utcnow().year + 1))
    rel = []
    for i in range(3):
        relative = random.randint(0, count - 1)
        if relative not in rel and relative != citizen_id:
            rel.append(relative)
    upd = {
            "town": str(random.randint(1, 100)),
            "street": str(random.randint(1, 1000)),
            "building": str(random.randint(1, 1000)),
            "apartment": random.randint(1, 10000),
            "name": str(random.randint(1, 1000000)),
            "birth_date": date,
            "gender": random.choice(["male", "female"]),
            "relatives": rel
        }
    for field in upd:
        if field in dont_change: upd.pop(field)
    return upd

def not_unique_generate(count, field):
    imp = generate_import(count)
    imp['citizens'][0][field] = random.randint(1, count - 1)
    return imp

def negative_generate(count, field):
    imp = generate_import(count)
    imp['citizens'][0][field] = random.randint(-1000000000,-1)
    return imp

def null_generate(count, field):
    imp = generate_import(count)
    imp['citizens'][0][field] = None
    return imp

def string_without_alpha_and_digit_generate(count, field):
    imp = generate_import(count)
    invalid_value = "".join(random.sample("!@#$%^&*()_-+=[];:,.?/~", random.randint(1,10)))
    imp['citizens'][0][field] = invalid_value
    return imp

def empty_string_generate(count, field):
    imp = generate_import(count)
    imp['citizens'][0][field] = ""
    return imp

def wrong_date_generate(count, field):
    imp = generate_import(count)
    imp['citizens'][0][field] = "30.02.1986"
    return imp

def wrong_date_format_generate(count, field):
    imp = generate_import(count)
    imp['citizens'][0][field] = "26/12/1986"
    return imp

def invalid_relative_ties_generate(count, field):
    imp = generate_import(count)
    for citizen in imp['citizens']:
        if citizen[field]:
            citizen[field] = []
            break
    return imp

def unexist_relative_ties_generate(count, field):
    imp = generate_import(count)
    imp['citizens'][0][field].append(random.randint(count + 1, count + 1000))
    return imp

def missing_field_generate(count, field):
    imp = generate_import(count)
    imp['citizens'][0].pop(field)
    return imp

def excess_field_generate(count, field):
    imp = generate_import(count)
    imp['citizens'][0][field] = "value"
    return imp

def generate_import(count):
    imp = {"citizens": []}
    date = str(random.randint(10, 28)) + '.' + str(random.randint(10, 12)) + '.' + str(random.randint(1900, datetime.datetime.utcnow().year + 1))
    relatives = dict()
    relatives[0] = set()
    for i in range(1000):
        citizen = 0
        relative = i + 1
        relatives[citizen].add(relative)
        relatives[relative] = {0}

    '''for i in range(random.randint(0, 1000)):
        citizen = random.randint(0, count - 1)
        relative = random.randint(0, count - 1)
        if citizen == relative: continue
        if citizen in relatives: relatives[citizen].add(relative)
        else: relatives[citizen] = {relative}
        if relative in relatives: relatives[relative].add(citizen)
        else: relatives[relative] = {citizen}'''
    for i in range(count):
        rel = []
        if i in relatives:
            rel = list(relatives[i])
        imp["citizens"].append({
            "citizen_id": i,
            "town": str(random.randint(1, 100)),
            "street": str(random.randint(1, 1000)),
            "building": str(random.randint(1, 1000)),
            "apartment": random.randint(1, 10000),
            "name": str(random.randint(1, 1000000)),
            "birth_date": date,
            "gender": random.choice(["male", "female"]),
            "relatives": rel
        })
    with open("generated_import.txt", "w") as out:
        out.write(str(imp))
    return imp
