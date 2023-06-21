_F='credentials not found!'
_E='error while add event!'
_D='Delete Calendar Cache'
_C=False
_B=True
_A=None
import datetime,os
from beautiful_date import *
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from gcsa.calendar import AccessRoles,Calendar
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import DAILY,SA,SU,Recurrence
from gcsa.serializers.calendar_serializer import CalendarSerializer
from django_outbox.common import get_month_range,get_site_id_front
from education.models import GoogleCalendar as GC
def is_event_exists(gcalendar,start_date,end_date,event_summary=_A):
	events=gcalendar.get_events(start_date,end_date)
	if event_summary:
		summary=event_summary.strip().lower()
		for event in events:
			if event.summary.strip().lower()==summary:return _B
	elif events:
		for event in events:return _B
	return _C
def sync_calendar(request,cal,default_cal,credentials,date=_A):
	print('credentials',credentials);site_id=get_site_id_front(request);gcal_default=GoogleCalendar(default_cal,credentials_path=credentials);gcal=GoogleCalendar(cal,credentials_path=credentials)
	if not date:skrg=datetime.datetime.now()
	else:skrg=date
	start,end=get_month_range(skrg);events=gcal.get_events(start,end)
	for i in events:
		if not is_event_exists(gcal_default,i.start,i.end,i.summary):
			try:gcal_default.add_event(i);print('done add event',i);cache.delete(f"calendar_cache_{start.year}_{start.month}",version=site_id);print(_D,str(site_id))
			except Exception as e:print(_E,e)
		else:print('events already exists',i)
def sync_calendar_all(request,year=_A,month=_A):
	date=_A
	if year and month:date=datetime.datetime(year,month,1)
	site_id=get_site_id_front(request);gcal_default=GC.objects.filter(site_id=site_id,is_default=_B)[:1];gcal=GC.objects.filter(site_id=site_id,is_default=_C)
	if gcal_default:gcal_default=gcal_default.get()
	credentials=''
	if gcal_default.file_path_doc:credentials=gcal_default.file_path_doc.path
	if not credentials:return _F
	for i in gcal:
		if gcal_default.file_path_doc:sync_calendar(request,i.cal_name,gcal_default.cal_name,credentials=credentials,date=date)
	res=cache.get(f"calendar_cache_{year}_{month}",version=site_id)
	if not res:
		res=[];calendar=GoogleCalendar(gcal_default.cal_name,credentials_path=credentials);start,end=get_month_range(date);events=calendar.get_events(start,end)
		for i in events:tmp={'title':i.summary,'start':i.start,'end':i.end,'desc':i.description};res.append(tmp)
		print('GET FROM default Cal');cache.set(f"calendar_cache_{year}_{month}",res,version=site_id)
	else:print('GET FROM calendar_cache')
	return res
def add_new_events(request,default_cal,credentials_path,event_name,start,end,description):
	site_id=get_site_id(request);gcal_default=GC.objects.filter(site_id=site_id,is_default=_B)[:1]
	if gcal_default:gcal_default=gcal_default.get()
	credentials=''
	if gcal_default.file_path_doc:credentials=gcal_default.file_path_doc.path
	if not credentials:return _F
	event=Event(event_name,start=start,end=end,description=description,minutes_before_email_reminder=50);cal=GoogleCalendar(gcal_default.cal_name,credentials_path=credentials)
	if not is_event_exists(cal,start,end,event_name):
		try:cal.add_event(event);print('Event added!');cache.delete(f"calendar_cache_{start.year}_{start.month}",version=site_id);print(_D,str(site_id))
		except Exception as e:print(_E,e)
	else:print('event already exists!')
def index(request):
	A='credentials.json';calendar=GoogleCalendar('suratiwan03@gmail.com',credentials_path=A);print(f"calendar {calendar}");start=(6/Jun/2023)[12];end=(30/Jun/2023)[11:59:59];events=calendar.get_events(start,end)
	for event in events:print(event.start,' -- ',event.summary)
	for i in calendar.get_calendar_list():print(f"calendar list: {i.id}")
	gc=calendar.get_calendar();print(gc.id);gc_by_id=GoogleCalendar('inaqneoq@gmail.com',credentials_path=A)
	for i in gc_by_id.get_events(start,end):print(f"event summary: {i.summary}")
	return JsonResponse(CalendarSerializer.to_json(gc),safe=_C)