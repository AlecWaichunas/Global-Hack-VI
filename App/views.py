from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from App.models import *
from App.forms import *

APP_NAME = "APP NAME"

# Create your views here.
def index_view(request):
    context = { #context sends data to the html file
        'app_name': APP_NAME,
       # 'user': User,
        'shelters': Shelter.objects.all(),
    }
    return render(request, 'index.html', context)
    
def shelter_view(request, shelter_id):
    shelter = get_object_or_404(Shelter, pk=shelter_id)
    context = {
        'app_name': APP_NAME,
        'shelter': shelter,
    }
    
    return render(request, 'shelter.html', context)
    
def register_view(request):

    context = {
        'app_name': APP_NAME,
        'form': RegisterForm()
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            new_user = User.objects.create_user(form.cleaned_data['shelter_name'], form.cleaned_data['shelter_email'],
                                            form.cleaned_data['shelter_password'])
            food_service = FoodService(has_food_service=form.cleaned_data['shelter_foods'], foodLevel=0)
            rooms_service = RoomService(has_room_service=form.cleaned_data['shelter_rooms'], max_room=0, filled_rooms=0)
            house_service = HousingService(has_house_service=form.cleaned_data['shelter_housing'])
            food_service.save()
            rooms_service.save()
            house_service.save()
            shelter = Shelter(
                user = new_user,
                shelter_support_email=form.cleaned_data['shelter_support_email'],
                shelter_support_tele=form.cleaned_data['shelter_support_telephone'],
                shelter_city=form.cleaned_data['shelter_city'],
                shelter_address=form.cleaned_data['shelter_address'],
                shelter_state=form.cleaned_data['shelter_state'],
                shelter_desc=form.cleaned_data['shelter_desc'],
                service_foods=food_service,
                service_rooms=rooms_service,
                service_house=house_service
                )
            shelter.save()
            #log them in
            user = authenticate(username=form.cleaned_data['shelter_name'], password=form.cleaned_data['shelter_password'])
            if user is not None:
                login(request, user)
            #redirect to their homepage
            return render(request, 'index.html', context)

    
    return render(request, 'register.html', context)

def intake_view(request):
    context = { #context sends data to the html file
        'app_name': APP_NAME,
    }
    return render(request, 'intakeform.html', context)
    