'''
****************************************
formatmonth function comes from:

https://github.com/llazzaro/django-scheduler
****************************************
'''
from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from .models import Schedule

class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events

    def formatday(self, day, weekday, events):
        # Return a day as a table cell.
        events_from_day = events.filter(day__day=day).order_by('start_time')
        events_html = "<ul>"
        for event in events_from_day:
            event_name = '<a href=\"posts/%d/detail\">' % event.id + \
            event.title + '</a>'
            events_html += event_name + "<br>" + str(event.start_time) + "<br>"
        events_html += "</ul>"

        if day == 0:
            # return day outside month
            return '<td bgcolor="#DCDCDC" class="noday">&nbsp;</td>'
        else:
            return '<td class="%s"> %d %s </td>' \
            % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, week, events):
        # Return a complete week as a table row.
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in week)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        # Return a formatted month as a table.

        events = self.events.filter(day__month=themonth)
        #events = Schedule.objects.filter(author=self.user)

        v = []
        a = v.append
        a('<table border="5" bordercolorlight="#DCDCDC" bordercolordark="#2F4F4F"" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)