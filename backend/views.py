_T='delete'
_S='form_edit'
_R='save_edit'
_Q='language'
_P='update.html'
_O='form_add'
_N='save_add'
_M='file_exists'
_L='create.html'
_K='Action'
_J='Update'
_I='updated_at'
_H='tags'
_G='logo'
_F='POST'
_E='id'
_D='form'
_C=None
_B=False
_A='name'
from core.common import get_agency_info
from django.contrib import messages
from django.db.models import F,OuterRef,Subquery,Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.urls import reverse_lazy
from django.utils.text import Truncator
from django.views.generic import TemplateView
from django_outbox import msgbox
from django_outbox.common import get_natural_datetime,get_site_id,get_template
from education.models import Logo,Tags,TagsTranslation
from core.models import Photo
from parler.utils.context import switch_language
from parler.views import TranslatableCreateView,TranslatableUpdateView
from .forms import TagsForm,LogoForm
from core.forms import PhotoForm
mMsgBox=msgbox.ClsMsgBox()
class IndexView(TemplateView):
	site_id=_C
	def get(A,request,*D,**E):B=request;A.site_id=get_site_id(B);C=get_template(A.site_id,is_frontend=_B);print('template = ',C);A.template_name=C+'index.html';return super(IndexView,A).get(B,*(D),**E)
class TagsView(TemplateView):
	site_id=_C
	def get(A,request,*C,**D):B=request;A.site_id=get_site_id(B);E=get_template(A.site_id,is_frontend=_B);A.template_name=E+'tags.html';return super(TagsView,A).get(B,*(C),**D)
	def get_context_data(B,*C,**D):A=super(TagsView,B).get_context_data(*(C),**D);A['group_id']=2;return A
def tags_ajax(request):
	E=get_site_id(request);C=Tags.objects.all()[0];C.set_current_language('en');F=Subquery(TagsTranslation.objects.filter(master_id=OuterRef(_E),language_code=_E).values(_A));G=C.get_current_language();H=Tags.objects.language(G).filter(site_id=E).annotate(name_id=F);D=[]
	for B in H:A={};A['icon']=_C;A['uuid']=B.uuid;A[_I]=B.updated_at;A['Name (id)']=Truncator(B.name_id).chars(20);A['Name (en)']=Truncator(B.name).chars(20);A[_J]=get_natural_datetime(B.updated_at);A[_K]=_C;D.append(A)
	return JsonResponse(D,safe=_B)
def tags_create(request):
	A=request;C={};D=get_site_id(A);E=get_template(D,is_frontend=_B)+_L
	if A.method==_F:
		F=TagsForm(A.POST)
		if F.is_valid():
			G=Tags.objects.filter(translations__name=A.POST.get(_A))
			if G:messages.info(A,mMsgBox.get(_M));C[_D]=TagsForm()
			else:B=Tags.objects.language(_E).create(name=A.POST.get(_A));B.save();B.set_current_language('en');B.name=A.POST.get(_A);B.save();messages.info(A,mMsgBox.get(_N,A.POST.get(_A)));return redirect(reverse_lazy(_H))
	else:messages.info(A,mMsgBox.get(_O));C[_D]=TagsForm()
	return render(A,E,C)
def tags_update(request,uuid):
	A=request;C={};D=get_site_id(A);G=get_template(D,is_frontend=_B)+_P;E=Tags.objects.filter(site_id=D,uuid=uuid);F=get_object_or_404(E)
	if A.method==_F:
		H=TagsForm(A.POST,instance=F)
		if H.is_valid():I=A.POST.get(_Q);B=E.get();B.set_current_language(I);B.name=A.POST.get(_A);B.save();messages.info(A,mMsgBox.get(_R,A.POST.get(_A)));return redirect(reverse_lazy(_H))
	else:messages.info(A,mMsgBox.get(_S));C[_D]=TagsForm(instance=F)
	return render(A,G,C)
def tags_delete(request,uuid):A=request;F={};C=get_site_id(A);D=Tags.objects.filter(site_id=C,uuid=uuid);B=get_object_or_404(D);E=B.name;B.delete();messages.info(A,mMsgBox.get(_T,E));return redirect(reverse_lazy(_H))
class LogoView(TemplateView):
	site_id=_C
	def get(A,request,*C,**D):B=request;A.site_id=get_site_id(B);E=get_template(A.site_id,is_frontend=_B);A.template_name=E+'logo.html';return super(LogoView,A).get(B,*(C),**D)
	def get_context_data(A,*B,**C):D=super(LogoView,A).get_context_data(*(B),**C);return D
def logo_ajax(request):
	E=get_site_id(request);C=Subquery(Photo.objects.filter(object_id=OuterRef(_E),content_type__model=_G).values('file_path'));F=Logo.objects.filter(site_id=E).distinct().annotate(file_path=C).annotate(jml=Count(C));D=[]
	for B in F:A={};A['icon']=_C;A['uuid']=B.uuid;A[_I]=B.updated_at;A['Name']=Truncator(B.name).chars(20);A['Jumlah Foto']=B.jml;A['Foto']=B.file_path;A[_J]=get_natural_datetime(B.updated_at);A[_K]=_C;D.append(A)
	return JsonResponse(D,safe=_B)
def logo_create(request):
	E='str_file_path';D='photo';A=request;B={};F=get_site_id(A);G=get_template(F,is_frontend=_B)+_L
	if A.method==_F:
		C=LogoForm(A.POST);J=PhotoForm(A.POST)
		if C.is_valid():
			H=Logo.objects.filter(name=A.POST.get(_A))
			if H:messages.info(A,mMsgBox.get(_M));B[_D]=LogoForm();B[D]=PhotoForm()
			else:I=C.save();print('file path = ',A.POST.get(E));Photo.objects.create(content_object=I,file_path=A.POST.get(E));print('done...');messages.info(A,mMsgBox.get(_N,A.POST.get(_A)));return redirect(reverse_lazy(_G))
	else:messages.info(A,mMsgBox.get(_O));B[_D]=LogoForm();B[D]=PhotoForm()
	return render(A,G,B)
def logo_update(request,uuid):
	A=request;C={};D=get_site_id(A);G=get_template(D,is_frontend=_B)+_P;E=Logo.objects.filter(site_id=D,uuid=uuid);F=get_object_or_404(E)
	if A.method==_F:
		H=LogoForm(A.POST,instance=F)
		if H.is_valid():I=A.POST.get(_Q);B=E.get();B.set_current_language(I);B.name=A.POST.get(_A);B.save();messages.info(A,mMsgBox.get(_R,A.POST.get(_A)));return redirect(reverse_lazy(_G))
	else:messages.info(A,mMsgBox.get(_S));C[_D]=LogoForm(instance=F)
	return render(A,G,C)
def logo_delete(request,uuid):A=request;F={};C=get_site_id(A);D=Logo.objects.filter(site_id=C,uuid=uuid);B=get_object_or_404(D);E=B.name;B.delete();messages.info(A,mMsgBox.get(_T,E));return redirect(reverse_lazy(_G))