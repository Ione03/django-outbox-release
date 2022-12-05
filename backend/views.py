_AX='site name updated'
_AW='is_external'
_AV='order_menu'
_AU='Parent Menu'
_AT='file_path = '
_AS='select2_update'
_AR='Access From Menu cannot empty!'
_AQ='/pages/detail/'
_AP='Access From Menu'
_AO='is_visibled'
_AN='related link'
_AM='video gallery'
_AL='photo gallery'
_AK='social media'
_AJ='fail_add'
_AI='designation'
_AH='daily alert'
_AG='slide show'
_AF='notes'
_AE='address'
_AD='file_path_doc'
_AC='embed'
_AB='select2'
_AA='one_record_only'
_A9='Name (en)'
_A8='Name (id)'
_A7='related_link'
_A6='video_gallery'
_A5='photo_gallery'
_A4='social_media'
_A3='select2_menu'
_A2='daily_alert'
_A1='Link'
_A0='slide_show'
_z='alert'
_y=True
_x='form not valid '
_w='Content (en)'
_v='Content (id)'
_u='menu'
_t='document'
_s='banner'
_r='agency'
_q='pages'
_p='greeting'
_o='link'
_n='events'
_m='article'
_l='news'
_k='announcement'
_j='logo'
_i='Title (en)'
_h='Title (id)'
_g='location'
_f='Foto'
_e='file_path'
_d='Status'
_c='language'
_b='categories'
_a='Update'
_Z='tags'
_Y='delete'
_X='form_edit'
_W='save_edit'
_V='update.html'
_U='form_add'
_T='save_add'
_S='create.html'
_R='Action'
_Q='updated_at'
_P='uuid'
_O='icon'
_N='photo'
_M='str_file_path'
_L='content'
_K='status'
_J='en'
_I='POST'
_H='active_page_url'
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
	def get_context_data(self,*args,**kwargs):context=super(IndexView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page('dashboard');return context
class TagsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'tags.html';return super(TagsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(TagsView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_Z);return context
def tags_ajax(request):
	site_id=get_site_id(request);obj=Tags();obj.set_current_language(_J);subquery=Subquery(TagsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));lang=obj.get_current_language();obj2=Tags.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_A8]=Truncator(i.name_id).chars(50);res[_A9]=Truncator(i.name).chars(50);res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def tags_create(request):
	context={};context[_H]=_Z;context[_D]=get_translated_active_page(_Z);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=TagsForm(request.POST)
		if form.is_valid():
			tmp=Tags.objects.filter(translations__name=request.POST.get(_G))
			if tmp:messages.info(request,mMsgBox.get('file_exists'));context[_F]=TagsForm()
			else:post=Tags.objects.language(_A).create(name=request.POST.get(_G),status=request.POST.get(_K));post.set_current_language(_J);post.name=request.POST.get(_G);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_G)));return redirect(reverse_lazy(_Z))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=TagsForm()
	return render(request,template,context)
def tags_update(request,uuid):
	context={};context[_H]=_Z;context[_D]=get_translated_active_page(_Z);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=TagsForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_G);obj.status=request.POST.get(_K);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_G)));return redirect(reverse_lazy(_Z))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=TagsForm(instance=post)
	return render(request,template,context)
def tags_delete(request,uuid):context={};site_id=get_site_id(request);data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_Z))
class LogoView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'logo.html';return super(LogoView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(LogoView,self).get_context_data(*(args),**kwargs);context[_AA]=_y;context[_D]=get_translated_active_page(_j);return context
def logo_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_j).values(_e)[:1]);obj2=Logo.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res['Name']=Truncator(i.name).chars(50);res[_f]=i.file_path;res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def logo_create(request):
	context={};context[_H]=_j;context[_D]=get_translated_active_page(_j);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=LogoForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=form.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M));messages.info(request,mMsgBox.get(_T,request.POST.get(_G)));return redirect(reverse_lazy(_j))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=LogoForm();context[_N]=PhotoForm()
	return render(request,template,context)
def logo_update(request,uuid):
	context={};context[_H]=_j;context[_D]=get_translated_active_page(_j);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=LogoForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save()
			if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M));print('DOne')
			messages.info(request,mMsgBox.get(_W,request.POST.get(_G)));return redirect(reverse_lazy(_j))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=LogoForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def logo_delete(request,uuid):context={};site_id=get_site_id(request);data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_j))
