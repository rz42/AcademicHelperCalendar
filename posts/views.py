from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Schedule
import datetime
import calendar
from django.urls import reverse
from django.utils.safestring import mark_safe
from .utils import EventCalendar
from django.views.generic import DeleteView
from django.core.exceptions import ValidationError


@login_required
def create(request):
	username, userid = my_view(request)
	if request.method == "POST":
		if request.POST['title'] and request.POST['day'] and \
		request.POST['start_time'] and request.POST['end_time']:
			event = Schedule()
			event.pub_date = timezone.datetime.now()
			event.title = request.POST['title']
			temptitle = request.POST['title']
			event.day = request.POST['day']
			tempday = request.POST['day']
			event.start_time = request.POST['start_time']
			tempst = request.POST['start_time']
			event.end_time = request.POST['end_time']
			tempet = request.POST['end_time']
			event.author = request.user
			event.notes = request.POST['notes']
			try:
			    event.clean()
			    event.save()
			    return redirect('home')
			except ValidationError as e:
				msg = ""
				for i in e:
					msg += i
			    # Display the validation error as error msg to the user.
				return render(request, 'posts/create.html', {'error': msg})
		else:
			return render(request, 'posts/create.html', {'error': 'ERROR: You must include title, day, start time and end time to create an event'})
	else:
		return render(request, 'posts/create.html')

def my_view(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        userid = request.user.id
        return username, userid

@login_required
def home(request, extra_context=None):
    username, userid = my_view(request)
    after_day = request.GET.get('day__gte', None)
    extra_context = extra_context or {}
    if not after_day:
        today = datetime.date.today()
    else:
        try:
            split_after_day = after_day.split('-')
            today = datetime.date(year=int(split_after_day[0]), \
                month=int(split_after_day[1]), day=1)
        except:
            today = datetime.date.today()
    # find last day of previous month
    lDay = datetime.date(year=today.year, month=today.month, day=1) \
            - datetime.timedelta(days=1)
    # get the first day of previous month
    previous_month = datetime.date(year=lDay.year, \
        month=lDay.month, day=1)

    last_day = calendar.monthrange(today.year, today.month)
    # find last day of current month
    next_month = datetime.date(year=today.year, month=today.month, day=last_day[1])
    # goes a single day forward
    next_month = next_month + datetime.timedelta(days=1)
    # find first day of next month
    next_month = datetime.date(year=next_month.year, \
        month=next_month.month, day=1)

    extra_context['previous_month'] =  '?day__gte=' \
        + str(previous_month)
    extra_context['next_month'] = '?day__gte=' + str(next_month)

    # EventCalendar class from utils.py
    schedules = Schedule.objects.filter(author__id=userid)

    cal = EventCalendar(schedules)
    html_calendar = cal.formatmonth(today.year, today.month, withyear=True)
    html_calendar = \
        html_calendar.replace('<td ', '<td  width="200" height="180"')
    extra_context['calendar'] = mark_safe(html_calendar)
    extra_context['username'] = username
    schedules = Schedule.objects.order_by('start_time')
    extra_context['schedules'] = schedules
    return render(request, 'posts/home.html', extra_context) 


	#schedules = Schedule.objects.order_by('start_time')
	#return render(request, 'posts/home.html', {'schedules': schedules}) 

def delete(request, id):
    event = Schedule.objects.filter(pk=id).delete()
    return redirect('home')

def detail(request, pk):
	event = Schedule.objects.get(pk=pk)	    
	username, userid = my_view(request)
	if request.method == "POST":
		if request.POST['title'] and request.POST['day'] and \
		request.POST['start_time'] and request.POST['end_time']:
			new_event = Schedule()
			new_event.title = request.POST['title']
			new_event.day = request.POST['day']
			new_event.start_time = request.POST['start_time']
			new_event.end_time = request.POST['end_time']
			new_event.author = request.user
			new_event.notes = request.POST['notes']
			try:
			    new_event.clean()
			    new_event.save()
			    return delete(request, pk)
			except ValidationError as e:
			    msg = ""
			    for i in e:
			    	msg += i
			    # Display the validation error as error msg to the user.
			    return render(request, 'posts/create.html', {'error': msg})
		else:
			return render(request, 'posts/create.html', {'error': 'ERROR: You must include title, day, start time and end time to create an event'})
	return render(request, 'posts/detail.html', {'event': event})

def userposts(request):
    username, userid = my_view(request)
    org_event = []
    event = Schedule.objects.filter(author__id=userid).order_by('day')
    today = datetime.date.today()
    return render(request, 'posts/userposts.html', {'events': event, 'user': username})

