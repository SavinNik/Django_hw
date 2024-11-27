from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'

    sort_by = request.GET.get('sort', 'name')

    if sort_by == 'min_price':
        all_phones = Phone.objects.all().order_by('price')
    elif sort_by == 'max_price':
        all_phones = Phone.objects.all().order_by('-price')
    else:
        all_phones = Phone.objects.all().order_by('name')

    context = {
        'phones': all_phones,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {
        'phone': phone
    }
    return render(request, template, context)