class AnnouncementView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'announcement.html';return super(AnnouncementView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(AnnouncementView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_k);return context
def announcement_ajax(request):
	site_id=get_site_id(request);obj=Announcement();obj.set_current_language(_J);subquery1=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_L));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_k).values(_e)[:1]);lang=obj.get_current_language();obj2=Announcement.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);res[_v]=Truncator(i.content_id).chars(50);res[_w]=Truncator(i.content).chars(50);res[_f]=i.file_path;res['Priority']=i.get_priority_display();res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def announcement_create(request):
	context={};context[_H]=_k;context[_D]=_k;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=AnnouncementForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Announcement.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_L),categories_id=request.POST.get(_b),priority=request.POST.get('priority'),status=request.POST.get(_K));post.set_current_language(_J);post.title=request.POST.get(_E);post.content=request.POST.get(_L);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_M));messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_k))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=AnnouncementForm();context[_N]=PhotoForm()
	return render(request,template,context)
def announcement_update(request,uuid):
	context={};context[_H]=_k;context[_D]=get_translated_active_page(_k);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=AnnouncementForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_L);obj.categories_id=request.POST.get(_b);obj.status=request.POST.get(_K);obj.priority=request.POST.get('priority');obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_k))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=AnnouncementForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def announcement_delete(request,uuid):context={};site_id=get_site_id(request);data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_k))
class NewsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'news.html';return super(NewsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(NewsView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_l);return context
def news_ajax(request):
	site_id=get_site_id(request);obj=News();obj.set_current_language(_J);subquery1=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_L));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_l).values(_e)[:1]);lang=obj.get_current_language();obj2=News.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);res[_v]=Truncator(i.content_id).chars(50);res[_w]=Truncator(i.content).chars(50);res[_f]=i.file_path;res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def news_create(request):
	context={};context[_H]=_l;context[_D]=get_translated_active_page(_l);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=NewsForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=News.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_L),categories_id=request.POST.get(_b),status=request.POST.get(_K));post.set_current_language(_J);post.title=request.POST.get(_E);post.content=request.POST.get(_L);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_M));messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_l))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=NewsForm();context[_N]=PhotoForm()
	return render(request,template,context)
def news_update(request,uuid):
	context={};context[_H]=_l;context[_D]=get_translated_active_page(_l);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=NewsForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_L);obj.categories_id=request.POST.get(_b);obj.status=request.POST.get(_K);obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_l))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=NewsForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def news_delete(request,uuid):context={};site_id=get_site_id(request);data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_l))
class ArticleView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'article.html';return super(ArticleView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(ArticleView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_m);return context
def article_ajax(request):
	site_id=get_site_id(request);obj=Article();obj.set_current_language(_J);subquery1=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_L));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_m).values(_e)[:1]);lang=obj.get_current_language();obj2=Article.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);res[_v]=Truncator(i.content_id).chars(50);res[_w]=Truncator(i.content).chars(50);res[_f]=i.file_path;res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def article_create(request):
	context={};context[_H]=_m;context[_D]=get_translated_active_page(_m);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=ArticleForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Article.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_L),categories_id=request.POST.get(_b),status=request.POST.get(_K));post.set_current_language(_J);post.title=request.POST.get(_E);post.content=request.POST.get(_L);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_M));messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_m))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=ArticleForm();context[_N]=PhotoForm()
	return render(request,template,context)
def article_update(request,uuid):
	context={};context[_H]=_m;context[_D]=get_translated_active_page(_m);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=ArticleForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_L);obj.categories_id=request.POST.get(_b);obj.status=request.POST.get(_K);obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_m))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=ArticleForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def article_delete(request,uuid):context={};site_id=get_site_id(request);data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_m))
class EventsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'events.html';return super(EventsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(EventsView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_n);return context
def events_ajax(request):
	site_id=get_site_id(request);obj=Events();obj.set_current_language(_J);subquery1=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_L));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_n).values(_e)[:1]);lang=obj.get_current_language();obj2=Events.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);res[_v]=Truncator(i.content_id).chars(50);res[_w]=Truncator(i.content).chars(50);res[_f]=i.file_path;res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def events_create(request):
	context={};context[_H]=_n;context[_D]=get_translated_active_page(_n);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=EventsForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Events.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_L),location=request.POST.get(_g),categories_id=request.POST.get(_b),status=request.POST.get(_K),date=request.POST.get('date'),time=request.POST.get('time'));post.set_current_language(_J);post.title=request.POST.get(_E);post.content=request.POST.get(_L);post.location=request.POST.get(_g);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_M));messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_n))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=EventsForm();context[_N]=PhotoForm()
	return render(request,template,context)
