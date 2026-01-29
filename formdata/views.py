from django.shortcuts import render

# Create your views here.

def form(request):
    '''Show the web page with the form.'''
 
 
    template_name = "formdata/form.html"
    return render(request, template_name)

def submit(request):
    template_name = "formdata/confirmation.html"

    if request.POST:
        name = request.POST['name']
        fav = request.POST['fav']

    context = {
        'name': name,
        'fav': fav,
    }

    return render(request, template_name, context=context)