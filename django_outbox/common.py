_B='/admin'
_A=True
import calendar
from datetime import datetime,timedelta
from core.models import Service,Template
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
from django.contrib.sites.models import Site
from django.db.models import Subquery
from django.http import Http404
from django.utils.translation import gettext_lazy as _
def get_site_id(request):
	A=Site.objects.filter(domain=request.get_host()).values_list('id',flat=_A)
	if A:return A[0]
	raise Http404("domain belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_B)
def get_template(site_id,is_frontend=_A):
	A=Template.objects.filter(site__id=site_id,is_frontend=is_frontend).values_list('rel_path',flat=_A)[:1]
	if A:return A[0]
	raise Http404("template belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_B)
def get_week_date(year,month,day):
	A=calendar.Calendar();A=A.monthdatescalendar(year,month);E=False;D=0
	for D in range(0,len(A)-1):
		for F in A[D]:
			if F.day==day:E=_A;break
		if E:break
	B=A[D][0];B=datetime(B.year,B.month,B.day,0,0,0);C=A[D][6];C=datetime(C.year,C.month,C.day,23,59,59);return B,C
def add_months(sourcedate,months):B=sourcedate;A=B.month-1+months;C=B.year+A//12;A=A%12+1;D=min(B.day,calendar.monthrange(C,A)[1]);return datetime(C,A,D)
def get_natural_datetime(data_datetime,skrg=datetime.now()):
	H='a week ago';B=data_datetime;A=skrg;I=datetime(A.year,A.month,A.day,0,0,0);J=datetime(A.year,A.month,A.day,23,59,59);D=A-timedelta(days=1);K=datetime(D.year,D.month,D.day,0,0,0);L=datetime(D.year,D.month,D.day,23,59,59);F,G=get_week_date(A.year,A.month,A.day);M=F-timedelta(days=7);N=G-timedelta(days=7);O=F-timedelta(days=14);P=G-timedelta(days=14);Q=F-timedelta(days=21);R=G-timedelta(days=21);E=calendar.monthrange(A.year,A.month)[1];S=datetime(A.year,A.month,1,0,0,0);T=datetime(A.year,A.month,E,23,59,59);C=add_months(A,-1);E=calendar.monthrange(C.year,C.month)[1];U=datetime(C.year,C.month,1,0,0,0);V=datetime(C.year,C.month,E,23,59,59);C=add_months(A,-2);E=calendar.monthrange(C.year,C.month)[1];W=datetime(C.year,C.month,1,0,0,0);X=datetime(C.year,C.month,E,23,59,59)
	if I<=B<=J:return naturaltime(B)
	elif K<=B<=L:return naturalday(B)
	elif F<=B<=G:return _(B.strftime('%A'))
	elif M<=B<=N:
		if B.weekday()==6:return _(H)
		else:return _(H)+', '+_(B.strftime('%A'))
	elif O<=B<=P and A.weekday()==B.weekday():return _('two weeks ago')
	elif Q<=B<=R and A.weekday()==B.weekday():return _('three weeks ago')
	elif S<=B<=T:return _('this month')
	elif U<=B<=V and (A-B).days>=30:return _('a month ago')
	elif W<=B<=X and (A-B).days>=60:return _('two months ago')
	return naturalday(B)