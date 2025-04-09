from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import make_aware, is_naive, get_current_timezone


class Reservation(models.Model):
    CATEGORY_CHOICES = (
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    )
    RECURRENCE_CHOICES = (
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    recurrence = models.CharField(max_length=20, choices=RECURRENCE_CHOICES, default='none')
    recurrence_end = models.DateTimeField(null=True, blank=True)  # Optional end date for recurrence
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_recurring_events(self, start, end):
        """Generate recurring events for FullCalendar."""
        tz = get_current_timezone()
        if is_naive(self.start_time):
            self.start_time = make_aware(self.start_time, timezone=tz)

        if is_naive(self.end_time):
            self.end_time = make_aware(self.end_time, timezone=tz)

        if is_naive(start):
            start = make_aware(start, timezone=tz)

        if is_naive(end):
            end = make_aware(end, timezone=tz)

        if self.recurrence == 'none' or self.recurrence is None:

            if self.start_time >= start and self.end_time <= end:
                return [{'start': self.start_time, 'end': self.end_time}]
            return []

        rrule_map = {'daily': DAILY, 'weekly': WEEKLY, 'monthly': MONTHLY}
        duration = self.end_time - self.start_time
        rule = rrule(
            rrule_map[self.recurrence],
            dtstart=self.start_time,
            until=self.recurrence_end or end
        )
        events = []
        for dt in rule:
            if dt > end:
                break
            if dt >= start:
                events.append({
                    'start': dt,
                    'end': dt + duration
                })
        return events
