_AJ='site name updated'
_AI='is_external'
_AH='is_visibled'
_AG='order_menu'
_AF='file_path = '
_AE='phone'
_AD='email'
_AC='select2_menu'
_AB='designation'
_AA='location'
_A9='one_record_only'
_A8='notes'
_A7='address'
_A6='file_path_doc'
_A5='Link'
_A4='Name (en)'
_A3='Name (id)'
_A2='document'
_A1='related_link'
_A0='video_gallery'
_z='photo_gallery'
_y='social_media'
_x='alert'
_w='daily_alert'
_v='form not valid '
_u='slide_show'
_t='banner'
_s='agency'
_r='menu'
_q='pages'
_p='greeting'
_o='events'
_n='article'
_m='news'
_l='Content (en)'
_k='Content (id)'
_j='announcement'
_i='logo'
_h='Jumlah Foto'
_g='link'
_f='Title (en)'
_e='Title (id)'
_d='Foto'
_c='file_path'
_b='language'
_a='categories'
_Z='tags'
_Y='Update'
_X='delete'
_W='form_edit'
_V='save_edit'
_U='update.html'
_T='form_add'
_S='save_add'
_R='create.html'
_Q='Action'
_P='updated_at'
_O='uuid'
_N='icon'
_M='photo'
_L='status'
_K='str_file_path'
_J='content'
_I='en'
_H='POST'
_G='name'
_F='form'
_E='title'
_D='active_page'
_C=None
_B=False
_A='id'
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
from education.models import *
from core.models import Photo,Agency,AgencyTranslation,Service
from parler.utils.context import switch_language
from parler.views import TranslatableCreateView,TranslatableUpdateView
from django.contrib.sites.models import Site
from parler.utils import get_active_language_choices
from parler.utils.conf import LanguagesSetting
from django.http import Http404
from menu.models import *
from menu.menus import Menus
from .forms import *
from core.forms import PhotoForm
from core.views import download_image
mMsgBox=msgbox.ClsMsgBox()
def save_tags(tag_list,obj_master):
	i=0
	while i<len(tag_list):tag=Tags.objects.get(id=tag_list[i]);obj_master.tags.add(tag);i+=1
class IndexView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);print('template = ',template);self.template_name=template+'index.html';return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(IndexView,self).get_context_data(*(args),**kwargs);context[_D]='dashboard';return context
class TagsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'tags.html';return super(TagsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(TagsView,self).get_context_data(*(args),**kwargs);context[_D]=_Z;return context
def tags_ajax(request):
	site_id=get_site_id(request);obj=Tags();obj.set_current_language(_I);subquery=Subquery(TagsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));lang=obj.get_current_language();obj2=Tags.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery);lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_A3]=Truncator(i.name_id).chars(20);res[_A4]=Truncator(i.name).chars(20);res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def tags_create(request):
	context={};context[_D]=_Z;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=TagsForm(request.POST)
		if form.is_valid():
			tmp=Tags.objects.filter(translations__name=request.POST.get(_G))
			if tmp:messages.info(request,mMsgBox.get('file_exists'));context[_F]=TagsForm()
			else:post=Tags.objects.language(_A).create(name=request.POST.get(_G));post.set_current_language(_I);post.name=request.POST.get(_G);post.save();messages.info(request,mMsgBox.get(_S,request.POST.get(_G)));return redirect(reverse_lazy(_Z))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=TagsForm()
	return render(request,template,context)
def tags_update(request,uuid):
	context={};context[_D]=_Z;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=TagsForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_G);obj.save();messages.info(request,mMsgBox.get(_V,request.POST.get(_G)));return redirect(reverse_lazy(_Z))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=TagsForm(instance=post)
	return render(request,template,context)
def tags_delete(request,uuid):context={};site_id=get_site_id(request);data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_Z))
class LogoView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'logo.html';return super(LogoView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(LogoView,self).get_context_data(*(args),**kwargs);context[_A9]=True;context[_D]=_i;return context
def logo_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_i).values(_c)[:1]);obj2=Logo.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery).annotate(jml=Count(subquery));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res['Name']=Truncator(i.name).chars(20);res[_h]=i.jml;res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def logo_create(request):
	context={};context[_D]=_i;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=LogoForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=form.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_K));messages.info(request,mMsgBox.get(_S,request.POST.get(_G)));return redirect(reverse_lazy(_i))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=LogoForm();context[_M]=PhotoForm()
	return render(request,template,context)
