from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from App.models import *
from App.forms import *

from django.core.exceptions import ObjectDoesNotExist

APP_NAME = "Cloud Shelter"
USER_ID_NAME = 10000000

# Create your views here.
def index_view(request):
    user = request.user
    pos = 0
    
    if request.method == 'POST':
        username_form = request.POST.get('email', '')
        password_form = request.POST.get('password', '')
        if username_form is not None:
            print(User.objects.all())
            username_ = User.objects.filter(email=username_form)
            if len(username_) > 0: 
                password_ = password_form
                login_user = authenticate(username=(username_[0].username), password=password_)

                if login_user is not None:
                    login(request, login_user)
                    user = login_user
        else:
            logout(request)
            
    shelters = Shelter.objects.all()
    param = request.GET.get('sort')
    if param is not None:
        if param == 'shelter':
            shelters = shelters.order_by('shelter_name')
        elif param == 'shelter1':
            pos = 1
            shelters = shelters.order_by('-shelter_name')
        elif param == 'house':
            shelters = sorted(shelters, key=lambda s : s.available_rooms())
        elif param == 'house1':
            pos = 1
            shelters = sorted(shelters, key=lambda s : s.available_rooms())
            shelters = shelters.reverse()
        elif param == 'phouse':
            shelters = shelters.order_by('service_house')
        elif param == 'phouse1':
            pos = 1
            shelters = shelters.order_by('-service_house')
        elif param == 'health':
            shelters = shelters.order_by('service_physical_illness')
        elif param == 'health1':
            pos = 1
            shelters = shelters.order_by('-service_physical_illness')
        elif param == 'mental':
            shelters = shelters.order_by('service_mental_illness')
        elif param == 'mental1':
            pos = 1
            shelters = shelters.order_by('-service_mental_illness')
        elif param == 'vet':
            shelters = shelters.order_by('service_veteran_aid')
        elif param == 'vet1':
            pos = 1
            shelters = shelters.order_by('-service_veteran_aid')
        elif param == 'food':
            shelter = shelters.order_by('service_foods')
        elif param == 'food1':
            pos = 1
            shelter = shelters.order_by('-service_foods')
        
    context = { #context sends data to the html file
        'app_name': APP_NAME,
        'user': user,
        'shelters': shelters,
        'pos': pos
    }

    return render(request, 'index.html', context)
    
def shelter_view(request, shelter_id):
    shelter = get_object_or_404(Shelter, pk=shelter_id)
    context = {
        'app_name': APP_NAME,
        'user': request.user,
        'shelter': shelter,
    }
    
    return render(request, 'shelter.html', context)
    
def register_view(request):

    context = {
        'app_name': APP_NAME,
        'user': request.user
    }

    if request.method == 'POST':
        post = request.POST
        
        if post:
            new_email = post.get('email', '')
            new_shelter_name = post.get('shelter_name', '')
            
            try:
                user = User.objects.all().get(email=new_email)
            except DoesNotExist:
                context['error']="This email is already registered"
                return render(request, 'register.html', context)
                
            try:
                shelter = Shelter.objects.all().get(shelter_name=new_shelter_name)
            except DoesNotExist:    
                context['error']="This shelter is already registered"
                return render(request, 'register.html', context)
        
            userIDName = USER_ID_NAME
            try:
                userIDName = userIDName + User.objects.all().latest('id').id + 1
            except ObjectDoesNotExist:
                userIDName = USER_ID_NAME
                
            new_user = User.objects.create_user(
                                            username=userIDName, 
                                            email=new_email,
                                            password=post.get('password', ''))
            food_service = FoodService(has_food_service=post.get('shelter_foods',''), foodLevel=0)
            rooms_service = RoomService(has_room_service=post.get('room',''), max_room=0, filled_rooms=0)
            house_service = HousingService(has_house_service=post.get('housing',''))
            physical_service = PhysicalHealthService(has_physical_health_service=post.get('physical_health',''))
            mental_service = MentalHealthService(has_mental_health_service=post.get('mental_health',''))
            veteran_service = VeteranAid(has_veteran_aid=post.get('veteran_aid', ''))
            
            if post.get('shelter_foods', ''):
                food_service.has_food_service = True
                food_service.foodLevel = post.get('food_level', '')
                
            if post.get('room', ''):
                rooms_service.max_room=post.get('max_rooms', '')
                rooms_service.filled_rooms=post.get('rooms_filled', '')
                if rooms_service.max_room == 0:
                    rooms_service.has_room_service = False
            
            food_service.save()
            rooms_service.save()
            house_service.save()
            physical_service.save()
            mental_service.save()
            house_service.save()
            veteran_service.save()
            
            shelter = Shelter(
                user = new_user,
                userid=new_user.id,
                shelter_name=new_shelter_name,
                shelter_support_email=post.get('supp_email', ''),
                shelter_support_tele=post.get('supp_tele', ''),
                shelter_city=post.get('city', ''),
                shelter_address=post.get('address', ''),
                shelter_state=post.get('state', ''),
                shelter_desc=post.get('desc', ''),
                service_foods=food_service,
                service_rooms=rooms_service,
                service_house=house_service,
                service_physical_illness=physical_service,
                service_mental_illness=mental_service,
                service_veteran_aid=veteran_service,
                )
            shelter.save()
            #log them in
            user = authenticate(username=(new_user.id + USER_ID_NAME), password=post.get('shelter_password', ''))
            if user is not None:
                login(request, user)
            #redirect to their homepage
            return redirect('index')

    
    return render(request, 'register.html', context)
    
