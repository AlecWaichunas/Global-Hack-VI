from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from App.models import *
from App.forms import *

from django.core.exceptions import ObjectDoesNotExist

APP_NAME = "SUPER HAPPY AMAZING FUN TIME CODING"
USER_ID_NAME = 10000000

# Create your views here.
def index_view(request):
    user = request.user
    
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
    
    context = { #context sends data to the html file
        'app_name': APP_NAME,
        'user': user,
        'shelters': Shelter.objects.all()
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
            userIDName = USER_ID_NAME
            try:
                userIDName = userIDName + User.objects.all().latest('id').id + 1
            except ObjectDoesNotExist:
                userIDName = USER_ID_NAME
                
            new_user = User.objects.create_user(
                                            username=userIDName, 
                                            email=post.get('email', ''),
                                            password=post.get('password', ''))
            food_service = FoodService(has_food_service=post.get('shelter_foods',''), foodLevel=0)
            rooms_service = RoomService(has_room_service=post.get('room',''), max_room=0, filled_rooms=0)
            house_service = HousingService(has_house_service=post.get('housing',''))
            physical_service = PhysicalHealthService(has_physical_health_service=post.get('physical_health',''))
            mental_service = MentalHealthService(has_mental_health_service=post.get('mental_health',''))
            veteran_service = VeteranAid(has_veteran_aid=post.get('veteran_aid', ''))
            
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
                shelter_name=post.get('shelter_name', ''),
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
            return render(request, 'index.html', context)

    
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
        shelter.shelter_city = city
        shelter.shleter_state = state
        shelter.service_rooms.has_room_service = room
        if room:
            shelter.service_rooms.filled_rooms = post.get('rooms_filled', '')
            shelter.service_rooms.max_room = post.get('max_rooms', '')
        shelter.service_house.has_house_service = housing
        shelter.service_physical_illness.has_physical_health_service = physical_health
        shelter.service_mental_illness.has_mental_health_service = mental_health
        shelter.service_veteran_aid.has_veteran_aid = veteran
        
        shelter.service_rooms.save()
        shelter.service_physical_illness.save()
        shelter.service_mental_illness.save()
        shelter.service_veteran_aid.save()
        shelter.save()
        return redirect('shelter', shelter.id)
        
    
    return render(request, 'edit_shelter.html', context)
    
def logout_user(request):
    logout(request)
    return index_view(request)
    


def intake_view(request):
    context = { #context sends data to the html file
        'app_name': APP_NAME,
        'user': request.user,
    }
    '''
    errors = [] #Do Validation eventually
    
    if request.method == 'GET':
        enrollment_date = request.GET['enrollment_date']
        bed_date = request.GET['bed_date']
        
        firstName = request.GET['firstName']
        middleName = request.GET['middleName']
        lastName = request.GET['lastName']
        suffixName = request.GET['suffixName']
        birth_date = request.GET['birth_date']
        
        clientFacility = request.GET['clientFacility']
        clientRoom = request.GET['clientRoom']
        clientBed = request.GET['clientBed']

        ssn = request.GET['ssn']
        #gender = request.GET['gender']
        
        age = request.GET['age']
        phoneNum = request.GET['phoneNum']
        email = request.GET['email']
        #race = request.GET['race']
        
        #condition = request.GET['condition']
        #vetStatus = request.GET['vetStatus']
        #prior = request.GET['prior']
        #stayLength = request.GET['stayLength']
        
        #houseStat = request.GET['houseStat']
        zip = request.GET['zip']
        #zipStatus = request.GET['zipStatus']
        
        city2 = request.GET['city2']
        #state = request.GET['state']
        
        #income = request.GET['income']
    '''
    
    
    
    return render(request, 'intakeform.html', context)


'''
    errors = []
    if 'q' in request.GET:
        q = request.GET['q'] #ensures non-empty
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else: #add in each
            books = Book.objects.filter(title__icontains=q) #Case-insensitive
            return render(request, 'search_results.html', {'books': books, 'query': q})
    return render(request, 'search_form.html', {'errors': errors})
'''