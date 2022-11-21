_AH='file_path_doc'
_AG='file_exists'
_AF='phone'
_AE='email'
_AD='designation'
_AC='location'
_AB='one_record_only'
_AA='notes'
_A9='address'
_A8='Link'
_A7='Name (en)'
_A6='Name (id)'
_A5='tags.clear'
_A4='categories'
_A3='document'
_A2='relatedlink'
_A1='videogallery'
_A0='socialmedia'
_z='alert'
_y='dailyalert'
_x='form not valid '
_w='agency'
_v='photogallery'
_u='pages'
_t='greeting'
_s='slideshow'
_r='events'
_q='article'
_p='news'
_o='Content (en)'
_n='Content (id)'
_m='announcement'
_l='done...'
_k='file path = '
_j='logo'
_i='menu'
_h='link'
_g='update photo'
_f='Title (en)'
_e='Title (id)'
_d='DOne'
_c='Foto'
_b='Jumlah Foto'
_a='file_path'
_Z='language'
_Y='Update'
_X='tags'
_W='delete'
_V='form_edit'
_U='save_edit'
_T='update.html'
_S='form_add'
_R='save_add'
_Q='create.html'
_P='Action'
_O='updated_at'
_N='uuid'
_M='icon'
_L='photo'
_K='en'
_J='content'
_I='str_file_path'
_H='POST'
_G='title'
_F='form'
_E='active_page'
_D=None
_C='name'
_B='id'
_A=False
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
from menu.models import *
from menu.menus import Menus
from .forms import *
from core.forms import PhotoForm
mMsgBox=msgbox.ClsMsgBox()
def save_tags(tag_list,obj_master):
	i=0
	while i<len(tag_list):tag=Tags.objects.get(id=tag_list[i]);obj_master.tags.add(tag);i+=1
class IndexView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);print('template = ',template);self.template_name=template+'index.html';return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(IndexView,self).get_context_data(*(args),**kwargs);context[_E]='dashboard';return context
class TagsView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'tags.html';return super(TagsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(TagsView,self).get_context_data(*(args),**kwargs);context[_E]=_X;return context
def tags_ajax(request):
	site_id=get_site_id(request);obj=Tags();obj.set_current_language(_K);subquery=Subquery(TagsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_C));lang=obj.get_current_language();obj2=Tags.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery);lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_A6]=Truncator(i.name_id).chars(20);res[_A7]=Truncator(i.name).chars(20);res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def tags_create(request):
	context={};context[_E]=_X;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=TagsForm(request.POST)
		if form.is_valid():
			tmp=Tags.objects.filter(translations__name=request.POST.get(_C))
			if tmp:messages.info(request,mMsgBox.get(_AG));context[_F]=TagsForm()
			else:post=Tags.objects.language(_B).create(name=request.POST.get(_C));post.save();post.set_current_language(_K);post.name=request.POST.get(_C);post.save();messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_X))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=TagsForm()
	return render(request,template,context)
def tags_update(request,uuid):
	context={};context[_E]=_X;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=TagsForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_C);obj.save();messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_X))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=TagsForm(instance=post)
	return render(request,template,context)
def tags_delete(request,uuid):context={};site_id=get_site_id(request);data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_X))
class LogoView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'logo.html';return super(LogoView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(LogoView,self).get_context_data(*(args),**kwargs);context[_AB]=True;context[_E]=_j;return context
def logo_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_j).values(_a));obj2=Logo.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery).annotate(jml=Count(subquery));lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res['Name']=Truncator(i.name).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def logo_create(request):
	context={};context[_E]=_j;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=LogoForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			tmp=Logo.objects.filter(name=request.POST.get(_C))
			if tmp:messages.info(request,mMsgBox.get(_AG));context[_F]=LogoForm();context[_L]=PhotoForm()
			else:post=form.save();print(_k,request.POST.get(_I));Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_l);messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_j))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=LogoForm();context[_L]=PhotoForm()
	return render(request,template,context)