def logo_update(request,uuid):
	context={};context[_D]=_i;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_H:
		form=LogoForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save()
			if request.POST.get(_K):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_K));print('DOne')
			messages.info(request,mMsgBox.get(_V,request.POST.get(_G)));return redirect(reverse_lazy(_i))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=LogoForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def logo_delete(request,uuid):context={};site_id=get_site_id(request);data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_i))
class AnnouncementView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'announcement.html';return super(AnnouncementView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(AnnouncementView,self).get_context_data(*(args),**kwargs);context[_D]=_j;return context
def announcement_ajax(request):
	site_id=get_site_id(request);obj=Announcement();obj.set_current_language(_I);subquery1=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_j).values(_c)[:1]);lang=obj.get_current_language();obj2=Announcement.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_k]=Truncator(i.content_id).chars(20);res[_l]=Truncator(i.content).chars(20);res[_h]=i.jml;res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def announcement_create(request):
	context={};context[_D]=_j;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=AnnouncementForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Announcement.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_J),categories_id=request.POST.get(_a),priority=request.POST.get('priority'),status=request.POST.get(_L));post.set_current_language(_I);post.title=request.POST.get(_E);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_K));messages.info(request,mMsgBox.get(_S,request.POST.get(_E)));return redirect(reverse_lazy(_j))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=AnnouncementForm();context[_M]=PhotoForm()
	return render(request,template,context)
def announcement_update(request,uuid):
	context={};context[_D]=_j;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_H:
		form=AnnouncementForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_J);obj.categories_id=request.POST.get(_a);obj.status=request.POST.get(_L);obj.priority=request.POST.get('priority');obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
			if photo.is_valid():
				if request.POST.get(_K):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_K))
			messages.info(request,mMsgBox.get(_V,request.POST.get(_E)));return redirect(reverse_lazy(_j))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=AnnouncementForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def announcement_delete(request,uuid):context={};site_id=get_site_id(request);data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_j))
class NewsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'news.html';return super(NewsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(NewsView,self).get_context_data(*(args),**kwargs);context[_D]=_m;return context
def news_ajax(request):
	site_id=get_site_id(request);obj=News();obj.set_current_language(_I);subquery1=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_m).values(_c)[:1]);lang=obj.get_current_language();obj2=News.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_k]=Truncator(i.content_id).chars(20);res[_l]=Truncator(i.content).chars(20);res[_h]=i.jml;res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def news_create(request):
	context={};context[_D]=_m;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=NewsForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=News.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_J),categories_id=request.POST.get(_a),status=request.POST.get(_L));post.set_current_language(_I);post.title=request.POST.get(_E);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_K));messages.info(request,mMsgBox.get(_S,request.POST.get(_E)));return redirect(reverse_lazy(_m))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=NewsForm();context[_M]=PhotoForm()
	return render(request,template,context)
def news_update(request,uuid):
	context={};context[_D]=_m;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_H:
		form=NewsForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_J);obj.categories_id=request.POST.get(_a);obj.status=request.POST.get(_L);obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
			if photo.is_valid():
				if request.POST.get(_K):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_K))
			messages.info(request,mMsgBox.get(_V,request.POST.get(_E)));return redirect(reverse_lazy(_m))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=NewsForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def news_delete(request,uuid):context={};site_id=get_site_id(request);data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_m))
class ArticleView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'article.html';return super(ArticleView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(ArticleView,self).get_context_data(*(args),**kwargs);context[_D]=_n;return context
def article_ajax(request):
	site_id=get_site_id(request);obj=Article();obj.set_current_language(_I);subquery1=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_n).values(_c)[:1]);lang=obj.get_current_language();obj2=Article.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_k]=Truncator(i.content_id).chars(20);res[_l]=Truncator(i.content).chars(20);res[_h]=i.jml;res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def article_create(request):
	context={};context[_D]=_n;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=ArticleForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Article.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_J),categories_id=request.POST.get(_a),status=request.POST.get(_L));post.set_current_language(_I);post.title=request.POST.get(_E);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_K));messages.info(request,mMsgBox.get(_S,request.POST.get(_E)));return redirect(reverse_lazy(_n))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=ArticleForm();context[_M]=PhotoForm()
	return render(request,template,context)
def article_update(request,uuid):
	context={};context[_D]=_n;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_H:
		form=ArticleForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_J);obj.categories_id=request.POST.get(_a);obj.status=request.POST.get(_L);obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
			if photo.is_valid():
				if request.POST.get(_K):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_K))
			messages.info(request,mMsgBox.get(_V,request.POST.get(_E)));return redirect(reverse_lazy(_n))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=ArticleForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def article_delete(request,uuid):context={};site_id=get_site_id(request);data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_n))
class EventsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'events.html';return super(EventsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(EventsView,self).get_context_data(*(args),**kwargs);context[_D]=_o;return context
def events_ajax(request):
	site_id=get_site_id(request);obj=Events();obj.set_current_language(_I);subquery1=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_o).values(_c)[:1]);lang=obj.get_current_language();obj2=Events.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_k]=Truncator(i.content_id).chars(20);res[_l]=Truncator(i.content).chars(20);res[_h]=i.jml;res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def events_create(request):
	context={};context[_D]=_o;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=EventsForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Events.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_J),location=request.POST.get(_AA),categories_id=request.POST.get(_a),status=request.POST.get(_L),date=request.POST.get('date'),time=request.POST.get('time'));post.set_current_language(_I);post.title=request.POST.get(_E);post.content=request.POST.get(_J);post.location=request.POST.get(_AA);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_K));messages.info(request,mMsgBox.get(_S,request.POST.get(_E)));return redirect(reverse_lazy(_o))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=EventsForm();context[_M]=PhotoForm()
	return render(request,template,context)
def events_update(request,uuid):
	context={};context[_D]=_o;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_H:
		form=EventsForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_J);obj.location=request.POST.get(_AA);obj.categories_id=request.POST.get(_a);obj.status=request.POST.get(_L);obj.date=request.POST.get('date');obj.time=request.POST.get('time');obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
			if photo.is_valid():
				if request.POST.get(_K):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_K))
			messages.info(request,mMsgBox.get(_V,request.POST.get(_E)));return redirect(reverse_lazy(_o))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=EventsForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def events_delete(request,uuid):context={};site_id=get_site_id(request);data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_o))
class SlideShowView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'slide_show.html';return super(SlideShowView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SlideShowView,self).get_context_data(*(args),**kwargs);context[_D]=_u;return context
def slideshow_ajax(request):
	site_id=get_site_id(request);lst=[];obj=SlideShow();obj.set_current_language(_I);subquery1=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model='slideshow').values(_c)[:1]);lang=obj.get_current_language();obj2=SlideShow.objects.language(lang).filter(site_id=site_id).distinct().annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_k]=Truncator(i.content_id).chars(20);res[_l]=Truncator(i.content).chars(20);res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def slideshow_create(request):
	context={};context[_D]=_u;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=SlideShowForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=SlideShow.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_J),status=request.POST.get(_L));post.set_current_language(_I);post.title=request.POST.get(_E);post.content=request.POST.get(_J);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_K));messages.info(request,mMsgBox.get(_S,request.POST.get(_E)));return redirect(reverse_lazy(_u))
		else:print(_v);context[_F]=SlideShowForm();context[_M]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_T));context[_F]=SlideShowForm();context[_M]=PhotoForm()
	return render(request,template,context)
def slideshow_update(request,uuid):
	context={};context[_D]=_u;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.first()
	if request.method==_H:
		form=SlideShowForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_J);obj.status=request.POST.get(_L);obj.save()
			if request.POST.get(_K):obj.photo.clear();Photo.objects.create(content_object=obj,file_path=request.POST.get(_K))
			else:print('photo not valid')
			messages.info(request,mMsgBox.get(_V,request.POST.get(_E)));return redirect(reverse_lazy(_u))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=SlideShowForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def slideshow_delete(request,uuid):context={};site_id=get_site_id(request);data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_u))
class DailyAlertView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'daily_alert.html';return super(DailyAlertView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DailyAlertView,self).get_context_data(*(args),**kwargs);context[_D]=_w;return context
def dailyalert_ajax(request):
	site_id=get_site_id(request);lst=[];obj=DailyAlert();obj.set_current_language(_I);subquery1=Subquery(DailyAlertTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_x));lang=obj.get_current_language();obj2=DailyAlert.objects.language(lang).filter(site_id=site_id).annotate(alert_id=subquery1)
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res['Alert (id)']=Truncator(i.alert_id).chars(20);res['Alert (en)']=Truncator(i.alert).chars(20);res[_A5]=Truncator(i.link).chars(20);res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def dailyalert_create(request):
	context={};context[_D]=_w;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=DailyAlertForm(request.POST)
		if form.is_valid():post=DailyAlert.objects.language(_A).create(alert=request.POST.get(_x),link=request.POST.get(_g),status=request.POST.get(_L));post.set_current_language(_I);post.alert=request.POST.get(_x);post.save();messages.info(request,mMsgBox.get(_S,request.POST.get(_x)));return redirect(reverse_lazy(_w))
		else:print(_v);context[_F]=DailyAlertForm()
	else:messages.info(request,mMsgBox.get(_T));context[_F]=DailyAlertForm()
	return render(request,template,context)
