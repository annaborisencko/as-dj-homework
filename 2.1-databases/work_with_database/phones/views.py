from django.shortcuts import render, redirect
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    
    if request.GET.get('sort') == 'name':
        phones_objects = Phone.objects.all().order_by('name')
    elif request.GET.get('sort') == 'min_price':
        phones_objects = Phone.objects.all().order_by('price')
    elif request.GET.get('sort') == 'max_price':
        phones_objects = Phone.objects.all().order_by('-price')
    else:
        phones_objects = Phone.objects.all()

    context = {
        'phones': phones_objects
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {}
    return render(request, template, context)