def logo_update(request,uuid):
	context={};context[_E]=_j;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_H:
		form=LogoForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save();print('update text')
			if photo.is_valid():
				if request.POST.get(_I):print(_g);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_d)
			messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_j))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=LogoForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def logo_delete(request,uuid):context={};site_id=get_site_id(request);data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_j))
class AnnouncementView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'announcement.html';return super(AnnouncementView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(AnnouncementView,self).get_context_data(*(args),**kwargs);context[_E]=_m;return context
def announcement_ajax(request):
	site_id=get_site_id(request);obj=Announcement();obj.set_current_language(_K);subquery1=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_G));subquery2=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_m).values(_a));lang=obj.get_current_language();obj2=Announcement.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_n]=Truncator(i.content_id).chars(20);res[_o]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def announcement_create(request):
	context={};context[_E]=_m;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=AnnouncementForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Announcement.objects.language(_B).create(title=request.POST.get(_G),content=request.POST.get(_J));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_X),post);print(_k,request.POST.get(_I));Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_l);messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_m))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=AnnouncementForm();context[_L]=PhotoForm()
	return render(request,template,context)
def announcement_update(request,uuid):
	context={};context[_E]=_m;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_H:
		form=AnnouncementForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.save();obj.tags.clear();print(_A5);save_tags(request.POST.getlist(_X),obj)
			if photo.is_valid():
				if request.POST.get(_I):print(_g);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_d)
			messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_m))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=AnnouncementForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def announcement_delete(request,uuid):context={};site_id=get_site_id(request);data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_m))
class NewsView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'news.html';return super(NewsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(NewsView,self).get_context_data(*(args),**kwargs);context[_E]=_p;return context
def news_ajax(request):
	site_id=get_site_id(request);obj=News();obj.set_current_language(_K);subquery1=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_G));subquery2=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_p).values(_a));lang=obj.get_current_language();obj2=News.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_n]=Truncator(i.content_id).chars(20);res[_o]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def news_create(request):
	context={};context[_E]=_p;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=NewsForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=News.objects.language(_B).create(title=request.POST.get(_G),content=request.POST.get(_J));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_X),post);print(_k,request.POST.get(_I));Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_l);messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_p))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=NewsForm();context[_L]=PhotoForm()
	return render(request,template,context)
def news_update(request,uuid):
	context={};context[_E]=_p;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_H:
		form=NewsForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.save();obj.tags.clear();print(_A5);save_tags(request.POST.getlist(_X),obj)
			if photo.is_valid():
				if request.POST.get(_I):print(_g);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_d)
			messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_p))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=NewsForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def news_delete(request,uuid):context={};site_id=get_site_id(request);data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_p))
class ArticleView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'article.html';return super(ArticleView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(ArticleView,self).get_context_data(*(args),**kwargs);context[_E]=_q;return context
def article_ajax(request):
	site_id=get_site_id(request);obj=Article();obj.set_current_language(_K);subquery1=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_G));subquery2=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_q).values(_a));lang=obj.get_current_language();obj2=Article.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_n]=Truncator(i.content_id).chars(20);res[_o]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def article_create(request):
	context={};context[_E]=_q;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=ArticleForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Article.objects.language(_B).create(title=request.POST.get(_G),content=request.POST.get(_J));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_X),post);print(_k,request.POST.get(_I));Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_l);messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_q))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=ArticleForm();context[_L]=PhotoForm()
	return render(request,template,context)
def article_update(request,uuid):
	context={};context[_E]=_q;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_H:
		form=ArticleForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.save();obj.tags.clear();print(_A5);save_tags(request.POST.getlist(_X),obj)
			if photo.is_valid():
				if request.POST.get(_I):print(_g);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_d)
			messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_q))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=ArticleForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def article_delete(request,uuid):context={};site_id=get_site_id(request);data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_q))
