_A='/admin'
from calendar import monthrange
from datetime import datetime,timedelta
from core.models import Service,Template
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
from django.contrib.sites.models import Site
from django.db.models import Subquery
from django.http import Http404
from django.utils.translation import gettext_lazy as _
def get_site_id(request):
	A=Site.objects.filter(domain=request.get_host()).values_list('id',flat=True)
	if A:return A[0]
	raise Http404("domain belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_A)
def get_template(site_id,is_frontend=True):
	A=Template.objects.filter(site__id=site_id,is_frontend=is_frontend).values_list('rel_path',flat=True)[:1]
	if A:return A[0]
	raise Http404("template belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_A)
def get_natural_datetime(data_datetime):
	B=data_datetime;B=B.replace(tzinfo=None);print(B);A=datetime.now();print(A);E=A-timedelta(hours=24);F=A-timedelta(hours=48);G=A-timedelta(days=7);H=A-timedelta(days=14);I=A-timedelta(days=21);J=A-timedelta(days=28);D=monthrange(A.year,A.month)[1];K=A-timedelta(days=D+1)
	if E<B<A:return naturaltime(B)
	elif F<B<A:return naturalday(B)
	elif G<B<A:return _(B.strftime('%A'))
	elif H<B<A:
		C=(A-B).days-7
		if C==0:return _('Seminggu yang lalu')
	elif I<B<A:
		C=(A-B).days-14
		if C==0:return _('Dua minggu yang lalu')
	elif J<B<A:
		C=(A-B).days-21
		if C==0:return _('Tiga minggu yang lalu')
	elif K<B<A:
		C=(A-B).days-D
		if C==0:return _('Sebulan yang lalu')
	return naturalday(B)