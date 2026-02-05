from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
import time
# Create your views here.

dailyspecial = ["Lasagna Pizza 16in ($20)", "Chicken Parmigiana Pizza 16in ($22)", "Pepperoni Calzone ($12)", "Mozarella Calzone ($12)", "Cheese Steak Stromboli ($14)", "Buffalo Chicken Pizza 16in ($22)"]
dailyprices = {"Lasagna Pizza 16in ($20)": 20, "Chicken Parmigiana Pizza 16in ($22)": 22, "Pepperoni Calzone ($12)": 12, "Mozarella Calzone ($12)": 12, "Cheese Steak Stromboli ($14)": 14, "Buffalo Chicken Pizza 16in ($22)": 22}

restaurant_image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuQucWWXvrvfCOjksF6VShJ1uVjREDT6AzBA&s"
logo = "https://shop-logos.imgix.net/shops/20751/original/Peppinos_Pizza.PNG?auto=compress,format"

items = {'Garlic Bread': 2.50, 'Garlic Bread with Cheese': .5, 'French Fries': 5, 'Cheese Slice': 3, 'pep':.3,'sau':.3,'mush':.3, 
         'Cheese Pizza': 13, '14in': 2,'16in': 4, '18in': 7,'Sicilian Pizza': 20, 'Meat Lovers Pizza': 20, 'pepP':1,'sauP':1,'mushP':1,
         'Penne Alla Vodka':23,'Chicken Alfredo':25,'Lasagna':22}

initial = ["Garlic Bread", "French Fries", "Cheese Slice", "Cheese Pizza", "Sicilian Pizza", "Meat Lovers Pizza", "Penne Alla Vodka", "Chicken Alfredo", "Lasagna"]
#options 
options = {"Garlic Bread": ["Garlic Bread with Cheese"], "Cheese Slice": ["pep", "sau", "mush"], "Cheese Pizza": ["pepP", "sauP", "mushP", "14in", "16in", "18in"]}
labels = {"Garlic Bread with Cheese": "with cheese", "pep": "Pepperoni (+$0.30)", "sau": "Sausage (+$0.30)", "mush": "Mushrooms (+$0.30)", "pepP": 
          "Pepperoni (+$1.00)", "sauP": "Sausage (+$1.00)", "mushP": "Mushrooms (+$1.00)",
          "14in": "Size upgrade: 14in (+$2.00)", "16in": "Size upgrade: 16in (+$4.00)", "18in": "Size upgrade: 18in (+$7.00)",}

order_time = 0

def main(request):
    """ respond to url, delegate work to template"""

    template_name = "restaurant/main.html"

    context = {
        'restaurant': restaurant_image,
        'logo': logo
    }

    #dict of ctxt vars
    return render(request, template_name, context)

def order(request):
    """ respond to url, delegate work to template"""

    template_name = "restaurant/order.html"
    #dict of ctxt vars
    context = {
        'dailyspecial': random.choice(dailyspecial),
        'logo': logo
    }

    
    return render(request, template_name, context)


def submit(request):
    total = 0.0
    ordered = []
    template_name = "restaurant/confirmation.html"

    # calculate ready time
    now = time.time()
    print(now)
    ballpark = random.randint(30,60)
    ready = now + ballpark * 60
    readytime = time.ctime(ready)


    if request.POST:
        #required inputs
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        special = request.POST.get('special')

        #daily special
        daily = request.POST.get('daily')
        print(daily)
        if daily:
            total += dailyprices.get(daily, 0)
            ordered += [daily]

        #ordered items
        for i in initial:
            if i in request.POST:
                addon = []
                curr = i
                price = items[i]
                for a in options.get(i,[]):
                    if a in request.POST:
                        addon.append(labels[a])
                        price += items[a]
                if addon:
                     curr += " (" + ", ".join(addon) + ")"


                curr += " ${:,.2f}".format(price)
                ordered+= [curr]
                total += price
                
        dollars = " ${:,.2f}".format(total)
        print(ordered)
        
        
        
    context = {
        'name': name,
        'email': email,
        'number': number,
        'ordered': ordered,
        'total': dollars,
        'special': special,
        'readytime': readytime,
        'logo': logo
    } 
       

    return render(request, template_name, context)
