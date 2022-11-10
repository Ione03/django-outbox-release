from PIL import Image
from django_outbox.common import get_site_id
from datetime import datetime
from django.conf import settings
from django.shortcuts import HttpResponse
import io,os
def upload_photo(request,width,height):
	R='JPEG';Q='RGBA';P='image/png';O='.jpeg';K=height;J=width;I=request;H='/';G=True;print('inside upload photo');print(J);print(K);print('result = ');A=I.FILES.get('photo');print(A);print(A.size);print('Content TYPE = ');print(A.content_type);S=get_site_id(I);L=Image.open(io.BytesIO(A.read()));print('image');print(L);C=L.resize((J,K),Image.ANTIALIAS);print('resized_image');print(C);F=datetime.now();M=str(S)+'-'+F.strftime('%Y%m%d-%H%M%S-%f');print('filename');print(M);T=F.strftime('%Y');U=F.strftime('%m');V=F.strftime('%d')
	if A.content_type=='image/gif':D='.gif'
	elif A.content_type=='image/jpeg':D=O
	elif A.content_type=='image/jpg':D='.jpg'
	elif A.content_type==P:D=O
	elif A.content_type=='image/bmp':D='.bmp'
	else:D='.ief'
	print('ext');print(D);W=settings.BASE_DIR;E=settings.MEDIA_ROOT;print('base_dir');print(W);B='crop/'+T+H+U+H+V+H;print('path');print(B);X=os.makedirs(E/B,exist_ok=G);print('makedirs');print(X);print('media root + path');print(E/B);B=B+M+D
	if A.content_type==P:
		C.load();N=Image.new('RGB',C.size,(255,255,255));print('Image PNG ')
		if C.mode==Q:print(Q);N.paste(C,mask=C.getchannel('A'));N.save(E/B,R,quality=80,optimize=G)
		else:print('NON RGBA');C.save(E/B,R,quality=80,optimize=G)
	else:print('NON PNG');C.save(E/B,quality=80,optimize=G)
	print('resize image');print(B);return HttpResponse(B)