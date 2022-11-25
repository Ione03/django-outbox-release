from PIL import Image
from django_outbox.common import get_site_id
from datetime import datetime
from django.conf import settings
from django.shortcuts import HttpResponse
import io,os
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render,redirect
from .  import forms
def register(request):
	B=request
	if B.method=='POST':
		A=CustomUserCreationForm(B.POST)
		if A.is_valid():C=A.save();return redirect('/account/login')
	else:A=forms.CustomUserCreationForm(label_suffix='')
	return render(B,'registration/register.html',{'form':A})
def upload_photo(request,width,height):
	M='JPEG';L='image/png';K='.jpeg';I=request;H='/';G=True;A=I.FILES.get('photo');N=get_site_id(I);O=Image.open(io.BytesIO(A.read()));B=O.resize((width,height),Image.ANTIALIAS);E=datetime.now();P=str(N)+'-'+E.strftime('%Y%m%d-%H%M%S-%f');Q=E.strftime('%Y');R=E.strftime('%m');S=E.strftime('%d')
	if A.content_type=='image/gif':D='.gif'
	elif A.content_type=='image/jpeg':D=K
	elif A.content_type=='image/jpg':D='.jpg'
	elif A.content_type==L:D=K
	elif A.content_type=='image/bmp':D='.bmp'
	else:D='.ief'
	T=settings.BASE_DIR;F=settings.MEDIA_ROOT;C='crop/'+Q+H+R+H+S+H;U=os.makedirs(F/C,exist_ok=G);C=C+P+D
	if A.content_type==L:
		B.load();J=Image.new('RGB',B.size,(255,255,255))
		if B.mode=='RGBA':J.paste(B,mask=B.getchannel('A'));J.save(F/C,M,quality=80,optimize=G)
		else:B.save(F/C,M,quality=80,optimize=G)
	else:B.save(F/C,quality=80,optimize=G)
	return HttpResponse(C)