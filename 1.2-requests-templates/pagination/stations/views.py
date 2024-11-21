import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open(BUS_STATION_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        bus_stations_ = [row for row in reader]

    paginator = Paginator(bus_stations_, 10)

    try:
        page_number = int(request.GET.get("page", 1))
    except ValueError:
        page_number = 1

    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page,
        'page': page,
    }
    return render(request, 'stations/index.html', context)