def events_update(request,uuid):
	context={};context[_H]=_n;context[_D]=get_translated_active_page(_n);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=EventsForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_L);obj.location=request.POST.get(_g);obj.categories_id=request.POST.get(_b);obj.status=request.POST.get(_K);obj.date=request.POST.get('date');obj.time=request.POST.get('time');obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_n))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=EventsForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def events_delete(request,uuid):context={};site_id=get_site_id(request);data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_n))
class SlideShowView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'slide_show.html';return super(SlideShowView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SlideShowView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_AG);return context
def slideshow_ajax(request):
	site_id=get_site_id(request);lst=[];obj=SlideShow();obj.set_current_language(_J);subquery1=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_L));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model='slideshow').values(_e)[:1]);lang=obj.get_current_language();obj2=SlideShow.objects.language(lang).filter(site_id=site_id).distinct().annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);res[_v]=Truncator(i.content_id).chars(50);res[_w]=Truncator(i.content).chars(50);res[_f]=i.file_path;res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def slideshow_create(request):
	context={};context[_H]=_A0;context[_D]=get_translated_active_page(_AG);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=SlideShowForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=SlideShow.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_L),status=request.POST.get(_K));post.set_current_language(_J);post.title=request.POST.get(_E);post.content=request.POST.get(_L);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M));messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_A0))
		else:print(_x);context[_F]=SlideShowForm();context[_N]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=SlideShowForm();context[_N]=PhotoForm()
	return render(request,template,context)
def slideshow_update(request,uuid):
	context={};context[_H]=_A0;context[_D]=get_translated_active_page(_AG);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.first()
	if request.method==_I:
		form=SlideShowForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_L);obj.status=request.POST.get(_K);obj.save()
			if request.POST.get(_M):obj.photo.clear();Photo.objects.create(content_object=obj,file_path=request.POST.get(_M))
			else:print('photo not valid')
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_A0))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=SlideShowForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def slideshow_delete(request,uuid):context={};site_id=get_site_id(request);data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A0))
class DailyAlertView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'daily_alert.html';return super(DailyAlertView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DailyAlertView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_AH);return context
def dailyalert_ajax(request):
	site_id=get_site_id(request);lst=[];obj=DailyAlert();obj.set_current_language(_J);subquery1=Subquery(DailyAlertTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_z));lang=obj.get_current_language();obj2=DailyAlert.objects.language(lang).filter(site_id=site_id).annotate(alert_id=subquery1)
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res['Alert (id)']=Truncator(i.alert_id).chars(50);res['Alert (en)']=Truncator(i.alert).chars(50);res[_A1]=Truncator(i.link).chars(50);res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def dailyalert_create(request):
	context={};context[_H]=_A2;context[_D]=get_translated_active_page(_AH);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=DailyAlertForm(request.POST)
		if form.is_valid():post=DailyAlert.objects.language(_A).create(alert=request.POST.get(_z),link=request.POST.get(_o),status=request.POST.get(_K));post.set_current_language(_J);post.alert=request.POST.get(_z);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_z)));return redirect(reverse_lazy(_A2))
		else:print(_x);context[_F]=DailyAlertForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=DailyAlertForm()
	return render(request,template,context)
def dailyalert_update(request,uuid):
	context={};context[_H]=_A2;context[_D]=get_translated_active_page(_AH);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=DailyAlertForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.alert=request.POST.get(_z);obj.link=request.POST.get(_o);obj.status=request.POST.get(_K);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_z)));return redirect(reverse_lazy(_A2))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=DailyAlertForm(instance=post)
	return render(request,template,context)
def dailyalert_delete(request,uuid):context={};site_id=get_site_id(request);data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.alert;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A2))
class GreetingView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'greeting.html';return super(GreetingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(GreetingView,self).get_context_data(*(args),**kwargs);context[_AA]=_y;context[_D]=get_translated_active_page(_p);return context
def greeting_ajax(request):
	site_id=get_site_id(request);obj=Greeting();obj.set_current_language(_J);subquery1=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_L));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_p).values(_e)[:1]);lang=obj.get_current_language();obj2=Greeting.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);res[_v]=Truncator(i.content_id).chars(50);res[_w]=Truncator(i.content).chars(50);res[_f]=i.file_path;res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def greeting_create(request):
	context={};context[_H]=_p;context[_D]=get_translated_active_page(_p);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=GreetingForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Greeting.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_L),name=request.POST.get(_G),designation=request.POST.get(_AI),status=request.POST.get(_K));post.set_current_language(_J);post.title=request.POST.get(_E);post.content=request.POST.get(_L);post.name=request.POST.get(_G);post.designation=request.POST.get(_AI);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_M));messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_p))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=GreetingForm();context[_N]=PhotoForm()
	return render(request,template,context)