class EventsView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'events.html';return super(EventsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(EventsView,self).get_context_data(*(args),**kwargs);context[_E]=_r;return context
def events_ajax(request):
	site_id=get_site_id(request);obj=Events();obj.set_current_language(_K);subquery1=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_G));subquery2=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_r).values(_a));lang=obj.get_current_language();obj2=Events.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_n]=Truncator(i.content_id).chars(20);res[_o]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def events_create(request):
	context={};context[_E]=_r;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=EventsForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Events.objects.language(_B).create(title=request.POST.get(_G),content=request.POST.get(_J),location=request.POST.get(_AC),date=request.POST.get('date'),time=request.POST.get('time'));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.location=request.POST.get(_AC);post.save();save_tags(request.POST.getlist(_X),post);print(_k,request.POST.get(_I));Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_l);messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_r))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=EventsForm();context[_L]=PhotoForm()
	return render(request,template,context)
def events_update(request,uuid):
	context={};context[_E]=_r;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_H:
		form=EventsForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.location=request.POST.get(_AC);obj.date=request.POST.get('date');obj.time=request.POST.get('time');obj.save();obj.tags.clear();print(_A5);save_tags(request.POST.getlist(_X),obj)
			if photo.is_valid():
				if request.POST.get(_I):print(_g);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_d)
			messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_r))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=EventsForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def events_delete(request,uuid):context={};site_id=get_site_id(request);data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_r))
class SlideShowView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'slideshow.html';return super(SlideShowView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SlideShowView,self).get_context_data(*(args),**kwargs);context[_E]=_s;return context
def slideshow_ajax(request):
	site_id=get_site_id(request);lst=[];obj=SlideShow.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_G));subquery2=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_s).values(_a));lang=obj.get_current_language();obj2=SlideShow.objects.language(lang).filter(site_id=site_id).distinct().annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto))
		for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_n]=Truncator(i.content_id).chars(20);res[_o]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def slideshow_create(request):
	context={};context[_E]=_s;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=SlideShowForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=SlideShow.objects.language(_B).create(title=request.POST.get(_G),content=request.POST.get(_J),link=request.POST.get(_h));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.link=request.POST.get(_h);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_s))
		else:print(_x);context[_F]=SlideShowForm();context[_L]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_S));context[_F]=SlideShowForm();context[_L]=PhotoForm()
	return render(request,template,context)
def slideshow_update(request,uuid):
	context={};context[_E]=_s;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all();context['post_photo']=post_photo
	if request.method==_H:
		form=SlideShowForm(request.POST,instance=post);photo=PhotoForm(request.POST)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.link=request.POST.get(_h);obj.save()
			if request.POST.get(_I):print('photo is valid');print('Insert New photo');Photo.objects.create(content_object=obj,file_path=request.POST.get(_I));print(_d)
			else:print('photo not valid')
			messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_s))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=SlideShowForm(instance=post);context[_L]=PhotoForm()
	return render(request,template,context)
def slideshow_delete(request,uuid):context={};site_id=get_site_id(request);data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_s))
class DailyAlertView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'dailyalert.html';return super(DailyAlertView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DailyAlertView,self).get_context_data(*(args),**kwargs);context[_E]=_y;return context
def dailyalert_ajax(request):
	site_id=get_site_id(request);lst=[];obj=DailyAlert.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(DailyAlertTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_z));lang=obj.get_current_language();obj2=DailyAlert.objects.language(lang).filter(site_id=site_id).annotate(alert_id=subquery1)
		for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res['Alert (id)']=Truncator(i.alert_id).chars(20);res['Alert (en)']=Truncator(i.alert).chars(20);res[_A8]=Truncator(i.link).chars(20);res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def dailyalert_create(request):
	context={};context[_E]=_y;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=DailyAlertForm(request.POST)
		if form.is_valid():post=DailyAlert.objects.language(_B).create(alert=request.POST.get(_z),link=request.POST.get(_h),status=request.POST.get('status'));post.set_current_language(_K);post.alert=request.POST.get(_z);post.save();messages.info(request,mMsgBox.get(_R,request.POST.get(_z)));return redirect(reverse_lazy(_y))
		else:print(_x);context[_F]=DailyAlertForm()
	else:messages.info(request,mMsgBox.get(_S));context[_F]=DailyAlertForm()
	return render(request,template,context)
