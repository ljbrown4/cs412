from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
# Create your views here.

dailyspecial = []


def main(request):
    """ respond to url, delegate work to template"""

    template_name = "restaurant/main.html"

    #dict of ctxt vars
    return render(request, template_name)

def order(request):
    """ respond to url, delegate work to template"""

    template_name = "restaurant/order.html"
    #dict of ctxt vars
    context = {
        'dailyspecial': random.choice(dailyspecial),
    }

    return render(request, template_name, context)

def confirmation(request):
    """ respond to url, delegate work to template"""

    template_name = "restaurant/confirmation.html"

    #dict of ctxt vars
    context = {
        'readytime': random.randint(30,60),
    }
    return render(request, template_name, context)
