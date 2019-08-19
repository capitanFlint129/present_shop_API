from rest_framework import serializers
from my_api.models import Citizen
from rest_framework_recursive.fields import RecursiveField
from my_api.auxiliary_funcs import get_import_id
import json

class CitizenSerializer(serializers.Serializer):
    #import_id = serializers.IntegerField()
    citizen_id = serializers.IntegerField(max_value=2147483647, min_value=0)
    town = serializers.CharField(max_length=255)#validator (has alpha or digit)
    street = serializers.CharField(max_length=255)#validator (has alpha or digit)
    building = serializers.CharField(max_length=255)#validator (has alpha or digit)
    apartment = serializers.IntegerField(max_value=2147483647, min_value=0)
    name = serializers.CharField(max_length=255)
    birth_date = serializers.DateField(input_formats=['%d.%m.%Y'])
    gender = serializers.ChoiceField(choices=['male', 'female'])
    relatives = serializers.ListField(child=serializers.IntegerField(min_value=0))
    #SlugRelatedField(many=True, slug_field='citizen_id', queryset=Citizen.objects.all())
    '''
    class Meta:
        model = Citizen
        fields = '__all__'
    '''
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