def dailyalert_update(request,uuid):
	context={};context[_D]=_w;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=DailyAlertForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.alert=request.POST.get(_x);obj.link=request.POST.get(_g);obj.status=request.POST.get(_L);obj.save();messages.info(request,mMsgBox.get(_V,request.POST.get(_x)));return redirect(reverse_lazy(_w))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=DailyAlertForm(instance=post)
	return render(request,template,context)
def dailyalert_delete(request,uuid):context={};site_id=get_site_id(request);data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.alert;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_w))
class GreetingView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'greeting.html';return super(GreetingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(GreetingView,self).get_context_data(*(args),**kwargs);context[_A9]=True;context[_D]=_p;return context
def greeting_ajax(request):
	site_id=get_site_id(request);obj=Greeting();obj.set_current_language(_I);subquery1=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_p).values(_c)[:1]);lang=obj.get_current_language();obj2=Greeting.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_k]=Truncator(i.content_id).chars(20);res[_l]=Truncator(i.content).chars(20);res[_h]=i.jml;res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def greeting_create(request):
	context={};context[_D]=_p;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=GreetingForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Greeting.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_J),name=request.POST.get(_G),designation=request.POST.get(_AB),status=request.POST.get(_L));post.set_current_language(_I);post.title=request.POST.get(_E);post.content=request.POST.get(_J);post.name=request.POST.get(_G);post.designation=request.POST.get(_AB);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_K));messages.info(request,mMsgBox.get(_S,request.POST.get(_E)));return redirect(reverse_lazy(_p))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=GreetingForm();context[_M]=PhotoForm()
	return render(request,template,context)
def greeting_update(request,uuid):
	context={};context[_D]=_p;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_H:
		form=GreetingForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_J);obj.name=request.POST.get(_G);obj.designation=request.POST.get(_AB);obj.status=request.POST.get(_L);obj.save()
			if photo.is_valid():
				if request.POST.get(_K):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_K))
			messages.info(request,mMsgBox.get(_V,request.POST.get(_E)));return redirect(reverse_lazy(_p))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=GreetingForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def greeting_delete(request,uuid):context={};site_id=get_site_id(request);data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_p))
class PagesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'pages.html';return super(PagesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PagesView,self).get_context_data(*(args),**kwargs);context[_D]=_q;return context
def pages_ajax(request):
	site_id=get_site_id(request);obj=Pages();obj.set_current_language(_I);subquery1=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_q).values(_c)[:1]);lang=obj.get_current_language();obj2=Pages.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_k]=Truncator(i.content_id).chars(20);res[_l]=Truncator(i.content).chars(20);res[_h]=i.jml;res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def menu_already_used(site_id,menu_id):
	A='translations__title';lang=get_active_language_choices()[0];pages=Pages.objects.language(lang).filter(site_id=site_id,menu_id=menu_id).values(A)
	if pages:return pages[0][A]
	return _C
def pages_create(request):
	A='fail_add';context={};context[_D]=_q;context['select2']='Access From Menu';site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=PagesForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			menu_id=request.POST.get(_AC)
			if menu_id:
				menu_name_already_used=menu_already_used(site_id,menu_id)
				if not menu_name_already_used:post=Pages.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_J),menu_id=menu_id,status=request.POST.get(_L));post.set_current_language(_I);post.title=request.POST.get(_E);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_K));obj=Menu.objects.get(id=menu_id);obj.link='/pages/detail/'+post.slug;obj.save();messages.info(request,mMsgBox.get(_S,request.POST.get(_E)));return redirect(reverse_lazy(_q))
				else:messages.info(request,mMsgBox.get(A,'Menu already used by '+menu_name_already_used));context[_F]=PagesForm(request.POST);context[_M]=PhotoForm(request.POST)
			else:messages.info(request,mMsgBox.get(A,'Access From Menu cannot empty!'));context[_F]=PagesForm(request.POST);context[_M]=PhotoForm(request.POST)
	else:messages.info(request,mMsgBox.get(_T));context[_F]=PagesForm();context[_M]=PhotoForm()
	return render(request,template,context)
def pages_update(request,uuid):
	context={};context[_D]=_q;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_H:
		form=PagesForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_J);obj.menu_id=request.POST.get(_r);obj.status=request.POST.get(_L);obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
			if photo.is_valid():
				if request.POST.get(_K):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_K))
			messages.info(request,mMsgBox.get(_V,request.POST.get(_E)));return redirect(reverse_lazy(_q))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=PagesForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def pages_delete(request,uuid):context={};site_id=get_site_id(request);data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_q))
