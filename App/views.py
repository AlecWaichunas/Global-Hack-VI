from django.shortcuts import render

APP_NAME = "NULL"

# Create your views here.
def index_view(request):
    context = { #context sends data to the html file
        'app_name': APP_NAME,
    }
    return render(request, 'index.html', context)
    