from django.urls import path
from . import views


urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('create/', views.create_reservation, name='create_reservation'),
    path('edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('events/', views.get_events, name='get_events'),
    path('update_event/', views.update_event, name='update_event'),
]
