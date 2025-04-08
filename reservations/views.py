from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reservation
from .forms import ReservationForm
from django.http import JsonResponse
from django.core.serializers import serialize
import json


def calendar_view(request):
    return render(request, 'reservations/calendar.html')


def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('calendar')
    else:
        form = ReservationForm()
    return render(request, 'reservations/reservation_form.html', {'form': form})

@login_required
def get_events(request):
    reservations = Reservation.objects.filter(user=request.user)
    events = []
    for reservation in reservations:
        events.append({
            'title': reservation.title,
            'start': reservation.start_time.isoformat(),
            'end': reservation.end_time.isoformat(),
            'description': reservation.description,
        })
    return JsonResponse(events, safe=False)