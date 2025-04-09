from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
import json
from datetime import datetime
from dateutil import parser
from .models import Reservation
from .forms import ReservationForm


@login_required
def calendar_view(request):
    return render(request, 'reservations/calendar.html')


@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            send_mail(
                subject=f'New Reservation: {reservation.title}',
                message=f'You have created a reservation:\n\nTitle: {reservation.title}\nStart: {reservation.start_time}\nEnd: {reservation.end_time}\nCategory: {reservation.category}',
                from_email=None,
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            return redirect('calendar')
    else:
        form = ReservationForm()
    return render(request, 'reservations/reservation_form.html', {'form': form})


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            send_mail(
                subject=f'Updated Reservation: {reservation.title}',
                message=f'You have updated a reservation:\n\nTitle: {reservation.title}\nStart: {reservation.start_time}\nEnd: {reservation.end_time}\nCategory: {reservation.category}',
                from_email=None,
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            return redirect('calendar')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservations/reservation_form.html', {'form': form, 'edit': True})


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('calendar')
    return render(request, 'reservations/delete_confirm.html', {'reservation': reservation})


@login_required
def get_events(request):
    from dateutil import parser

    start = request.GET.get('start')
    end = request.GET.get('end')
    reservations = Reservation.objects.filter(user=request.user)
    events = []

    for reservation in reservations:
        color_map = {
            'work': '#3788d8',
            'personal': '#00cc00',
            'meeting': '#ff9900',
            'other': '#808080'
        }

        try:
            start_dt = parser.parse(start) if start else reservation.start_time
            end_dt = parser.parse(end) if end else (reservation.recurrence_end or reservation.end_time)
        except ValueError:
            print('value error', ValueError)
            start_dt = reservation.start_time
            end_dt = reservation.recurrence_end or reservation.end_time

        recurring_events = reservation.get_recurring_events(start_dt, end_dt)
        for event in recurring_events:
            events.append({
                'id': reservation.id,
                'title': reservation.title,
                'start': event['start'].isoformat(),
                'end': event['end'].isoformat(),
                'description': reservation.description,
                'category': reservation.category,
                'backgroundColor': color_map.get(reservation.category, '#808080'),
                'borderColor': '#000000'
            })
    return JsonResponse(events, safe=False)


@require_POST
@login_required
def update_event(request):
    data = json.loads(request.body)
    reservation = get_object_or_404(Reservation, id=data['id'], user=request.user)
    reservation.start_time = data['start']
    reservation.end_time = data['end']
    reservation.save()
    return JsonResponse({'status': 'success'})
