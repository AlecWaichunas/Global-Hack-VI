"""ghack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
#Be sure to import any views!
from ghack.views import hello, current_datetime, hours_ahead, contact
from App import views

#url(regex, viewfunction) See: http://djangobook.com/views-urlconfs/
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index_view, name='index'),
    # url(r'^hello/$', hello), #https://ghack-ethanx94.c9users.io/<regex>
    url(r'^time/$', current_datetime), 
    # url(r'^contact/$', contact),
    
    # url(r'^meta/$', views.display_meta), 
    # url(r'^metaPath/$', views.current_url_request_path), 
    # url(r'^metaGET/$', views.ua_browser), 
    # url(r'^search-form/$', views.search_form),
    # url(r'^search/$', views.search),
    
    # #\d{1,2} matches one or two digits (99hr max)
    # #parentheses allow passing data in like a function
    # url(r'^time/plus/(\d{1,2})/$', hours_ahead),
]
