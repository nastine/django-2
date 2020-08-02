from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
import csv

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, mode='r', encoding='cp1251') as f:
        stations_info = list(csv.DictReader(f))

    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(stations_info, 10)
    stations = paginator.get_page(current_page)

    previous_page, next_page = None, None
    if stations.has_previous():
        previous_page = f'?page={stations.previous_page_number()}'
    if stations.has_next():
        next_page = f'?page={stations.next_page_number()}'

    return render(request, 'index.html', context={
        'bus_stations': stations,
        'current_page': current_page,
        'prev_page_url': previous_page,
        'next_page_url': next_page,
    })