def dailyalert_update(request,uuid):
	context={};context[_E]=_y;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=DailyAlertForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.alert=request.POST.get(_z);obj.link=request.POST.get(_h);obj.status=request.POST.get('status');obj.save();messages.info(request,mMsgBox.get(_U,request.POST.get(_z)));return redirect(reverse_lazy(_y))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=DailyAlertForm(instance=post)
	return render(request,template,context)
def dailyalert_delete(request,uuid):context={};site_id=get_site_id(request);data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.alert;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_y))
class GreetingView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'greeting.html';return super(GreetingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(GreetingView,self).get_context_data(*(args),**kwargs);context[_AB]=True;context[_E]=_t;return context
def greeting_ajax(request):
	site_id=get_site_id(request);obj=Greeting();obj.set_current_language(_K);subquery1=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_G));subquery2=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_t).values(_a));lang=obj.get_current_language();obj2=Greeting.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_n]=Truncator(i.content_id).chars(20);res[_o]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def greeting_create(request):
	context={};context[_E]=_t;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=GreetingForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Greeting.objects.language(_B).create(title=request.POST.get(_G),content=request.POST.get(_J),name=request.POST.get(_C),designation=request.POST.get(_AD));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.name=request.POST.get(_C);post.designation=request.POST.get(_AD);post.save();save_tags(request.POST.getlist(_X),post);print(_k,request.POST.get(_I));Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_l);messages.info(request,mMsgBox.get(_R,request.POST.get(_G)));return redirect(reverse_lazy(_t))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=GreetingForm();context[_L]=PhotoForm()
	return render(request,template,context)
def greeting_update(request,uuid):
	context={};context[_E]=_t;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_H:
		form=GreetingForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.name=request.POST.get(_C);obj.designation=request.POST.get(_AD);obj.save()
			if photo.is_valid():
				if request.POST.get(_I):print(_g);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_d)
			messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_t))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=GreetingForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def greeting_delete(request,uuid):context={};site_id=get_site_id(request);data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_t))
class PagesView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'pages.html';return super(PagesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PagesView,self).get_context_data(*(args),**kwargs);context[_E]=_u;return context
def pages_ajax(request):
	site_id=get_site_id(request);obj=Pages();obj.set_current_language(_K);subquery1=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_G));subquery2=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_u).values(_a));lang=obj.get_current_language();obj2=Pages.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_n]=Truncator(i.content_id).chars(20);res[_o]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def pages_create(request):
	context={};context[_E]=_u;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=PagesForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Pages.objects.language(_B).create(title=request.POST.get(_G),content=request.POST.get(_J),menu_id=request.POST.get(_i));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_X),post);print(_k,request.POST.get(_I));Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_l);messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_u))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=PagesForm();context[_L]=PhotoForm()
	return render(request,template,context)
def pages_update(request,uuid):
	context={};context[_E]=_u;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_H:
		form=PagesForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.menu_id=request.POST.get(_i);obj.save();obj.tags.clear();print(_A5);save_tags(request.POST.getlist(_X),obj)
			if photo.is_valid():
				if request.POST.get(_I):print(_g);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_d)
			messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_u))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=PagesForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def pages_delete(request,uuid):context={};site_id=get_site_id(request);data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_u))