def greeting_update(request,uuid):
	context={};context[_H]=_p;context[_D]=get_translated_active_page(_p);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=GreetingForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_L);obj.name=request.POST.get(_G);obj.designation=request.POST.get(_AI);obj.status=request.POST.get(_K);obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_p))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=GreetingForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def greeting_delete(request,uuid):context={};site_id=get_site_id(request);data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_p))
class PagesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'pages.html';return super(PagesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PagesView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_q);return context
def pages_ajax(request):
	site_id=get_site_id(request);obj=Pages();obj.set_current_language(_J);subquery1=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery2=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_L));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_q).values(_e)[:1]);lang=obj.get_current_language();obj2=Pages.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);res[_v]=Truncator(i.content_id).chars(50);res[_w]=Truncator(i.content).chars(50);res[_f]=i.file_path;res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def menu_already_used(site_id,menu_id):
	A='translations__title';lang=get_active_language_choices()[0];pages=Pages.objects.language(lang).filter(site_id=site_id,menu_id=menu_id).values(A)
	if pages:return pages[0][A]
	return _C
def pages_create(request):
	context={};context[_H]=_q;context[_D]=get_translated_active_page(_q);context[_AB]=_AP;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=PagesForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			menu_id=request.POST.get(_A3)
			if menu_id:
				menu_name_already_used=menu_already_used(site_id,menu_id)
				if not menu_name_already_used:post=Pages.objects.language(_A).create(title=request.POST.get(_E),content=request.POST.get(_L),menu_id=menu_id,status=request.POST.get(_K));post.set_current_language(_J);post.title=request.POST.get(_E);post.content=request.POST.get(_L);post.save();save_tags(request.POST.getlist(_Z),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_M));obj=Menu.objects.get(id=menu_id);obj.link=_AQ+post.slug;obj.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_q))
				else:messages.info(request,mMsgBox.get(_AJ,'Menu already used by '+menu_name_already_used));context[_F]=PagesForm(request.POST);context[_N]=PhotoForm(request.POST)
			else:messages.info(request,mMsgBox.get(_AJ,_AR));context[_F]=PagesForm(request.POST);context[_N]=PhotoForm(request.POST)
	else:messages.info(request,mMsgBox.get(_U));context[_F]=PagesForm();context[_N]=PhotoForm()
	return render(request,template,context)
def pages_update(request,uuid):
	context={};context[_H]=_q;context[_D]=get_translated_active_page(_q);context[_AB]=_AP;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	select2_update={_A:post.menu_id,'text':post.menu.name if post.menu else _C};context[_AS]=select2_update
	if request.method==_I:
		form=PagesForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			menu_id=request.POST.get(_A3)
			if menu_id:
				lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.content=request.POST.get(_L);obj.menu_id=menu_id;obj.status=request.POST.get(_K);obj.save();obj.tags.clear();save_tags(request.POST.getlist(_Z),obj)
				if photo.is_valid():
					if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M))
				obj=Menu.objects.get(id=menu_id);obj.link=_AQ+post.slug;obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_q))
			else:messages.info(request,mMsgBox.get(_AJ,_AR));context[_F]=PagesForm(request.POST,instance=post);context[_N]=PhotoForm(request.POST,instance=post_photo)
	else:messages.info(request,mMsgBox.get(_X));context[_F]=PagesForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def pages_delete(request,uuid):context={};site_id=get_site_id(request);data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_q))
class SocialMediaView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'social_media.html';return super(SocialMediaView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SocialMediaView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_AK);return context
def socialmedia_ajax(request):
	site_id=get_site_id(request);obj2=SocialMedia.objects.filter(site_id=site_id);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res['Kind']=i.get_kind_display();res[_A1]=Truncator(i.link).chars(70);res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def socialmedia_create(request):
	context={};context[_H]=_A4;context[_D]=get_translated_active_page(_AK);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=SocialMediaForm(request.POST)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_o)));return redirect(reverse_lazy(_A4))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=SocialMediaForm()
	return render(request,template,context)
def socialmedia_update(request,uuid):
	context={};context[_H]=_A4;context[_D]=get_translated_active_page(_AK);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=SocialMediaForm(request.POST,instance=post)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_o)));return redirect(reverse_lazy(_A4))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=SocialMediaForm(instance=post)
	return render(request,template,context)
