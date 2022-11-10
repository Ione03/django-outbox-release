from core.models import Service
from django.http import Http404
from django.shortcuts import redirect
from .common import get_site_id
def redirect_service(request):
	B=request;print('redirect');C=get_site_id(B);A=Service.objects.filter(site_id=C).values_list('kind',flat=True);print('service = ',A)
	if A:
		if A[0]==1:return redirect('/id/edu')
	raise Http404("service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(B.get_host(),'/admin'))