def edit_shelter_view(request):
    user = request.user
    shelter = ""
    if user is not None:
        shelter = Shelter.objects.all().filter(userid=user.id)[0]
        
    context = {
        'app_name': APP_NAME,
        'user': request.user,
        'shelter': shelter
    }
        
    if request.method == 'POST':
        post = request.POST
        shelter_name = post.get('shelter_name', '')
        email = post.get('email', '')
        desc = post.get('desc', '')
        supp_email = post.get('supp_email', '')
        supp_tele = post.get('supp_tele', '')
        address = post.get('address', '')
        city = post.get('city', '')
        state = post.get('state', '')
        food = post.get('food', '')
        room = post.get('room', '')
        housing = post.get('housing', '')
        physical_health = post.get('physical_health', '')
        mental_health = post.get('mental_health', '')
        veteran = post.get('veteran', '')
        restrict = post.get('restrict', '')
        
        shelter.shelter_name = shelter_name
        shelter.shelter_desc = desc
        shelter.shelter_restrictions = restrict
        shelter.shelter_support_email = supp_email
        shelter.shelter_support_tele = supp_tele
        shelter.shelter_address = address
        shelter.service_foods.has_food_service = food
        
        shelter.shelter_city = city
        shelter.shleter_state = state
        shelter.service_rooms.has_room_service = room
        if room:
            shelter.service_rooms.filled_rooms = post.get('rooms_filled', '')
            shelter.service_rooms.max_room = post.get('max_rooms', '')
            if shelter.service_rooms.max_room == 0:
                shelter.service_rooms.has_room_service = False
        if food:
            print(food)
            shelter.service_foods.foodLevel = post.get('food_amount','')
        shelter.service_house.has_house_service = housing
        shelter.service_physical_illness.has_physical_health_service = physical_health
        shelter.service_mental_illness.has_mental_health_service = mental_health
        shelter.service_veteran_aid.has_veteran_aid = veteran
        
        shelter.service_foods.save()
        shelter.service_rooms.save()
        shelter.service_physical_illness.save()
        shelter.service_mental_illness.save()
        shelter.service_veteran_aid.save()
        shelter.save()
        return redirect('shelter', shelter.id)
        
    
    return render(request, 'edit_shelter.html', context)
    
def logout_user(request):
    logout(request)
    return redirect('index')
    


def intake_view(request):
    context = { #context sends data to the html file
        'app_name': APP_NAME,
        'user': request.user,
    }
    
    intake = Intake()

    
    if request.method == 'POST':
        post = request.POST
        
        intake.enrollment_date = post.get('enrollment_date', '')
        intake.bed_date = post.get('bed_date', '')
        
        intake.firstName = post.get('firstName', '')
        intake.middleName = post.get('middleName', '')
        intake.lastName = post.get('lastName', '')
        intake.suffixName = post.get('suffixName', '')
        intake.birth_date = post.get('birth_date', '')
        
        intake.clientFacility = post.get('clientFacility', '')
        intake.clientRoom = post.get('clientRoom', '')
        intake.clientBed = post.get('clientBed', '')

        intake.ssn = post.get('ssn', '')
        intake.gender = post.get('gender', '') #
        
        intake.age = post.get('age', '')
        intake.phoneNum = post.get('phoneNum', '')
        intake.email = post.get('email', '')
        intake.race = post.get('race', '') #
        
        intake.condition = post.get('condition', '') #
        intake.vetStatus = post.get('vetStatus', '') #
        intake.prior = post.get('prior', '') #
        intake.stayLength = post.get('stayLength', '') #
        
        intake.houseStat = post.get('houseStat', '') #
        intake.zip = post.get('zip', '')
        intake.zipStatus = post.get('zipStatus', '') #
        
        intake.city2 = post.get('city2', '')
        intake.state = post.get('state', '') #
        
        intake.income = post.get('income', '') #
        intake.save()    

    
    return render(request, 'intakeform.html', context)


def search_records(request):
    user = request.user
    if not user:
        redirect('index')
        
    search_fields = [
        "Name",
        "SSN",
        "Date of Birth",
        "age",
        "Phone Number",
        "Email",
        "Race",
        "Zip code",
        "City",
        "State"
    ]
    
    
    context = {
        'app_name': APP_NAME,
        'search_fields': search_fields
    }
        
    return render(request, 'search_records.html', context)

