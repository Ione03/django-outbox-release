_E='/id/dashboard/'
_D='force_authenticate'
_C='User-Agent'
_B=False
_A=True
import io,os,urllib
from datetime import datetime,timedelta
from ipaddress import ip_address as validate_ip
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login,logout
from django.http import JsonResponse
from django.shortcuts import HttpResponse,redirect,render
from PIL import Image
from core.models import Service,User,UserLog
from django_outbox.common import get_site_id
from .  import forms
from .forms import CustomUserCreationForm
from .models import Template,ModelListSetting
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str as force_text
from .tokens import account_activation_token
def register(request):
	B=request
	if B.method=='POST':
		A=CustomUserCreationForm(B.POST)
		if A.is_valid():C=A.save();return redirect('/account/login')
	else:A=forms.CustomUserCreationForm(label_suffix='')
	return render(B,'registration/register.html',{'form':A})
def create_unique_name(request):A=get_site_id(request);B=datetime.now();return str(A)+'-'+B.strftime('%Y%m%d-%H%M%S-%f')
def download_image(request,url):B=create_unique_name(request);F=settings.MEDIA_ROOT;A='youtube/';C=os.path.join(F,A);G=os.makedirs(C,exist_ok=_A);print('create dir = ',G);D='.jpg';A=A+B+D;H=B+D;E=os.path.join(C,H);print('full name = ',E);urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({'http':'proxy.server:3128'})));urllib.request.urlretrieve(url,E);return A
def upload_photo(request,width,height,save_as_png=0):
	O='JPEG';N='image/png';M='.jpeg';L='data.content_type=';I=save_as_png;H=request;A=H.FILES.get('photo');P=Image.open(io.BytesIO(A.read()));B=P.resize((width,height),Image.ANTIALIAS);F=create_unique_name(H);G=datetime.now();Q=G.strftime('%Y');R=G.strftime('%m');S=G.strftime('%d');print(L,A.content_type)
	if A.content_type=='image/gif':D='.gif'
	elif A.content_type=='image/jpeg':D=M
	elif A.content_type=='image/jpg':D='.jpg'
	elif A.content_type==N:D=M
	elif A.content_type=='image/bmp':D='.bmp'
	else:D='.ief'
	J=settings.MEDIA_ROOT;E=os.path.join('crop',Q,R,S);C=os.path.join(J,E);print('media_root_path',C);T=os.makedirs(C,exist_ok=_A)
	if not I:F=F+D
	else:F=F+'.png'
	E=os.path.join(E,F);print('path = ',E);C=os.path.join(J,E);print(L,A.content_type)
	if not I:
		print('not save_as_png')
		if A.content_type==N:
			B.load();print('resized_image.mode=',B.mode);K=Image.new('RGB',B.size,(255,255,255))
			if B.mode=='RGBA':K.paste(B,mask=B.getchannel('A'));K.save(C,O,quality=80,optimize=_A)
			else:B.save(C,O,quality=80,optimize=_A)
		else:print('NON PNG');B.save(C,quality=80,optimize=_A)
	else:print('save as png');B.save(C,quality=80,optimize=_A)
	return HttpResponse(E)
def get_ip(request):
	B=request;A=B.headers.get('X-Forwarded-For',B.META.get('REMOTE_ADDR','127.0.0.1'))
	if A:
		try:validate_ip(A)
		except ValueError:A='10.0.0.1'
	return A
def redirect_to_main(request,social_media,site_id):B=social_media;A=request;C=get_ip(A);D=A.headers.get(_C,'')[:255];E,F=UserLog.objects.get_or_create(site_id=site_id,social_media=B,ip_address=C,user_agent=D,is_expired=_B);return redirect('/id/accounts/'+B+'/login/?process=login&s='+str(E.uuid))
def pre_login(request):
	A=request;B=get_site_id(A);C=datetime.now();C=C-timedelta(minutes=1);UserLog.objects.filter(site_id=B,is_expired=_B,created_at__lt=C).update(is_expired=_A);D=get_ip(A);E=A.headers.get(_C,'')[:255];F=get_active_domain(A)
	if not UserLog.objects.filter(site_id=B,is_expired=_B,is_complete=_B,user_agent=E,ip_address=D):UserLog.objects.create(site_id=B,user_agent=E,ip_address=D,active_domain=F['active_domain'])
	return HttpResponse({'ok'})
def force_authenticate_in(request,user_id):
	A=User.objects.get(id=user_id)
	if A:A.backend=settings.AUTHENTICATION_BACKENDS[0];print(_D);login(request,A)
	return HttpResponse({'ok'})
def force_authenticate_out(request):logout(request);return HttpResponse({'ok'})
def social_media(request,user_id,uuid):
	F='user not found';D=request;B=UserLog.objects.filter(uuid=uuid)
	if B:
		B=B.get()
		if B.site.domain!=D.get_host():return HttpResponse({'site ID not valid'})
	else:return HttpResponse({'session key not valid'})
	A=None;C=Service.objects.filter(site_id=B.site.id)
	if C:
		C=C.get();A=User.objects.filter(id=user_id)
		if A:
			A=A.get();E=_B
			for G in A.agency.all():
				if G.id==C.agency.id:E=_A;break
			if not E:return HttpResponse({'user not registered in this site'})
		else:return HttpResponse({F})
	else:return HttpResponse({'service not found'})
	if A:A.backend=settings.AUTHENTICATION_BACKENDS[0];print(_D);login(D,A);return redirect(_E)
	return HttpResponse({F})
def post_login_redirect(request,user_id,uuid):
	A=UserLog.objects.filter(uuid=uuid)
	if A:A=A.get();A.user_id=user_id;A.save();B=request.scheme+'://';B=B+A.site.domain;print(B);return HttpResponse(B+'/id/accounts/login/?u='+str(A.user_id)+'&media='+A.social_media+'&s='+str(A.uuid))
	return HttpResponse(_E)
def get_crop_image_size(request,model_name):
	C=model_name;F=get_site_id(request);A=Template.objects.filter(site__id=F,is_frontend=_A)[:1];print('template',A);print('model_name',C);C=C.replace('_',' ')
	if A:
		A=A.get().id;D=0;E=0;B=ModelListSetting.objects.filter(template_id=A,model_list__name__iexact=C)
		if B:B=B.get();D=B.image_width;E=B.image_height
	return JsonResponse({'ww':D,'hh':E},safe=_B)
def account_activation_sent(request):return render(request,'account_activation_sent.html')
def activate(request,uidb64,token):
	try:B=force_text(urlsafe_base64_decode(uidb64));A=User.objects.get(pk=B)
	except (TypeError,ValueError,OverflowError,User.DoesNotExist):A=None
	if A is not None and account_activation_token.check_token(A,token):A.email_confirmed=_A;A.save();return redirect('user')
	else:return render(request,'account_activation_invalid.html')