class SocialMediaView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'socialmedia.html';return super(SocialMediaView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SocialMediaView,self).get_context_data(*(args),**kwargs);context[_E]=_A0;return context
def socialmedia_ajax(request):
	site_id=get_site_id(request);obj2=SocialMedia.objects.filter(site_id=site_id);lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res['Kind']=i.kind;res[_A8]=Truncator(i.link).chars(30);res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def socialmedia_create(request):
	context={};context[_E]=_A0;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=SocialMediaForm(request.POST)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_A0))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=SocialMediaForm()
	return render(request,template,context)
def socialmedia_update(request,uuid):
	context={};context[_E]=_A0;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=SocialMediaForm(request.POST,instance=post)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_A0))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=SocialMediaForm(instance=post)
	return render(request,template,context)
def socialmedia_delete(request,uuid):context={};site_id=get_site_id(request);data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.link;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_A0))
class PhotoGalleryView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'photogallery.html';return super(PhotoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PhotoGalleryView,self).get_context_data(*(args),**kwargs);context[_E]=_v;return context
def photogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=PhotoGallery.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(PhotoGalleryTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_G));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_v).values(_a));lang=obj.get_current_language();obj2=PhotoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto))
		for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def photogallery_create(request):
	context={};context[_E]=_v;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=PhotoGalleryForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=PhotoGallery.objects.language(_B).create(title=request.POST.get(_G));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_v))
		else:print(_x);context[_F]=PhotoGalleryForm();context[_L]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_S));context[_F]=PhotoGalleryForm();context[_L]=PhotoForm()
	return render(request,template,context)
def photogallery_update(request,uuid):
	context={};context[_E]=_v;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_H:
		form=PhotoGalleryForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.save()
			if photo.is_valid():
				if request.POST.get(_I):print(_g);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_I));print(_d)
			messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_v))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=PhotoGalleryForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def photogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_v))
class VideoGalleryView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'videogallery.html';return super(VideoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(VideoGalleryView,self).get_context_data(*(args),**kwargs);context[_E]=_A1;return context
def videogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=VideoGallery.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(VideoGalleryTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_G));lang=obj.get_current_language();obj2=VideoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1)
		for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_e]=Truncator(i.title_id).chars(20);res[_f]=Truncator(i.title).chars(20);res['Embed']=Truncator(i.embed).chars(30);res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def videogallery_create(request):
	context={};context[_E]=_A1;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=VideoGalleryForm(request.POST)
		if form.is_valid():post=VideoGallery.objects.language(_B).create(title=request.POST.get(_G),embed=request.POST.get('embed'));post.set_current_language(_K);post.title=request.POST.get(_G);post.save();messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_A1))
		else:print(_x);context[_F]=VideoGalleryForm()
	else:messages.info(request,mMsgBox.get(_S));context[_F]=VideoGalleryForm()
	return render(request,template,context)
def videogallery_update(request,uuid):
	context={};context[_E]=_A1;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=VideoGalleryForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.embed=request.POST.get('embed');obj.save();messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_A1))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=VideoGalleryForm(instance=post)
	return render(request,template,context)
def videogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_A1))
class RelatedLinkView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'relatedlink.html';return super(RelatedLinkView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(RelatedLinkView,self).get_context_data(*(args),**kwargs);context[_E]=_A2;return context
def relatedlink_ajax(request):
	site_id=get_site_id(request);lst=[];obj=RelatedLink.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(RelatedLinkTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_C));lang=obj.get_current_language();obj2=RelatedLink.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1)
		for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_A6]=Truncator(i.name_id).chars(20);res[_A7]=Truncator(i.name).chars(20);res[_A8]=Truncator(i.link).chars(30);res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def relatedlink_create(request):
	context={};context[_E]=_A2;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=RelatedLinkForm(request.POST)
		if form.is_valid():post=RelatedLink.objects.language(_B).create(name=request.POST.get(_C),link=request.POST.get(_h));post.set_current_language(_K);post.name=request.POST.get(_C);post.save();messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_A2))
		else:print(_x);context[_F]=RelatedLinkForm()
	else:messages.info(request,mMsgBox.get(_S));context[_F]=RelatedLinkForm()
	return render(request,template,context)
