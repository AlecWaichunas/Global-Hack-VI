from django.shortcuts import render

from django.core.mail import send_mail

from django.template.loader import get_template
from django.template import Context

from django.http import Http404, HttpResponse, HttpResponseRedirect
import datetime

# Connect View Classes to urls.py
def hello(request):
    return HttpResponse("Hello world")
    
def current_datetime(request):
    now = datetime.datetime.now()
    #html = "<html><body>It is now %s.</body></html>" % now
    '''
    t = get_template('dateapp/current_datetime.html')
    #html = t.render(Context({'current_date': now}))
    #return HttpResponse(html)
    '''
    return render(request, 'dateapp/current_datetime.html', {'current_date': now})
    
def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    '''
    html = "In %s hour(s), it will be  %s.  " % (offset, dt)
    return HttpResponse(html)
    '''
    return render(request, 'dateapp/hours_ahead.html', {'hour_offset': offset, 'next_time': dt})
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})