def socialmedia_delete(request,uuid):context={};site_id=get_site_id(request);data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.link;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A4))
class PhotoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'photo_gallery.html';return super(PhotoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PhotoGalleryView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_AL);return context
def photogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=PhotoGallery();obj.set_current_language(_J);subquery1=Subquery(PhotoGalleryTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model='photogallery').values(_e)[:1]);lang=obj.get_current_language();obj2=PhotoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);res[_f]=i.file_path;res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def photogallery_create(request):
	context={};context[_H]=_A5;context[_D]=get_translated_active_page(_AL);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=PhotoGalleryForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=PhotoGallery.objects.language(_A).create(title=request.POST.get(_E),status=request.POST.get(_K));post.set_current_language(_J);post.title=request.POST.get(_E);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M));messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_A5))
		else:print(_x);context[_F]=PhotoGalleryForm();context[_N]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=PhotoGalleryForm();context[_N]=PhotoForm()
	return render(request,template,context)
def photogallery_update(request,uuid):
	context={};context[_H]=_A5;context[_D]=get_translated_active_page(_AL);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=PhotoGalleryForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.status=request.POST.get(_K);obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_A5))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=PhotoGalleryForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def photogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A5))
def get_video_id(url_video):
	tmp=url_video.split('/')
	if tmp:return tmp[len(tmp)-1]
def download_thumbnail(request,video_id):download_url='https://img.youtube.com/vi/'+video_id+'/mqdefault.jpg';return download_image(request,download_url)
class VideoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'video_gallery.html';return super(VideoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(VideoGalleryView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_AM);return context
def videogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=VideoGallery();obj.set_current_language(_J);subquery1=Subquery(VideoGalleryTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model='videogallery').values(_e));lang=obj.get_current_language();obj2=VideoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);res[_f]=i.file_path;res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def videogallery_create(request):
	context={};context[_H]=_A6;context[_D]=get_translated_active_page(_AM);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=VideoGalleryForm(request.POST)
		if form.is_valid():post=VideoGallery.objects.language(_A).create(title=request.POST.get(_E),embed=request.POST.get(_AC),status=request.POST.get(_K));post.set_current_language(_J);post.title=request.POST.get(_E);post.save();video_id=get_video_id(post.embed_video);file_path=download_thumbnail(request,video_id);Photo.objects.create(content_object=post,file_path=file_path);messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_A6))
		else:print(_x);context[_F]=VideoGalleryForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=VideoGalleryForm()
	return render(request,template,context)
def videogallery_update(request,uuid):
	context={};context[_H]=_A6;context[_D]=get_translated_active_page(_AM);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=VideoGalleryForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.embed=request.POST.get(_AC);obj.status=request.POST.get(_K);obj.save();print('data = ');print(obj);print(post);video_id=get_video_id(obj.embed_video);file_path=download_thumbnail(request,video_id);obj.photo.clear();Photo.objects.create(content_object=obj,file_path=file_path);messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_A6))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=VideoGalleryForm(instance=post)
	return render(request,template,context)
def videogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A6))
class RelatedLinkView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'related_link.html';return super(RelatedLinkView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(RelatedLinkView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_AN);return context
def relatedlink_ajax(request):
	site_id=get_site_id(request);lst=[];obj=RelatedLink();obj.set_current_language(_J);subquery1=Subquery(RelatedLinkTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));lang=obj.get_current_language();obj2=RelatedLink.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1)
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_A8]=Truncator(i.name_id).chars(50);res[_A9]=Truncator(i.name).chars(50);res[_A1]=Truncator(i.link).chars(70);res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def relatedlink_create(request):
	context={};context[_H]=_A7;context[_D]=get_translated_active_page(_AN);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=RelatedLinkForm(request.POST)
		if form.is_valid():post=RelatedLink.objects.language(_A).create(name=request.POST.get(_G),link=request.POST.get(_o),status=request.POST.get(_K));post.set_current_language(_J);post.name=request.POST.get(_G);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_G)));return redirect(reverse_lazy(_A7))
		else:print(_x);context[_F]=RelatedLinkForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=RelatedLinkForm()
	return render(request,template,context)
def relatedlink_update(request,uuid):
	context={};context[_H]=_A7;context[_D]=get_translated_active_page(_AN);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=RelatedLinkForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_G);obj.link=request.POST.get(_o);obj.status=request.POST.get(_K);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_G)));return redirect(reverse_lazy(_A7))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=RelatedLinkForm(instance=post)
	return render(request,template,context)
