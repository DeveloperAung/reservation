from django.urls import path
from . import views


urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('create/', views.create_reservation, name='create_reservation'),
    path('events/', views.get_events, name='get_events'),
]