def relatedlink_update(request,uuid):
	context={};context[_E]=_A2;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=RelatedLinkForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_C);obj.link=request.POST.get(_h);obj.save();messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_A2))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=RelatedLinkForm(instance=post)
	return render(request,template,context)
def relatedlink_delete(request,uuid):context={};site_id=get_site_id(request);data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_A2))
class DocumentView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'document.html';return super(DocumentView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DocumentView,self).get_context_data(*(args),**kwargs);context[_E]=_A3;return context
def document_ajax(request):
	site_id=get_site_id(request);lst=[];obj=Document.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_C));subquery2=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_J));lang=obj.get_current_language();obj2=Document.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1).annotate(content_id=subquery2)
		for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_A6]=Truncator(i.name_id).chars(20);res[_A7]=Truncator(i.name).chars(20);res['content (id)']=Truncator(i.content_id).chars(30);res['content (en)']=Truncator(i.content).chars(30);res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def document_create(request):
	context={};context[_E]=_A3;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:form=DocumentForm(request.POST,request.FILES);print('form=',form);post=Document.objects.language(_B).create(name=request.POST.get(_C),content=request.POST.get(_J),file_path_doc=request.POST.get(_AH));post.set_current_language(_K);post.name=request.POST.get(_C);post.content=request.POST.get(_J);post.save();messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_A3))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=DocumentForm()
	return render(request,template,context)
def document_update(request,uuid):
	context={};context[_E]=_A3;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=DocumentForm(request.POST,request.FILES,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_C);obj.content=request.POST.get(_J);obj.file_path_doc=request.POST.get(_AH);obj.save();messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_A3))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=DocumentForm(instance=post)
	return render(request,template,context)
def document_delete(request,uuid):context={};site_id=get_site_id(request);data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_A3))
class MenuView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'menu.html';return super(MenuView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(MenuView,self).get_context_data(*(args),**kwargs);context[_E]=_i;return context
def menugroup_create(request):A='Frontend';site_id=get_site_id(request);obj,created=MenuGroup.objects.get_or_create(site_id=site_id,name=A,defaults={'site_id':site_id,_C:A});return obj.id
def menu_ajax(request):
	site_id=get_site_id(request);group_id=menugroup_create(request);lst=[];menu=Menus(menu_group=group_id,kinds=1,site_id=site_id)
	if menu:
		obj2=menu.get_menus();print(obj2)
		for i in obj2:
			tmp='';lvl=i['level']
			while lvl>0:tmp+='<i class="fa fa-long-arrow-right"></i> &nbsp;&nbsp;&nbsp;&nbsp; ';lvl-=1
			res={};res[_M]=_D;res[_N]=i[_B];res[_O]=_D;res['Name']=Truncator(i[_C]).chars(20);res['Tree']=tmp+Truncator(i[_C]).chars(20);res[_A8]=Truncator(i[_h]).chars(30);res['Icon']=Truncator(i[_M]).chars(30);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def menu_create(request):
	context={};context[_E]=_i;site_id=get_site_id(request);group_id=menugroup_create(request);menu_group=MenuGroup.objects.get(id=group_id);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=MenuForm(request.POST)
		if form.is_valid():post=form.save(commit=_A);post.kind=1;post.save();post.menu_group.add(menu_group);messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_i))
		else:print(_x);context[_F]=MenuForm()
	else:messages.info(request,mMsgBox.get(_S));context[_F]=MenuForm()
	return render(request,template,context)
def menu_update(request,uuid):
	context={};context[_E]=_i;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Menu.objects.filter(id=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=MenuForm(request.POST,instance=post)
		if form.is_valid():form.save();messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_i))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=MenuForm(instance=post)
	return render(request,template,context)