def relatedlink_delete(request,uuid):context={};site_id=get_site_id(request);data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A7))
class DocumentView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'document.html';return super(DocumentView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DocumentView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_t);return context
def document_ajax(request):
	site_id=get_site_id(request);lst=[];obj=Document();obj.set_current_language(_J);subquery1=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery2=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_L));lang=obj.get_current_language();obj2=Document.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1).annotate(content_id=subquery2)
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_A8]=Truncator(i.name_id).chars(20);res[_A9]=Truncator(i.name).chars(20);res['content (id)']=Truncator(i.content_id).chars(30);res['content (en)']=Truncator(i.content).chars(30);res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def document_create(request):
	context={};context[_H]=_t;context[_D]=get_translated_active_page(_t);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=DocumentForm(request.POST,request.FILES);print('form=',form)
		if form.is_valid():print('categories = ',request.POST.get(_b));print('file = ',request.FILES.get(_AD));post=Document.objects.language(_A).create(name=request.POST.get(_G),content=request.POST.get(_L),file_path_doc=request.FILES.get(_AD),categories_id=request.POST.get(_b),status=request.POST.get(_K));post.set_current_language(_J);post.name=request.POST.get(_G);post.content=request.POST.get(_L);post.save();print(_AT,post.file_path_doc.path);post.size=os.stat(post.file_path_doc.path).st_size;post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_G)));return redirect(reverse_lazy(_t))
		else:messages.info(request,mMsgBox.get('form_fail'));context[_F]=DocumentForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=DocumentForm()
	return render(request,template,context)
def document_update(request,uuid):
	context={};context[_H]=_t;context[_D]=get_translated_active_page(_t);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=DocumentForm(request.POST,request.FILES,instance=post)
		if form.is_valid():
			lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_G);obj.content=request.POST.get(_L)
			if request.FILES.get(_AD):obj.file_path_doc=request.FILES.get(_AD)
			obj.status=request.POST.get(_K);obj.categories_id=request.POST.get(_b);obj.save();print(_AT,obj.file_path_doc.path);obj.size=os.stat(obj.file_path_doc.path).st_size;obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_G)));return redirect(reverse_lazy(_t))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=DocumentForm(instance=post)
	return render(request,template,context)
def document_delete(request,uuid):context={};site_id=get_site_id(request);data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_t))
class MenuView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'menu.html';return super(MenuView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(MenuView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_u);return context
def get_menu_group(site_id):
	A='Frontend Site ';site_name=Site.objects.get(pk=site_id).domain;menugroup=MenuGroup.objects.filter(site=site_id,kind=1);print('menugroup = ',menugroup)
	if menugroup:return menugroup[0].id
	else:
		lang1=get_active_language_choices()[0];lang2=_A
		if lang1==_A:lang2=_J
		post=MenuGroup.objects.language(lang1).create(site_id=site_id,kind=1,name=A+site_name);post.set_current_language(lang2);post.name=A+site_name;post.save();return post.id
def menu_ajax(request):
	A='Name (';site_id=get_site_id(request);group_id=get_menu_group(site_id);print('group_id = ',group_id);lst=[]
	if group_id:
		lang=get_active_language_choices()[0];lang2=_A
		if lang==_A:lang2=_J
		menu=Menus(menu_group=group_id,kinds=1,site_id=site_id)
		if menu:
			obj2=menu.get_menus()
			for i in obj2:
				tmp='';lvl=i['level']
				while lvl>0:tmp+='<i class="fa fa-long-arrow-right"></i> &nbsp;&nbsp;&nbsp;&nbsp; ';lvl-=1
				res={};res[_O]=_C;res[_P]=i[_P];res[_Q]=_C;res[A+lang+')']=Truncator(i[_G]).chars(50);res[A+lang2+')']=Menu.objects.language(lang2).get(pk=i[_A]).name;res['Tree']=tmp+Truncator(i[_G]).chars(70);res[_A1]=Truncator(i[_o]).chars(70);res['Icon']=Truncator(i[_O]).chars(50);res['Visibled']=Truncator(i[_AO]).chars(50);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def menu_create(request):
	context={};context[_H]=_u;context[_D]=get_translated_active_page(_u);context[_AB]=_AU;site_id=get_site_id(request);group_id=get_menu_group(site_id);menu_group=MenuGroup.objects.get(id=group_id);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=MenuForm(request.POST)
		if form.is_valid():form_clean=form.cleaned_data;print('select2_menu = ',request.POST.get(_A3));post=Menu.objects.language(_A).create(name=form_clean[_G],parent_id=request.POST.get(_A3),link=form_clean[_o],order_menu=form_clean[_AV],icon=form_clean[_O],is_visibled=form_clean[_AO],is_external=form_clean[_AW]);post.menu_group.add(menu_group);post.set_current_language(_J);post.name=form_clean[_G];post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_G)));return redirect(reverse_lazy(_u))
		else:print(_x);context[_F]=MenuForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=MenuForm()
	return render(request,template,context)
