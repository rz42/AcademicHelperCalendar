from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
 
class Schedule(models.Model):
    title = models.CharField(max_length=200)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def summary(self):
        return self.title[:10]

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedule'

    def overlapCheck(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        start_sig = new_start.split(':')
        this_start = datetime.time(int(start_sig[0]), int(start_sig[1]), int(start_sig[2]))
        end_sig = new_end.split(':')
        this_end = datetime.time(int(end_sig[0]), int(end_sig[1]), int(end_sig[2]))

        # edge case
        if this_start == fixed_end or this_end == fixed_start:
            overlap = False
        # inner limits
        elif (this_start >= fixed_start and this_start <= fixed_end) or \
            (this_end >= fixed_start and this_end <= fixed_end):
            overlap = True
        # outer limits
        elif this_start <= fixed_start and this_end >= fixed_end:
            overlap = True
        return overlap

    def clean(self):
        if self.end_time <= self.start_time:
            msg = 'Ending time must be after the starting time'
            raise ValidationError(msg)
        user_events = Schedule.objects.filter(author=self.author)
        events = user_events.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.overlapCheck(event.start_time, event.end_time, \
                    self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' \
                        + str(event.title) + ' on ' +\
                        str(event.day) + ', ' + str(event.start_time) \
                        + '-' + str(event.end_time))
