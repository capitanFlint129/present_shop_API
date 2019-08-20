from rest_framework import serializers
from my_api.models import Citizen
from rest_framework_recursive.fields import RecursiveField
from my_api.auxiliary_funcs import get_import_id
import json

def has_digit_or_alpha(value):
    if not any([(str.isalpha(i) or str.isdigit(i)) for i in value]):
        raise serializers.ValidationError()

class CitizenSerializer(serializers.Serializer):
    citizen_id = serializers.IntegerField(max_value=2147483647, min_value=0)
    town = serializers.CharField(max_length=255, validators=[has_digit_or_alpha])#validator (has alpha or digit)
    street = serializers.CharField(max_length=255, validators=[has_digit_or_alpha])#validator (has alpha or digit)
    building = serializers.CharField(max_length=255, validators=[has_digit_or_alpha])#validator (has alpha or digit)
    apartment = serializers.IntegerField(max_value=2147483647, min_value=0)
    name = serializers.CharField(max_length=255)
    birth_date = serializers.DateField(input_formats=['%d.%m.%Y'])
    gender = serializers.ChoiceField(choices=['male', 'female'])
    relatives = serializers.ListField(child=serializers.IntegerField(min_value=0))

    def to_representation(self, citizen):
        return {
            "citizen_id": citizen.citizen_id,
            "town": citizen.town,
            "street": citizen.street,
            "building": citizen.building,
            "apartment": citizen.apartment,
            "name": citizen.name,
            "birth_date": citizen.birth_date,
            "gender": citizen.gender,
            "relatives": citizen.get_relatives(),
        }


    def validate(self, attrs):
        #print('^^^^^^^^^', attrs.keys())
        #print('!!!!!!!!!', self.initial_data)
        #print('@@@@@@@@@', self.fields.keys())
        unknown =  set(attrs.keys()) - set(self.fields.keys())
        #print('$$$$$$$$$', unknown)
        if unknown:
            raise serializers.ValidationError("Unknown field(s): {}".format(", ".join(unknown)))
        return attrs

    def create(self, validated_data):        
        citizen = Citizen.objects.create(
            import_id = get_import_id(),
            citizen_id = validated_data['citizen_id'],
            town = validated_data['town'],
            street = validated_data['street'],
            building = validated_data['building'],
            apartment = validated_data['apartment'],
            name = validated_data['name'],
            birth_date = validated_data['birth_date'],
            gender = validated_data['gender'],
            relatives=json.dumps(validated_data['relatives'])
            )
        return citizen        
    
    def update(self, instance, validated_data):
        instance.citizen_id = validated_data.get('citizen_id', instance.citizen_id)
        instance.town = validated_data.get('town', instance.town)
        instance.street = validated_data.get('street', instance.street)
        instance.building = validated_data.get('building', instance.building)
        instance.apartment = validated_data.get('apartment', instance.apartment)
        instance.name = validated_data.get('name', instance.name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.gender = validated_data.get('gender', instance.gender)

        current_relatives = set(instance.get_relatives())
        new_relatives = set(validated_data.get('relatives', instance.relatives))

        for citizen_id in (current_relatives - new_relatives):
            citizen = Citizen.objects.filter(citizen_id=citizen_id).get(import_id__exact=instance.import_id)
            print('REL', citizen.get_relatives(), 'ID', instance.citizen_id)
            new_list = citizen.get_relatives()
            new_list.remove(instance.citizen_id)
            print('NEW_LIST', new_list)
            citizen.set_relatives(new_list)
            citizen.save()
        
        for citizen_id in (new_relatives - current_relatives):
            citizen = Citizen.objects.filter(citizen_id=citizen_id).get(import_id__exact=instance.import_id)
            print('REL', citizen.get_relatives(), 'ID', instance.citizen_id)
            new_list = citizen.get_relatives()
            new_list.append(instance.citizen_id)
            print('NEW_LIST', new_list)
            citizen.set_relatives(new_list)
            citizen.save()

        instance.set_relatives(validated_data.get('relatives', instance.relatives))

        instance.save()
        print('HERE')
        return instance
'''
class CitizenPatchSerializer(serializers.Serializer):

    def __init__(self, import_id, citizen_id,*args, **kwargs):
        self.import_id = import_id
        self.citizen_id = citizen_id
        return super().__init__(*args, **kwargs)

    citizen_id = serializers.IntegerField(max_value=2147483647, min_value=0, required=False)
    town = serializers.CharField(max_length=255, validators=has_digit_or_alpha, required=False)#validator (has alpha or digit)
    street = serializers.CharField(max_length=255, validators=has_digit_or_alpha, required=False)#validator (has alpha or digit)
    building = serializers.CharField(max_length=255, validators=has_digit_or_alpha, required=False)#validator (has alpha or digit)
    apartment = serializers.IntegerField(max_value=2147483647, min_value=0, required=False)
    name = serializers.CharField(max_length=255, required=False)
    birth_date = serializers.DateField(input_formats=['%d.%m.%Y'], required=False)
    gender = serializers.ChoiceField(choices=['male', 'female'], required=False)
    relatives = serializers.ListField(child=serializers.IntegerField(min_value=0), required=False)

    def validate(self, attrs):
        unknown =  set(self.initial_data) - set(self.fields)
        if unknown:
            raise ValidationError("Unknown field(s): {}".format(", ".join(unknown)))
        return attrs
    
    def create(self, validated_data):        
        citizen = Citizen.objects.create(
            import_id=get_import_id(),
            citizen_id = validated_data['citizen_id'],
            town = validated_data['town'],
            street = validated_data['street'],
            building = validated_data['building'],
            apartment = validated_data['apartment'],
            name = validated_data['name'],
            birth_date = validated_data['birth_date'],
            gender = validated_data['gender'],
            relatives=json.dumps(validated_data['relatives'])
            )
        return citizen        
    
    def update(self, instance, validated_data):
        instance.import_id = validated_data.get('import_id', instance.import_id)
        instance.citizen_id = validated_data.get('citizen_id', instance.citizen_id)
        instance.town = validated_data.get('town', instance.town)
        instance.street = validated_data.get('street', instance.street)
        instance.building = validated_data.get('building', instance.building)
        instance.apartment = validated_data.get('apartment', instance.apartment)
        instance.name = validated_data.get('name', instance.name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.set_relatives(validated_data.get('relatives', instance.relatives))
        instance.save()
        return instance
'''