class SocialMediaView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'social_media.html';return super(SocialMediaView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SocialMediaView,self).get_context_data(*(args),**kwargs);context[_D]=_y;return context
def socialmedia_ajax(request):
	site_id=get_site_id(request);obj2=SocialMedia.objects.filter(site_id=site_id);lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res['Kind']=i.kind;res[_A5]=Truncator(i.link).chars(30);res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def socialmedia_create(request):
	context={};context[_D]=_y;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=SocialMediaForm(request.POST)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_S,request.POST.get(_g)));return redirect(reverse_lazy(_y))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=SocialMediaForm()
	return render(request,template,context)
def socialmedia_update(request,uuid):
	context={};context[_D]=_y;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=SocialMediaForm(request.POST,instance=post)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_V,request.POST.get(_g)));return redirect(reverse_lazy(_y))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=SocialMediaForm(instance=post)
	return render(request,template,context)
def socialmedia_delete(request,uuid):context={};site_id=get_site_id(request);data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.link;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_y))
class PhotoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'photo_gallery.html';return super(PhotoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PhotoGalleryView,self).get_context_data(*(args),**kwargs);context[_D]=_z;return context
def photogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=PhotoGallery();obj.set_current_language(_I);subquery1=Subquery(PhotoGalleryTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model='photogallery').values(_c)[:1]);lang=obj.get_current_language();obj2=PhotoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto))
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_h]=i.jml;res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def photogallery_create(request):
	context={};context[_D]=_z;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=PhotoGalleryForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=PhotoGallery.objects.language(_A).create(title=request.POST.get(_E),status=request.POST.get(_L));post.set_current_language(_I);post.title=request.POST.get(_E);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_K));messages.info(request,mMsgBox.get(_S,request.POST.get(_E)));return redirect(reverse_lazy(_z))
		else:print(_v);context[_F]=PhotoGalleryForm();context[_M]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_T));context[_F]=PhotoGalleryForm();context[_M]=PhotoForm()
	return render(request,template,context)
def photogallery_update(request,uuid):
	context={};context[_D]=_z;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_H:
		form=PhotoGalleryForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.status=request.POST.get(_L);obj.save()
			if photo.is_valid():
				if request.POST.get(_K):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_K))
			messages.info(request,mMsgBox.get(_V,request.POST.get(_E)));return redirect(reverse_lazy(_z))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=PhotoGalleryForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def photogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_z))
def get_video_id(url_video):
	tmp=url_video.split('/')
	if tmp:return tmp[len(tmp)-1]
def download_thumbnail(request,video_id):download_url='https://img.youtube.com/vi/'+video_id+'/mqdefault.jpg';return download_image(request,download_url)
class VideoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'video_gallery.html';return super(VideoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(VideoGalleryView,self).get_context_data(*(args),**kwargs);context[_D]=_A0;return context
def videogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=VideoGallery();obj.set_current_language(_I);subquery1=Subquery(VideoGalleryTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));lang=obj.get_current_language();obj2=VideoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1)
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res['Embed']=Truncator(i.embed).chars(30);res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def videogallery_create(request):
	context={};context[_D]=_A0;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=VideoGalleryForm(request.POST)
		if form.is_valid():post=VideoGallery.objects.language(_A).create(title=request.POST.get(_E),embed=request.POST.get('embed'),status=request.POST.get(_L));post.set_current_language(_I);post.title=request.POST.get(_E);post.save();video_id=get_video_id(post.embed_video);file_path=download_thumbnail(request,video_id);Photo.objects.create(content_object=post,file_path=file_path);messages.info(request,mMsgBox.get(_S,request.POST.get(_E)));return redirect(reverse_lazy(_A0))
		else:print(_v);context[_F]=VideoGalleryForm()
	else:messages.info(request,mMsgBox.get(_T));context[_F]=VideoGalleryForm()
	return render(request,template,context)
def videogallery_update(request,uuid):
	context={};context[_D]=_A0;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=VideoGalleryForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.embed=request.POST.get('embed');obj.status=request.POST.get(_L);obj.save();print('data = ');print(obj);print(post);video_id=get_video_id(obj.embed_video);file_path=download_thumbnail(request,video_id);obj.photo.clear();Photo.objects.create(content_object=obj,file_path=file_path);messages.info(request,mMsgBox.get(_V,request.POST.get(_E)));return redirect(reverse_lazy(_A0))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=VideoGalleryForm(instance=post)
	return render(request,template,context)
def videogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_A0))
class RelatedLinkView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'related_link.html';return super(RelatedLinkView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(RelatedLinkView,self).get_context_data(*(args),**kwargs);context[_D]=_A1;return context
def relatedlink_ajax(request):
	site_id=get_site_id(request);lst=[];obj=RelatedLink();obj.set_current_language(_I);subquery1=Subquery(RelatedLinkTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));lang=obj.get_current_language();obj2=RelatedLink.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1)
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_A3]=Truncator(i.name_id).chars(20);res[_A4]=Truncator(i.name).chars(20);res[_A5]=Truncator(i.link).chars(30);res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def relatedlink_create(request):
	context={};context[_D]=_A1;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=RelatedLinkForm(request.POST)
		if form.is_valid():post=RelatedLink.objects.language(_A).create(name=request.POST.get(_G),link=request.POST.get(_g),status=request.POST.get(_L));post.set_current_language(_I);post.name=request.POST.get(_G);post.save();messages.info(request,mMsgBox.get(_S,request.POST.get(_G)));return redirect(reverse_lazy(_A1))
		else:print(_v);context[_F]=RelatedLinkForm()
	else:messages.info(request,mMsgBox.get(_T));context[_F]=RelatedLinkForm()
	return render(request,template,context)
def relatedlink_update(request,uuid):
	context={};context[_D]=_A1;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=RelatedLinkForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_G);obj.link=request.POST.get(_g);obj.status=request.POST.get(_L);obj.save();messages.info(request,mMsgBox.get(_V,request.POST.get(_G)));return redirect(reverse_lazy(_A1))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=RelatedLinkForm(instance=post)
	return render(request,template,context)
def relatedlink_delete(request,uuid):context={};site_id=get_site_id(request);data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_A1))
class DocumentView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'document.html';return super(DocumentView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DocumentView,self).get_context_data(*(args),**kwargs);context[_D]=_A2;return context
def document_ajax(request):
	site_id=get_site_id(request);lst=[];obj=Document();obj.set_current_language(_I);subquery1=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery2=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));lang=obj.get_current_language();obj2=Document.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1).annotate(content_id=subquery2)
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_A3]=Truncator(i.name_id).chars(20);res[_A4]=Truncator(i.name).chars(20);res['content (id)']=Truncator(i.content_id).chars(30);res['content (en)']=Truncator(i.content).chars(30);res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def document_create(request):
	context={};context[_D]=_A2;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=DocumentForm(request.POST,request.FILES);print('form=',form)
		if form.is_valid():print('categories = ',request.POST.get(_a));print('file = ',request.FILES.get(_A6));post=Document.objects.language(_A).create(name=request.POST.get(_G),content=request.POST.get(_J),file_path_doc=request.FILES.get(_A6),categories_id=request.POST.get(_a),status=request.POST.get(_L));post.set_current_language(_I);post.name=request.POST.get(_G);post.content=request.POST.get(_J);post.save();print(_AF,post.file_path_doc.path);post.size=os.stat(post.file_path_doc.path).st_size;post.save();messages.info(request,mMsgBox.get(_S,request.POST.get(_G)));return redirect(reverse_lazy(_A2))
		else:messages.info(request,mMsgBox.get('form_fail'));context[_F]=DocumentForm()
	else:messages.info(request,mMsgBox.get(_T));context[_F]=DocumentForm()
	return render(request,template,context)
def document_update(request,uuid):
	context={};context[_D]=_A2;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=DocumentForm(request.POST,request.FILES,instance=post)
		if form.is_valid():
			lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_G);obj.content=request.POST.get(_J)
			if request.FILES.get(_A6):obj.file_path_doc=request.FILES.get(_A6)
			obj.status=request.POST.get(_L);obj.categories_id=request.POST.get(_a);obj.save();print(_AF,obj.file_path_doc.path);obj.size=os.stat(obj.file_path_doc.path).st_size;obj.save();messages.info(request,mMsgBox.get(_V,request.POST.get(_G)));return redirect(reverse_lazy(_A2))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=DocumentForm(instance=post)
	return render(request,template,context)
