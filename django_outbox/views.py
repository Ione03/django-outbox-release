from django.http import Http404
from django.shortcuts import redirect
from core.models import Service
from .common import get_site_id_front
def service_exists(request):
	A=get_site_id_front(request);print('site id from service is exists',A);B=Service.objects.filter(site_id=A);print('service',B)
	for C in B:
		if C.is_demo:return'demo'
		else:return C.get_kind_display()
	return None
def redirect_service(request):
	A=request;print('redirect....');B=service_exists(A)
	if B:return redirect(f"/id/{B}/")
	else:print('return NONE, SET redirect to NONE');return redirect(f"/id/demo/")
	raise Http404("service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(A.get_host(),'/admin'))