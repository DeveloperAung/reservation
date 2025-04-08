from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    CATEGORY_CHOICES = (
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
