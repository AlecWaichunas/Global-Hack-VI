from django.contrib import admin
from .models import RoomService, FoodService, HousingService, Shelter

# Register your models here.
admin.site.register(RoomService)
admin.site.register(FoodService)
admin.site.register(HousingService)
admin.site.register(Shelter)