def menu_update(request,uuid):
	context={};context[_H]=_u;context[_D]=get_translated_active_page(_u);context[_AB]=_AU;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Menu.objects.filter(uuid=uuid);post=get_object_or_404(data);select2_update={_A:post.parent_id,'text':post.parent.name if post.parent else _C};context[_AS]=select2_update
	if request.method==_I:
		form=MenuForm(request.POST,instance=post)
		if form.is_valid():form_clean=form.cleaned_data;lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.name=form_clean[_G];obj.parent_id=request.POST.get(_A3);obj.link=form_clean[_o];obj.order_menu=form_clean[_AV];obj.icon=form_clean[_O];obj.is_visibled=form_clean[_AO];obj.is_external=form_clean[_AW];obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_G)));return redirect(reverse_lazy(_u))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=MenuForm(instance=post)
	return render(request,template,context)
def menu_delete(request,uuid):context={};site_id=get_site_id(request);data=Menu.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_u))
def site_name_update(site_id,name):site=Site.objects.get(id=site_id);site.name=name;site.save()
def get_translated_active_page(active_page):
	ret=active_page;lang=get_active_language_choices()[0];obj=Menu.objects.translated(lang).filter(translations__name=active_page)
	if obj:ret=obj[0].name
	ret=ret.replace(' ','_');return ret.lower
class AgencyView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'agency.html';return super(AgencyView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(AgencyView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_r);context[_AA]=_y;return context
def agency_ajax(request):
	site_id=get_site_id(request);obj=Agency();obj.set_current_language(_J);service=Service.objects.filter(site_id=site_id).values_list(_r,flat=_y);subquery1=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_AE));subquery2=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_AF));lang=obj.get_current_language();obj2=Agency.objects.language(lang).filter(id=service[0]).annotate(address_id=subquery1).annotate(notes_id=subquery2);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res['Name']=Truncator(i.name).chars(50);res['Address (id)']=Truncator(i.address_id).chars(50);res['Address (en)']=Truncator(i.address).chars(50);res['Description (id)']=Truncator(i.notes_id).chars(50);res['Description (en)']=Truncator(i.notes).chars(50);res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def agency_create(request):
	context={};context[_H]=_r;context[_D]=get_translated_active_page(_r);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=AgencyForm(request.POST)
		if form.is_valid():post=Agency.objects.language(_A).create(address=request.POST.get(_AE),notes=request.POST.get(_AF),name=request.POST.get(_G),email=request.POST.get('email'),phone=request.POST.get('phone'),fax=request.POST.get('fax'),whatsapp=request.POST.get('whatsapp'),status=request.POST.get(_K));post.set_current_language(_J);post.address=request.POST.get(_AE);post.notes=request.POST.get(_AF);post.save();site_name_update(site_id,request.POST.get(_G));print(_AX);messages.info(request,mMsgBox.get(_T,request.POST.get(_G)));return redirect(reverse_lazy(_r))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=AgencyForm()
	return render(request,template,context)
def agency_update(request,uuid):
	context={};context[_H]=_r;context[_D]=get_translated_active_page(_r);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=AgencyForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.address=request.POST.get(_AE);obj.notes=request.POST.get(_AF);obj.name=request.POST.get(_G);obj.email=request.POST.get('email');obj.phone=request.POST.get('phone');obj.fax=request.POST.get('fax');obj.whatsapp=request.POST.get('whatsapp');obj.status=request.POST.get(_K);obj.save();print('site name begin update');site_name_update(site_id,request.POST.get(_G));print(_AX);messages.info(request,mMsgBox.get(_W,request.POST.get(_G)));return redirect(reverse_lazy(_r))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=AgencyForm(instance=post)
	return render(request,template,context)
