from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class RoomService(models.Model):
    has_room_service = models.BooleanField()
    max_room = models.IntegerField()
    filled_rooms = models.IntegerField()
    
class FoodService(models.Model):
    has_food_service = models.BooleanField()
    foodLevel = models.PositiveIntegerField() #Out of 3 In need, good amount, over capacity

class HousingService(models.Model):
    has_house_service = models.BooleanField()
    
class PhysicalHealthService(models.Model):
    has_physical_health_service = models.BooleanField()
    #service list: illnesses, injuries, physical abuse?
    
class MentalHealthService(models.Model):
    has_mental_health_service = models.BooleanField()
    #service list: mental illnesses?
    
class VeteranAid(models.Model):
    has_veteran_aid = models.BooleanField()
    #service list: veterans aid services?

class Shelter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userid = models.IntegerField()
    
    shelter_name = models.CharField(max_length=500)
    shelter_support_email = models.CharField(max_length=200)
    shelter_support_tele = models.CharField(max_length=15)
    shelter_address = models.CharField(max_length=200)
    shelter_city = models.CharField(max_length=200)
    shelter_state = models.CharField(max_length=2)
    shelter_desc = models.CharField(max_length=5000)
    shelter_restrictions = models.CharField(max_length=2000)
    
    service_rooms = models.OneToOneField(RoomService)
    service_foods = models.OneToOneField(FoodService)
    service_house = models.OneToOneField(HousingService)
    service_physical_illness = models.OneToOneField(PhysicalHealthService)
    service_mental_illness = models.OneToOneField(MentalHealthService)
    service_veteran_aid = models.OneToOneField(VeteranAid)
    
    def __str__(self):
        return self.shelter_name