def document_delete(request,uuid):context={};site_id=get_site_id(request);data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_A2))
class MenuView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'menu.html';return super(MenuView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(MenuView,self).get_context_data(*(args),**kwargs);context[_D]=_r;return context
def get_menu_group(site_id):
	A='Frontend Site ';site_name=Site.objects.get(pk=site_id).domain;menugroup=MenuGroup.objects.filter(site=site_id,kind=1);print('menugroup = ',menugroup)
	if menugroup:return menugroup[0].id
	else:
		lang1=get_active_language_choices()[0];lang2=_A
		if lang1==_A:lang2=_I
		post=MenuGroup.objects.language(lang1).create(site_id=site_id,kind=1,name=A+site_name);post.set_current_language(lang2);post.name=A+site_name;post.save();return post.id
def menu_ajax(request):
	A='Name (';site_id=get_site_id(request);group_id=get_menu_group(site_id);print('group_id = ',group_id);lst=[]
	if group_id:
		lang=get_active_language_choices()[0];lang2=_A
		if lang==_A:lang2=_I
		menu=Menus(menu_group=group_id,kinds=1,site_id=site_id)
		if menu:
			obj2=menu.get_menus();print(obj2)
			for i in obj2:
				tmp='';lvl=i['level']
				while lvl>0:tmp+='<i class="fa fa-long-arrow-right"></i> &nbsp;&nbsp;&nbsp;&nbsp; ';lvl-=1
				res={};res[_N]=_C;res[_O]=i[_O];res[_P]=_C;res[A+lang+')']=Truncator(i[_G]).chars(20);res[A+lang2+')']=Menu.objects.language(lang2).get(pk=i[_A]).name;res['Tree']=tmp+Truncator(i[_G]).chars(20);res[_A5]=Truncator(i[_g]).chars(30);res['Icon']=Truncator(i[_N]).chars(30);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def menu_create(request):
	context={};context[_D]=_r;context['select2']='Parent Menu';site_id=get_site_id(request);group_id=get_menu_group(site_id);menu_group=MenuGroup.objects.get(id=group_id);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=MenuForm(request.POST)
		if form.is_valid():form_clean=form.cleaned_data;print('select2_menu = ',request.POST.get(_AC));post=Menu.objects.language(_A).create(name=form_clean[_G],parent_id=request.POST.get(_AC),link=form_clean[_g],order_menu=form_clean[_AG],icon=form_clean[_N],is_visibled=form_clean[_AH],is_external=form_clean[_AI]);post.menu_group.add(menu_group);post.set_current_language(_I);post.name=form_clean[_G];post.save();messages.info(request,mMsgBox.get(_S,request.POST.get(_G)));return redirect(reverse_lazy(_r))
		else:print(_v);context[_F]=MenuForm()
	else:messages.info(request,mMsgBox.get(_T));context[_F]=MenuForm()
	return render(request,template,context)
def menu_update(request,uuid):
	context={};context[_D]=_r;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Menu.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=MenuForm(request.POST,instance=post)
		if form.is_valid():form_clean=form.cleaned_data;print(form_clean);lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.name=form_clean[_G];obj.parent_id=request.POST.get('parent');obj.link=form_clean[_g];obj.order_menu=form_clean[_AG];obj.icon=form_clean[_N];obj.is_visibled=form_clean[_AH];obj.is_external=form_clean[_AI];obj.save();messages.info(request,mMsgBox.get(_V,request.POST.get(_G)));return redirect(reverse_lazy(_r))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=MenuForm(instance=post)
	return render(request,template,context)
def menu_delete(request,uuid):context={};site_id=get_site_id(request);data=Menu.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_r))
def site_name_update(site_id,name):site=Site.objects.get(id=site_id);site.name=name;site.save()
class AgencyView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'agency.html';return super(AgencyView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(AgencyView,self).get_context_data(*(args),**kwargs);context[_D]=_s;context[_A9]=True;return context
def agency_ajax(request):
	site_id=get_site_id(request);obj=Agency();obj.set_current_language(_I);service=Service.objects.filter(site_id=site_id).values_list(_s,flat=True);subquery1=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_A7));subquery2=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_A8));lang=obj.get_current_language();obj2=Agency.objects.language(lang).filter(id=service[0]).annotate(address_id=subquery1).annotate(notes_id=subquery2);lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res['Name']=Truncator(i.name).chars(20);res['Address (id)']=Truncator(i.address_id).chars(20);res['Address (en)']=Truncator(i.address).chars(20);res['Description (id)']=Truncator(i.notes_id).chars(20);res['Description (en)']=Truncator(i.notes).chars(20);res[_AD]=i.email;res[_AE]=i.phone;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def agency_create(request):
	context={};context[_D]=_s;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=AgencyForm(request.POST)
		if form.is_valid():post=Agency.objects.language(_A).create(address=request.POST.get(_A7),notes=request.POST.get(_A8),name=request.POST.get(_G),email=request.POST.get(_AD),phone=request.POST.get(_AE),fax=request.POST.get('fax'),whatsapp=request.POST.get('whatsapp'),status=request.POST.get(_L));post.set_current_language(_I);post.address=request.POST.get(_A7);post.notes=request.POST.get(_A8);post.save();site_name_update(site_id,request.POST.get(_G));print(_AJ);messages.info(request,mMsgBox.get(_S,request.POST.get(_G)));return redirect(reverse_lazy(_s))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=AgencyForm()
	return render(request,template,context)
