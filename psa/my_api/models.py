from django.db import models
from django.db import connection
import json

class Citizen(models.Model):
    import_id = models.IntegerField(default=0)
    citizen_id = models.IntegerField() 
    town = models.CharField(max_length=255)#validate 1 digit or alpha
    street = models.CharField(max_length=255)#
    building = models.CharField(max_length=255)#
    apartment = models.IntegerField() 
    name = models.CharField(max_length=255)    
    birth_date = models.DateField()
    gender = models.CharField(max_length=255, choices=[('male', 'male'), ('female', 'female')])
    relatives = models.TextField()
    
    def set_relatives(self, relatives):
        self.relatives = json.dumps(relatives)

    def get_relatives(self):
        return json.loads(self.relatives)
    
    class Meta:
        ordering = ['citizen_id']