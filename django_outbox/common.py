_F='cpanelresult'
_E='authbox.web.id'
_D='srv135.niagahoster.com'
_C='QQ0GWU5HOJ7OYZWNM82IX2IA6PZGEK6M'
_B='u1578244'
_A=True
import calendar,json,os
from datetime import datetime,timedelta
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
from django.contrib.sites.models import Site
from django.db.models import Subquery
from django.http import Http404,JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from core.models import Agency,Service,Template,User
def get_site_id(request):
	D=request
	if not D:return-1
	E=D.user.id
	if not E:return-1
	C=User.objects.filter(id=D.user.id)
	if not C:return-2
	C=C.get();A=C.agency.filter(is_default=_A)
	if not A:return-3
	if len(A)>1:return-31
	A=A[0];print('agency == ',A);B=Service.objects.filter(agency_id=A.id,is_default=_A)
	if not B:return-4
	if len(B)>1:return-41
	B=B[0]
	if B:return B.site_id
	return 0
def get_agency_from(request):A=User.objects.get(id=request.user.id);B=A.agency.all()[0];return B.id
def create_sub_domain(sub_domain):A=_B;B=_C;C=_D;D=_E;E='/public_html';F=f"curl -H'Authorization: cpanel {A}:{B}' 'https://{C}:2083/json-api/cpanel?cpanel_jsonapi_func=addsubdomain&cpanel_jsonapi_module=SubDomain&cpanel_jsonapi_version=2&domain={sub_domain}&rootdomain={D}&dir={E}'";G=os.popen(F).read();H=json.loads(G);return H[_F]['data'][0]
def delete_sub_domain(sub_domain):A=_B;B=_C;C=_D;D=_E;E=f"curl -H'Authorization: cpanel {A}:{B}' 'https://{C}:2083/json-api/cpanel?cpanel_jsonapi_func=delsubdomain&cpanel_jsonapi_module=SubDomain&cpanel_jsonapi_version=2&domain={sub_domain}.{D}'";F=os.popen(E).read();G=json.loads(F);return G[_F]['data'][0]
def get_site_id_front(request):
	A=Site.objects.filter(domain=request.get_host()).values_list('id',flat=_A)
	if A:return A[0]
	return 0
def get_template(site_id,is_frontend=_A):
	B=site_id;print('site',B);A=Template.objects.filter(site__id=B,is_frontend=is_frontend).values_list('rel_path',flat=_A)[:1];print('template',A)
	if A:return A[0]
	raise Http404("template belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%'/admin')
def get_week_date(year,month,day):
	A=calendar.Calendar();A=A.monthdatescalendar(year,month);E=False;D=0
	for D in range(0,len(A)-1):
		for F in A[D]:
			if F.day==day:E=_A;break
		if E:break
	B=A[D][0];B=datetime(B.year,B.month,B.day,0,0,0);C=A[D][6];C=datetime(C.year,C.month,C.day,23,59,59);return B,C
def get_month_range(date):A=date;B=calendar.monthrange(A.year,A.month)[1];C=datetime(A.year,A.month,1);D=datetime(A.year,A.month,B,23,59,59);return C,D
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