def agency_update(request,uuid):
	context={};context[_D]=_s;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=AgencyForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.address=request.POST.get(_A7);obj.notes=request.POST.get(_A8);obj.name=request.POST.get(_G);obj.email=request.POST.get(_AD);obj.phone=request.POST.get(_AE);obj.fax=request.POST.get('fax');obj.whatsapp=request.POST.get('whatsapp');obj.status=request.POST.get(_L);obj.save();print('site name begin update');site_name_update(site_id,request.POST.get(_G));print(_AJ);messages.info(request,mMsgBox.get(_V,request.POST.get(_G)));return redirect(reverse_lazy(_s))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=AgencyForm(instance=post)
	return render(request,template,context)
def agency_delete(request,uuid):context={};site_id=get_site_id(request);data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_s))
class CategoriesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'categories.html';return super(CategoriesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(CategoriesView,self).get_context_data(*(args),**kwargs);context[_D]=_a;return context
def categories_ajax(request):
	site_id=get_site_id(request);obj=Categories();obj.set_current_language(_I);subquery1=Subquery(CategoriesTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));lang=obj.get_current_language();obj2=Categories.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1);lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_A3]=Truncator(i.name_id).chars(20);res[_A4]=Truncator(i.name).chars(20);res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def categories_create(request):
	context={};context[_D]=_a;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=CategoriesForm(request.POST)
		if form.is_valid():post=Categories.objects.language(_A).create(name=request.POST.get(_G));post.set_current_language(_I);post.name=request.POST.get(_G);post.save();messages.info(request,mMsgBox.get(_S,request.POST.get(_G)));return redirect(reverse_lazy(_a))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=CategoriesForm()
	return render(request,template,context)
def categories_update(request,uuid):
	context={};context[_D]=_a;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=CategoriesForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_b);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_G);obj.save();messages.info(request,mMsgBox.get(_V,request.POST.get(_G)));return redirect(reverse_lazy(_a))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=CategoriesForm(instance=post)
	return render(request,template,context)
def categories_delete(request,uuid):context={};site_id=get_site_id(request);data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_a))
def menu_lookup_ajax(request):
	A='translations__name';lang=get_active_language_choices()[0];site_id=get_site_id(request);group_id=get_menu_group(site_id);print('menugroup=',group_id,lang);search=request.GET.get('search')
	if search:object_list=Menu.objects.translated(lang).filter(menu_group__id=group_id).filter(translations__name__icontains=search).values(_A,text=F(A))
	else:object_list=Menu.objects.translated(lang).filter(menu_group__id=group_id).values(_A,text=F(A))
	return JsonResponse({'results':list(object_list),'pagination':{'more':True}},safe=_B)
class BannerView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'banner.html';return super(BannerView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(BannerView,self).get_context_data(*(args),**kwargs);context[_D]=_t;return context
def banner_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_t).values(_c));obj2=Banner.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery);lst=[]
	for i in obj2:
		res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at
		if i.position==1:pos='TOP'
		elif i.position==2:pos='MIDDLE TOP'
		elif i.position==3:pos='MIDDLE BOTTOM'
		elif i.position==4:pos='BOTTOM'
		else:pos='NOT DEFIND'
		res['Position']=pos;res[_d]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_Q]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def banner_create(request):
	context={};context[_D]=_t;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_R
	if request.method==_H:
		form=BannerForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=form.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_K));messages.info(request,mMsgBox.get(_S,request.POST.get('position')));return redirect(reverse_lazy(_t))
	else:messages.info(request,mMsgBox.get(_T));context[_F]=BannerForm();context[_M]=PhotoForm()
	return render(request,template,context)
def banner_update(request,uuid):
	context={};context[_D]=_t;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_U;data=Banner.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_H:
		form=BannerForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save()
			if request.POST.get(_K):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_K));print('DOne')
			messages.info(request,mMsgBox.get(_V,request.POST.get('position')));return redirect(reverse_lazy(_t))
	else:messages.info(request,mMsgBox.get(_W));context[_F]=BannerForm(instance=post);context[_M]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def banner_delete(request,uuid):context={};site_id=get_site_id(request);data=Banner.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.position;post.delete();messages.info(request,mMsgBox.get(_X,tmp));return redirect(reverse_lazy(_t))