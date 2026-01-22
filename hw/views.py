from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.

import time
import random

def home(request):
    ''' fn to respond to the "home" request'''

    response_text = f'''
    <html>
    <h1> Hello, world </h1>
    The current time is {time.ctime()}.
    </html>
    '''

    return HttpResponse(response_text)

def home_page(request):
    """ respond to url, delegate work to template"""

    template_name = "hw/home.html"
    #dict of ctxt vars
    context = {
        'time': time.ctime(),
        'letter1': chr(random.randint(65,90)),
        'letter2': chr(random.randint(65,90)),
        'num': random.randint(1,20),
    }
    return render(request, template_name, context)

def about(request):
    """ respond to url, delegate work to template"""

    template_name = "hw/about.html"
    #dict of ctxt vars
    context = {
        'time': time.ctime(),
        'letter1': chr(random.randint(65,90)),
        'letter2': chr(random.randint(65,90)),
        'num': random.randint(1,20),
    }
    return render(request, template_name, context)