from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
# Create your views here.

quotes = ["It is our choices, Harry, that show what we truly are, far more than our abilities,",
          "It matters not what someone is born, but what they grow to be!",
          "It is my belief... that the truth is generally preferable to lies." ]

images = ['https://static.independent.co.uk/s3fs-public/thumbnails/image/2014/07/24/17/Albus-Dumbledore.jpg',
          'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4UTqWXbMXK01JULIJMJzy527DWJX8G0gi6w&s',
          'https://hp-intothefire.wikidot.com/local--files/dumbledore-albus/Dumbledore.jpg']

def home_page(request):
    """ respond to url, delegate work to template"""

    template_name = "quotes/home.html"

    #dict of ctxt vars
    context = {
        'image': random.choice(images),
        'quote': random.choice(quotes),
    }
    return render(request, template_name, context)