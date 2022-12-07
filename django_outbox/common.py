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
def get_natural_datetime(skrg,data_datetime):
	B=data_datetime;A=skrg;B=B.replace(tzinfo=None);H=datetime(A.year,A.month,A.day,0,0,0);I=datetime(A.year,A.month,A.day,23,59,59);D=A-timedelta(days=1);J=datetime(D.year,D.month,D.day,0,0,0);K=datetime(D.year,D.month,D.day,23,59,59);F,G=get_week_date(A.year,A.month,A.day);L=F-timedelta(days=7);M=G-timedelta(days=7);N=F-timedelta(days=14);O=G-timedelta(days=14);P=F-timedelta(days=21);Q=G-timedelta(days=21);E=calendar.monthrange(A.year,A.month)[1];R=datetime(A.year,A.month,1,0,0,0);S=datetime(A.year,A.month,E,23,59,59);C=add_months(A,-1);E=calendar.monthrange(C.year,C.month)[1];T=datetime(C.year,C.month,1,0,0,0);U=datetime(C.year,C.month,E,23,59,59);C=add_months(A,-2);E=calendar.monthrange(C.year,C.month)[1];V=datetime(C.year,C.month,1,0,0,0);W=datetime(C.year,C.month,E,23,59,59)
	if H<=B<=I:return naturaltime(B)
	elif J<=B<=K:return naturalday(B)
	elif F<=B<=G:return _(B.strftime('%A'))
	elif L<=B<=M:return _('minggu lalu')+' hari '+_(B.strftime('%A'))
	elif N<=B<=O and A.weekday()==B.weekday():return _('dua minggu lalu')
	elif P<=B<=Q and A.weekday()==B.weekday():return _('tiga minggu lalu')
	elif R<=B<=S:return _('bulan ini')
	elif T<=B<=U and (A-B).days>=30:return _('bulan lalu')
	elif V<=B<=W and (A-B).days>=60:return _('dua bulan lalu')
	return naturalday(B)