def agency_delete(request,uuid):context={};site_id=get_site_id(request);data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_r))
class CategoriesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'categories.html';return super(CategoriesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(CategoriesView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_b);return context
def categories_ajax(request):
	site_id=get_site_id(request);obj=Categories();obj.set_current_language(_J);subquery1=Subquery(CategoriesTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));lang=obj.get_current_language();obj2=Categories.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_A8]=Truncator(i.name_id).chars(50);res[_A9]=Truncator(i.name).chars(50);res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def categories_create(request):
	context={};context[_H]=_b;context[_D]=get_translated_active_page(_b);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=CategoriesForm(request.POST)
		if form.is_valid():post=Categories.objects.language(_A).create(name=request.POST.get(_G),status=request.POST.get(_K));post.set_current_language(_J);post.name=request.POST.get(_G);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_G)));return redirect(reverse_lazy(_b))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=CategoriesForm()
	return render(request,template,context)
def categories_update(request,uuid):
	context={};context[_H]=_b;context[_D]=get_translated_active_page(_b);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=CategoriesForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_G);obj.status=request.POST.get(_K);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_G)));return redirect(reverse_lazy(_b))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=CategoriesForm(instance=post)
	return render(request,template,context)
def categories_delete(request,uuid):context={};site_id=get_site_id(request);data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_b))
def menu_lookup_ajax(request):
	A='translations__name';lang=get_active_language_choices()[0];site_id=get_site_id(request);group_id=get_menu_group(site_id);print('menugroup=',group_id,lang);search=request.GET.get('search')
	if search:object_list=Menu.objects.translated(lang).filter(menu_group__id=group_id).filter(translations__name__icontains=search).values(_A,text=F(A))
	else:object_list=Menu.objects.translated(lang).filter(menu_group__id=group_id).values(_A,text=F(A))
	return JsonResponse({'results':list(object_list),'pagination':{'more':_y}},safe=_B)
class BannerView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'banner.html';return super(BannerView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(BannerView,self).get_context_data(*(args),**kwargs);context[_D]=get_translated_active_page(_s);return context
def banner_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_s).values(_e));obj2=Banner.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery);lst=[]
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res['Priority']=i.get_priority_display();res[_f]=i.file_path;res[_A1]=Truncator(i.link).chars(70);res[_d]=i.get_status_display();res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def banner_create(request):
	context={};context[_H]=_s;context[_D]=get_translated_active_page(_s);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=BannerForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=form.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M));messages.info(request,mMsgBox.get(_T,request.POST.get('position')));return redirect(reverse_lazy(_s))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=BannerForm();context[_N]=PhotoForm()
	return render(request,template,context)
def banner_update(request,uuid):
	context={};context[_H]=_s;context[_D]=get_translated_active_page(_s);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Banner.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=BannerForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save()
			if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M));print('DOne')
			messages.info(request,mMsgBox.get(_W,request.POST.get('position')));return redirect(reverse_lazy(_s))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=BannerForm(instance=post);context[_N]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def banner_delete(request,uuid):context={};site_id=get_site_id(request);data=Banner.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.position;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_s))
class LocationView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'location.html';return super(LocationView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(LocationView,self).get_context_data(*(args),**kwargs);context[_AA]=_y;context[_D]=get_translated_active_page(_g);return context
def location_ajax(request):
	site_id=get_site_id(request);lst=[];obj=Location();obj.set_current_language(_J);subquery1=Subquery(LocationTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));lang=obj.get_current_language();obj2=Location.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1)
	for i in obj2:res={};res[_O]=_C;res[_P]=i.uuid;res[_Q]=i.updated_at;res[_h]=Truncator(i.title_id).chars(50);res[_i]=Truncator(i.title).chars(50);tmp=Truncator(i.embed).chars(100);tmp=tmp.replace('<',' ');tmp=tmp.replace('>',' ');res['Embed']=tmp;res[_a]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def location_create(request):
	context={};context[_H]=_g;context[_D]=get_translated_active_page(_g);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=LocationForm(request.POST)
		if form.is_valid():post=Location.objects.language(_A).create(title=request.POST.get(_E),embed=request.POST.get(_AC),status=request.POST.get(_K));post.set_current_language(_J);post.title=request.POST.get(_E);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_g))
		else:print(_x);context[_F]=LocationForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=LocationForm()
	return render(request,template,context)
def location_update(request,uuid):
	context={};context[_H]=_g;context[_D]=get_translated_active_page(_g);site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Location.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=LocationForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_c);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_E);obj.embed=request.POST.get(_AC);obj.status=request.POST.get(_K);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_g))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=LocationForm(instance=post)
	return render(request,template,context)
def location_delete(request,uuid):context={};site_id=get_site_id(request);data=Location.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_g))