def menu_delete(request,uuid):context={};site_id=get_site_id(request);data=Menu.objects.filter(id=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_i))
class AgencyView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'agency.html';return super(AgencyView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(AgencyView,self).get_context_data(*(args),**kwargs);context[_E]=_w;context[_AB]=True;return context
def agency_ajax(request):
	site_id=get_site_id(request);obj=Agency();obj.set_current_language(_K);service=Service.objects.filter(site_id=site_id).values_list(_w,flat=True);subquery1=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_A9));subquery2=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_AA));lang=obj.get_current_language();obj2=Agency.objects.language(lang).filter(id=service[0]).annotate(address_id=subquery1).annotate(notes_id=subquery2);lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res['Name']=Truncator(i.name).chars(20);res['Address (id)']=Truncator(i.address_id).chars(20);res['Address (en)']=Truncator(i.address).chars(20);res['Description (id)']=Truncator(i.notes_id).chars(20);res['Description (en)']=Truncator(i.notes).chars(20);res[_AE]=i.email;res[_AF]=i.phone;res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def agency_create(request):
	context={};context[_E]=_w;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=AgencyForm(request.POST)
		if form.is_valid():post=Agency.objects.language(_B).create(address=request.POST.get(_A9),notes=request.POST.get(_AA),name=request.POST.get(_C),email=request.POST.get(_AE),phone=request.POST.get(_AF),fax=request.POST.get('fax'),whatsapp=request.POST.get('whatsapp'));post.save();post.set_current_language(_K);post.address=request.POST.get(_A9);post.notes=request.POST.get(_AA);post.save();messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_w))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=AgencyForm()
	return render(request,template,context)
def agency_update(request,uuid):
	context={};context[_E]=_w;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=AgencyForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.address=request.POST.get(_A9);obj.notes=request.POST.get(_AA);obj.name=request.POST.get(_C);obj.email=request.POST.get(_AE);obj.phone=request.POST.get(_AF);obj.fax=request.POST.get('fax');obj.whatsapp=request.POST.get('whatsapp');obj.save();messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_w))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=AgencyForm(instance=post)
	return render(request,template,context)
def agency_delete(request,uuid):context={};site_id=get_site_id(request);data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_w))
class CategoriesView(TemplateView):
	site_id=_D
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'categories.html';return super(CategoriesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(CategoriesView,self).get_context_data(*(args),**kwargs);context[_E]=_A4;return context
def categories_ajax(request):
	site_id=get_site_id(request);obj=Categories();obj.set_current_language(_K);subquery1=Subquery(CategoriesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_C));lang=obj.get_current_language();obj2=Categories.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1);lst=[]
	for i in obj2:res={};res[_M]=_D;res[_N]=i.uuid;res[_O]=i.updated_at;res[_A6]=Truncator(i.name_id).chars(20);res[_A7]=Truncator(i.name).chars(20);res[_Y]=get_natural_datetime(i.updated_at);res[_P]=_D;lst.append(res)
	return JsonResponse(lst,safe=_A)
def categories_create(request):
	context={};context[_E]=_A4;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Q
	if request.method==_H:
		form=CategoriesForm(request.POST)
		if form.is_valid():post=Categories.objects.language(_B).create(name=request.POST.get(_C));post.save();post.set_current_language(_K);post.name=request.POST.get(_C);post.save();messages.info(request,mMsgBox.get(_R,request.POST.get(_C)));return redirect(reverse_lazy(_A4))
	else:messages.info(request,mMsgBox.get(_S));context[_F]=CategoriesForm()
	return render(request,template,context)
def categories_update(request,uuid):
	context={};context[_E]=_A4;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_H:
		form=CategoriesForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_C);obj.save();messages.info(request,mMsgBox.get(_U,request.POST.get(_C)));return redirect(reverse_lazy(_A4))
	else:messages.info(request,mMsgBox.get(_V));context[_F]=CategoriesForm(instance=post)
	return render(request,template,context)
def categories_delete(request,uuid):context={};site_id=get_site_id(request);data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_W,tmp));return redirect(reverse_lazy(_A4))