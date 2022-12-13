from core.models import Service
from django.http import Http404
from django.shortcuts import redirect
from .common import get_site_id
def service_exists(request):A=get_site_id(request);return Service.objects.filter(site_id=A).values_list('kind',flat=True)
def redirect_service(request):
	A=request;B=service_exists(A)
	if B:
		if B[0]==1:return redirect('/id/edu/')
	raise Http404("service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(A.get_host(),'/admin'))