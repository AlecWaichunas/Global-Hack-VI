# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

# Create your models here.
class RoomService(models.Model):
    has_room_service = models.BooleanField()
    max_room = models.IntegerField()
    filled_rooms = models.IntegerField()
    
    def __str__(self):
        return has_room_service
    
class FoodService(models.Model):
    has_food_service = models.BooleanField()
    foodLevel = models.PositiveIntegerField() #Out of 3 In need, good amount, over capacity
    def __str__(self):
        return self.foodLevel or 0

class HousingService(models.Model):
    has_house_service = models.BooleanField()
    
    def __str__(self):
        return self.has_house_service
    
class PhysicalHealthService(models.Model):
    has_physical_health_service = models.BooleanField()
    #service list: illnesses, injuries, physical abuse?
    def __str__(self):
        return self.has_physical_health_service
    
class MentalHealthService(models.Model):
    has_mental_health_service = models.BooleanField()
    #service list: mental illnesses?
    def __str__(self):
        return self.has_mental_health_service
    
class VeteranAid(models.Model):
    has_veteran_aid = models.BooleanField()
    #service list: veterans aid services?
    def __str__(self):
        return self.has_veteran_aid

class Shelter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userid = models.IntegerField()
    
    shelter_name = models.CharField(max_length=500)
    shelter_support_email = models.CharField(max_length=200) #See Below?
    shelter_support_tele = models.CharField(max_length=15) #See Below?
    
    #shelter_support_email = models.EmailField(max_length=70,blank=True)
    
    #See Phone Regex Above
    #shelter_support_tele = models.CharField(validators=[phone_regex], blank=True) # validators should be a list
    
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
    
    def available_rooms(self):
        if not self.service_rooms.has_room_service:
            return 0
        return (self.service_rooms.filled_rooms - self.service_rooms.max_room)
    
    def __str__(self):
        return self.shelter_name


