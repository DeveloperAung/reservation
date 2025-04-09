from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['title', 'description', 'start_time', 'end_time', 'category', 'recurrence', 'recurrence_end']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'recurrence_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'category': forms.Select(),
            'recurrence': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        recurrence_end = cleaned_data.get('recurrence_end')
        recurrence = cleaned_data.get('recurrence')
        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError("End time must be after start time")
        if recurrence != 'none' and recurrence_end and recurrence_end <= start_time:
            raise forms.ValidationError("Recurrence end must be after start time")
        return cleaned_data
