from django.shortcuts import render

def landing_page(request):
    return render(request, 'core/landing.html')

def o_itinga(request):
    return render(request, 'core/o-itinga.html')

def sobre_nos(request):
    return render(request, 'core/sobre-nos.html')