class Intake(models.Model):

    GENERAL_CHOICES = (('0', 'No'), 
                    ('1', 'Yes'),
                    ('98', 'Don\'t Know'),
                    ('99', 'Refused'),)

    GENDER_CHOICES = (('0', 'Male'), 
                  ('1', 'Female'),
                  ('2', 'Transgender Male to Female'),
                  ('3', 'Transgender Female to Male'),
                  ('97', 'Other'),
                  ('98', 'Don\'t Know'),
                  ('99', 'Refused'),)
    
    RACE_CHOICES = (('0', 'American Indian/Alaskan Native'), 
                    ('1', 'Asian'),
                    ('2', 'Black/African American'),
                    ('3', 'Native Hawaiian or Other Pacific Islander'),
                    ('4', 'White/Caucasian'),
                    ('98', 'Don\'t Know'),
                    ('99', 'Refused'),)
    
    PRIOR_CHOICES = (('0', 'Emergency Shelter'),
				    ('1', 'Transitional Housing for Homeless Persons (including homeless youth)	'),
				    ('2', 'Permanent Housing for Formerly Homeless Persons (such as SHP, S+C, SRO Mod Rehab)'),
				    ('3', 'Psychiatric Hospital'),
				    ('4', 'Substance Abuse Treatment Center'),
				    ('5', 'Hospital'),
				    ('6', 'Prison'),
				    ('7', 'Rental by Client, No Housing Subsidy'),
				    ('8', 'Rental by Client, with VASH Housing Subsidy'),
				    ('9', 'Rental by Client, with Other (Non-Vash) Housing Subsidy'),
				    ('10', 'Owned by Client, No Housing Subsidy'),
				    ('11', 'Owned by Client, with Housing Subsidy'),
				    ('12', 'Staying or Living in a Family Member’s Room, Apartment, or House'),
				    ('13', 'Staying or Living in a Friend’s Room, Apartment, or House'),
				    ('14', 'Hotel/Motel Paid for Without Emergency Shelter Voucher'),
				    ('15', 'Foster Care Home/Foster Care Group Home'),
				    ('16', 'Places Not Meant for Habitation e.g., (Vehicles, Abandoned Building, Bus/Train/Subway Station/Airport, etc)'),
				    ('17', 'Safe Haven'),
				    ('97', 'Other (Describe)'),
				    ('98', 'Don\'t Know'),
				    ('99', 'Refused'),)
    
    LENGTH_CHOICES = (('0', 'One Week or Less'),
                    ('1', 'Less Than a Month'),
                    ('2', '1-3 Months'),
                    ('3', 'More Than 3 Months, but Less Than a Year'),
                    ('4', 'More Than a Year'),
                    ('98', 'Don\'t Know'),
                    ('99', 'Refused'),)
    
    HOUSING_CHOICES = (('0', 'Homeless'),
					    ('1', 'Housed, but at-risk of losing housing'),
						('2', 'Housed, but at imminent risk of losing housing'),
						('3', 'Stably Housed'),
					    ('98', 'Don\'t Know'),
                        ('99', 'Refused'),)
                        
    ZIP_CHOICES = (('0', 'Full Zip Reported'),
					('1', 'Partial Zip Reported'),
					('98', 'Don\'t Know'),
					('99', 'Refused'),)

    STATE_CHOICES = (('0', 'AL'),
					('1', 'AK'),
					('2', 'AZ'),
					('3', 'AR'),
					('4', 'CA'),
					('5', 'CO'),
					('6', 'CT'),
					('7', 'DE'),
					('8', 'FL'),
					('9', 'GA'),
					('10', 'HI'),
					('11', 'ID'),
					('12', 'IL'),
					('13', 'IN'),
					('14', 'IA'),
					('15', 'KS'),
					('16', 'KY'),
					('17', 'LA'),
					('18', 'ME'),
					('19', 'MD'),
					('20', 'MA'),
					('21', 'MI'),
					('22', 'MN'),
					('23', 'MS'),
					('24', 'MO'),
					('25', 'MT'),
					('26', 'NE'),
					('27', 'NV'),
					('28', 'NH'),
					('29', 'NJ'),
					('30', 'NM'),
					('31', 'NY'),
					('32', 'NC'),
					('33', 'ND'),
					('34', 'OH'),
					('35', 'OK'),
					('36', 'OR'),
					('37', 'PA'),
					('38', 'RI'),
					('39', 'SC'),
					('40', 'SD'),
					('41', 'TN'),
					('42', 'TX'),
					('43', 'UT'),
				    ('44', 'VT'),
					('45', 'VA'),
					('46', 'WA'),
					('47', 'WV'),
					('48', 'WI'),
					('49', 'WY'),
					('98', 'Don\'t Know'),
					('99', 'Refused'),)
                    
    enrollment_date = models.DateField()
    
    firstName = models.CharField(max_length=20)
    middleName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    suffixName = models.CharField(max_length=4)
    birth_date = models.DateField()
    
    bed_date = models.DateField()
    clientFacility = models.CharField(max_length=20)
    clientRoom = models.IntegerField()
    clientBed = models.IntegerField()
    
    ssn = models.IntegerField() #CONTAINS Dashes, must fix or manipulatate input box via JS
    #http://stackoverflow.com/questions/8077840/choicefield-in-django-model
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    
    age = models.IntegerField()
    phoneNum = models.CharField(validators=[phone_regex], max_length=16, blank=True) # validators should be a list
    email = models.EmailField(max_length=70,blank=True)
    race = models.CharField(max_length=2, choices=RACE_CHOICES)
    
    condition = models.CharField(max_length=2, choices=GENERAL_CHOICES)
    vetStatus = models.CharField(max_length=2, choices=GENERAL_CHOICES)
    prior = models.CharField(max_length=2, choices=PRIOR_CHOICES)
    stayLength = models.CharField(max_length=2, choices=LENGTH_CHOICES)
    
    houseStat = models.CharField(max_length=2, choices=HOUSING_CHOICES)
    zip = models.IntegerField()
    #zipStatus = models.CharField(max_length=2, choices=ZIP_CHOICES) ##
    
    city2 = models.CharField(max_length=60)
    #state = models.CharField(max_length=2, choices=STATE_CHOICES) ##
    
    income = models.CharField(max_length=2, choices=GENERAL_CHOICES)
    
    def __str__(self):
        return (self.firstName + " " + self.middleName + " " + self.lastName)
