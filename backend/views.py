_A7='file_exists'
_A6='location'
_A5='Name (en)'
_A4='Name (id)'
_A3='Link'
_A2='tags.clear'
_A1='document'
_A0='relatedlink'
_z='videogallery'
_y='socialmedia'
_x='alert'
_w='dailyalert'
_v='form not valid '
_u='photogallery'
_t='pages'
_s='greeting'
_r='slideshow'
_q='events'
_p='article'
_o='news'
_n='Content (en)'
_m='Content (id)'
_l='announcement'
_k='done...'
_j='file path = '
_i='logo'
_h='link'
_g='Title (en)'
_f='Title (id)'
_e='DOne'
_d='update photo'
_c='Foto'
_b='Jumlah Foto'
_a='file_path'
_Z='language'
_Y='delete'
_X='form_edit'
_W='save_edit'
_V='update.html'
_U='form_add'
_T='save_add'
_S='create.html'
_R='Action'
_Q='Update'
_P='updated_at'
_O='uuid'
_N='icon'
_M='tags'
_L='photo'
_K='en'
_J='content'
_I='POST'
_H='str_file_path'
_G='title'
_F='form'
_E='name'
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
from core.models import Photo
from parler.utils.context import switch_language
from parler.views import TranslatableCreateView,TranslatableUpdateView
from .forms import *
from core.forms import PhotoForm
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
	def get_context_data(self,*args,**kwargs):context=super(TagsView,self).get_context_data(*(args),**kwargs);context[_D]=_M;return context
def tags_ajax(request):
	site_id=get_site_id(request);obj=Tags.objects.all()[0];obj.set_current_language(_K);subquery=Subquery(TagsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));lang=obj.get_current_language();obj2=Tags.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery);lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_A4]=Truncator(i.name_id).chars(20);res[_A5]=Truncator(i.name).chars(20);res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def tags_create(request):
	context={};context[_D]=_M;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=TagsForm(request.POST)
		if form.is_valid():
			tmp=Tags.objects.filter(translations__name=request.POST.get(_E))
			if tmp:messages.info(request,mMsgBox.get(_A7));context[_F]=TagsForm()
			else:post=Tags.objects.language(_A).create(name=request.POST.get(_E));post.save();post.set_current_language(_K);post.name=request.POST.get(_E);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_M))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=TagsForm()
	return render(request,template,context)
def tags_update(request,uuid):
	context={};context[_D]=_M;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=TagsForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_E);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_M))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=TagsForm(instance=post)
	return render(request,template,context)
def tags_delete(request,uuid):context={};site_id=get_site_id(request);data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_M))
class LogoView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'logo.html';return super(LogoView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(LogoView,self).get_context_data(*(args),**kwargs);context['one_record_only']=True;context[_D]=_i;return context
def logo_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_i).values(_a));obj2=Logo.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery).annotate(jml=Count(subquery));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res['Name']=Truncator(i.name).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def logo_create(request):
	context={};context[_D]=_i;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=LogoForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			tmp=Logo.objects.filter(name=request.POST.get(_E))
			if tmp:messages.info(request,mMsgBox.get(_A7));context[_F]=LogoForm();context[_L]=PhotoForm()
			else:post=form.save();print(_j,request.POST.get(_H));Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_k);messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_i))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=LogoForm();context[_L]=PhotoForm()
	return render(request,template,context)
def logo_update(request,uuid):
	context={};context[_D]=_i;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_I:
		form=LogoForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save();print('update text')
			if photo.is_valid():
				if request.POST.get(_H):print(_d);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_e)
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_i))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=LogoForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def logo_delete(request,uuid):context={};site_id=get_site_id(request);data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_i))
class AnnouncementView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'announcement.html';return super(AnnouncementView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(AnnouncementView,self).get_context_data(*(args),**kwargs);context[_D]=_l;return context
def announcement_ajax(request):
	site_id=get_site_id(request);obj=Announcement.objects.all()[0];obj.set_current_language(_K);subquery1=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery2=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_l).values(_a));lang=obj.get_current_language();obj2=Announcement.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_f]=Truncator(i.title_id).chars(20);res[_g]=Truncator(i.title).chars(20);res[_m]=Truncator(i.content_id).chars(20);res[_n]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def announcement_create(request):
	context={};context[_D]=_l;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=AnnouncementForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Announcement.objects.language(_A).create(title=request.POST.get(_G),content=request.POST.get(_J));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_M),post);print(_j,request.POST.get(_H));Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_k);messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_l))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=AnnouncementForm();context[_L]=PhotoForm()
	return render(request,template,context)
def announcement_update(request,uuid):
	context={};context[_D]=_l;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_I:
		form=AnnouncementForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.save();obj.tags.clear();print(_A2);save_tags(request.POST.getlist(_M),obj)
			if photo.is_valid():
				if request.POST.get(_H):print(_d);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_e)
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_l))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=AnnouncementForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def announcement_delete(request,uuid):context={};site_id=get_site_id(request);data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_l))
class NewsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'news.html';return super(NewsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(NewsView,self).get_context_data(*(args),**kwargs);context[_D]=_o;return context
def news_ajax(request):
	site_id=get_site_id(request);obj=News.objects.all()[0];obj.set_current_language(_K);subquery1=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery2=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_o).values(_a));lang=obj.get_current_language();obj2=News.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_f]=Truncator(i.title_id).chars(20);res[_g]=Truncator(i.title).chars(20);res[_m]=Truncator(i.content_id).chars(20);res[_n]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def news_create(request):
	context={};context[_D]=_o;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=NewsForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=News.objects.language(_A).create(title=request.POST.get(_G),content=request.POST.get(_J));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_M),post);print(_j,request.POST.get(_H));Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_k);messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_o))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=NewsForm();context[_L]=PhotoForm()
	return render(request,template,context)
def news_update(request,uuid):
	context={};context[_D]=_o;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_I:
		form=NewsForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.save();obj.tags.clear();print(_A2);save_tags(request.POST.getlist(_M),obj)
			if photo.is_valid():
				if request.POST.get(_H):print(_d);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_e)
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_o))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=NewsForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def news_delete(request,uuid):context={};site_id=get_site_id(request);data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_o))
class ArticleView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'article.html';return super(ArticleView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(ArticleView,self).get_context_data(*(args),**kwargs);context[_D]=_p;return context
def article_ajax(request):
	site_id=get_site_id(request);obj=Article.objects.all()[0];obj.set_current_language(_K);subquery1=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery2=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_p).values(_a));lang=obj.get_current_language();obj2=Article.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_f]=Truncator(i.title_id).chars(20);res[_g]=Truncator(i.title).chars(20);res[_m]=Truncator(i.content_id).chars(20);res[_n]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def article_create(request):
	context={};context[_D]=_p;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=ArticleForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Article.objects.language(_A).create(title=request.POST.get(_G),content=request.POST.get(_J));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_M),post);print(_j,request.POST.get(_H));Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_k);messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_p))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=ArticleForm();context[_L]=PhotoForm()
	return render(request,template,context)
def article_update(request,uuid):
	context={};context[_D]=_p;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_I:
		form=ArticleForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.save();obj.tags.clear();print(_A2);save_tags(request.POST.getlist(_M),obj)
			if photo.is_valid():
				if request.POST.get(_H):print(_d);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_e)
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_p))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=ArticleForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def article_delete(request,uuid):context={};site_id=get_site_id(request);data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_p))
class EventsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'events.html';return super(EventsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(EventsView,self).get_context_data(*(args),**kwargs);context[_D]=_q;return context
def events_ajax(request):
	site_id=get_site_id(request);obj=Events.objects.all()[0];obj.set_current_language(_K);subquery1=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery2=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_q).values(_a));lang=obj.get_current_language();obj2=Events.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_f]=Truncator(i.title_id).chars(20);res[_g]=Truncator(i.title).chars(20);res[_m]=Truncator(i.content_id).chars(20);res[_n]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def events_create(request):
	context={};context[_D]=_q;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=EventsForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Events.objects.language(_A).create(title=request.POST.get(_G),content=request.POST.get(_J),location=request.POST.get(_A6),date=request.POST.get('date'),time=request.POST.get('time'));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.location=request.POST.get(_A6);post.save();save_tags(request.POST.getlist(_M),post);print(_j,request.POST.get(_H));Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_k);messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_q))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=EventsForm();context[_L]=PhotoForm()
	return render(request,template,context)
def events_update(request,uuid):
	context={};context[_D]=_q;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_I:
		form=EventsForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.location=request.POST.get(_A6);obj.date=request.POST.get('date');obj.time=request.POST.get('time');obj.save();obj.tags.clear();print(_A2);save_tags(request.POST.getlist(_M),obj)
			if photo.is_valid():
				if request.POST.get(_H):print(_d);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_e)
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_q))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=EventsForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def events_delete(request,uuid):context={};site_id=get_site_id(request);data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_q))
class SlideShowView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'slideshow.html';return super(SlideShowView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SlideShowView,self).get_context_data(*(args),**kwargs);context[_D]=_r;return context
def slideshow_ajax(request):
	site_id=get_site_id(request);lst=[];obj=SlideShow.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery2=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_r).values(_a));lang=obj.get_current_language();obj2=SlideShow.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto))
		for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_f]=Truncator(i.title_id).chars(20);res[_g]=Truncator(i.title).chars(20);res[_m]=Truncator(i.content_id).chars(20);res[_n]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def slideshow_create(request):
	context={};context[_D]=_r;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=SlideShowForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=SlideShow.objects.language(_A).create(title=request.POST.get(_G),content=request.POST.get(_J),link=request.POST.get(_h));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.link=request.POST.get(_h);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_r))
		else:print(_v);context[_F]=SlideShowForm();context[_L]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=SlideShowForm();context[_L]=PhotoForm()
	return render(request,template,context)
def slideshow_update(request,uuid):
	context={};context[_D]=_r;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_I:
		form=SlideShowForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.link=request.POST.get(_h);obj.save()
			if photo.is_valid():
				if request.POST.get(_H):print(_d);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_e)
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_r))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=SlideShowForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def slideshow_delete(request,uuid):context={};site_id=get_site_id(request);data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_r))
class DailyAlertView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'dailyalert.html';return super(DailyAlertView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DailyAlertView,self).get_context_data(*(args),**kwargs);context[_D]=_w;return context
def dailyalert_ajax(request):
	site_id=get_site_id(request);lst=[];obj=DailyAlert.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(DailyAlertTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_x));lang=obj.get_current_language();obj2=DailyAlert.objects.language(lang).filter(site_id=site_id).annotate(alert_id=subquery1)
		for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res['Alert (id)']=Truncator(i.alert_id).chars(20);res['Alert (en)']=Truncator(i.alert).chars(20);res[_A3]=Truncator(i.link).chars(20);res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def dailyalert_create(request):
	context={};context[_D]=_w;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=DailyAlertForm(request.POST)
		if form.is_valid():post=DailyAlert.objects.language(_A).create(alert=request.POST.get(_x),link=request.POST.get(_h),status=request.POST.get('status'));post.set_current_language(_K);post.alert=request.POST.get(_x);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_x)));return redirect(reverse_lazy(_w))
		else:print(_v);context[_F]=DailyAlertForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=DailyAlertForm()
	return render(request,template,context)
def dailyalert_update(request,uuid):
	context={};context[_D]=_w;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=DailyAlertForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.alert=request.POST.get(_x);obj.link=request.POST.get(_h);obj.status=request.POST.get('status');obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_x)));return redirect(reverse_lazy(_w))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=DailyAlertForm(instance=post)
	return render(request,template,context)
def dailyalert_delete(request,uuid):context={};site_id=get_site_id(request);data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.alert;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_w))
class GreetingView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'greeting.html';return super(GreetingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(GreetingView,self).get_context_data(*(args),**kwargs);context[_D]=_s;return context
def greeting_ajax(request):
	site_id=get_site_id(request);obj=Greeting.objects.all()[0];obj.set_current_language(_K);subquery1=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery2=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_s).values(_a));lang=obj.get_current_language();obj2=Greeting.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_f]=Truncator(i.title_id).chars(20);res[_g]=Truncator(i.title).chars(20);res[_m]=Truncator(i.content_id).chars(20);res[_n]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def greeting_create(request):
	context={};context[_D]=_s;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=GreetingForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Greeting.objects.language(_A).create(title=request.POST.get(_G),content=request.POST.get(_J));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_M),post);print(_j,request.POST.get(_H));Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_k);messages.info(request,mMsgBox.get(_T,request.POST.get(_G)));return redirect(reverse_lazy(_s))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=GreetingForm();context[_L]=PhotoForm()
	return render(request,template,context)
def greeting_update(request,uuid):
	context={};context[_D]=_s;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_I:
		form=GreetingForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.save()
			if photo.is_valid():
				if request.POST.get(_H):print(_d);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_e)
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_s))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=GreetingForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def greeting_delete(request,uuid):context={};site_id=get_site_id(request);data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_s))
class PagesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'pages.html';return super(PagesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PagesView,self).get_context_data(*(args),**kwargs);context[_D]=_t;return context
def pages_ajax(request):
	site_id=get_site_id(request);obj=Pages.objects.all()[0];obj.set_current_language(_K);subquery1=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery2=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_J));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_t).values(_a));lang=obj.get_current_language();obj2=Pages.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto));lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_f]=Truncator(i.title_id).chars(20);res[_g]=Truncator(i.title).chars(20);res[_m]=Truncator(i.content_id).chars(20);res[_n]=Truncator(i.content).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def pages_create(request):
	context={};context[_D]=_t;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=PagesForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Pages.objects.language(_A).create(title=request.POST.get(_G),content=request.POST.get(_J),menu_id=request.POST.get('menu'));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.content=request.POST.get(_J);post.save();save_tags(request.POST.getlist(_M),post);print(_j,request.POST.get(_H));Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_k);messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_t))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=PagesForm();context[_L]=PhotoForm()
	return render(request,template,context)
def pages_update(request,uuid):
	context={};context[_D]=_t;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_I:
		form=PagesForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.content=request.POST.get(_J);obj.menu_id=request.POST.get('menu');obj.save();obj.tags.clear();print(_A2);save_tags(request.POST.getlist(_M),obj)
			if photo.is_valid():
				if request.POST.get(_H):print(_d);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_e)
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_t))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=PagesForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def pages_delete(request,uuid):context={};site_id=get_site_id(request);data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_t))
class SocialMediaView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'socialmedia.html';return super(SocialMediaView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SocialMediaView,self).get_context_data(*(args),**kwargs);context[_D]=_y;return context
def socialmedia_ajax(request):
	site_id=get_site_id(request);obj2=SocialMedia.objects.filter(site_id=site_id);lst=[]
	for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res['Kind']=i.kind;res[_A3]=Truncator(i.link).chars(30);res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def socialmedia_create(request):
	context={};context[_D]=_y;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=SocialMediaForm(request.POST)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_y))
	else:messages.info(request,mMsgBox.get(_U));context[_F]=SocialMediaForm()
	return render(request,template,context)
def socialmedia_update(request,uuid):
	context={};context[_D]=_y;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=SocialMediaForm(request.POST,instance=post)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_y))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=SocialMediaForm(instance=post)
	return render(request,template,context)
def socialmedia_delete(request,uuid):context={};site_id=get_site_id(request);data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.link;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_y))
class PhotoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'photogallery.html';return super(PhotoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PhotoGalleryView,self).get_context_data(*(args),**kwargs);context[_D]=_u;return context
def photogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=PhotoGallery.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(PhotoGalleryTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_u).values(_a));lang=obj.get_current_language();obj2=PhotoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(file_path=subquery_foto).annotate(jml=Count(subquery_foto))
		for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_f]=Truncator(i.title_id).chars(20);res[_g]=Truncator(i.title).chars(20);res[_b]=i.jml;res[_c]=i.file_path;res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def photogallery_create(request):
	context={};context[_D]=_u;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=PhotoGalleryForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=PhotoGallery.objects.language(_A).create(title=request.POST.get(_G));post.save();post.set_current_language(_K);post.title=request.POST.get(_G);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_u))
		else:print(_v);context[_F]=PhotoGalleryForm();context[_L]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=PhotoGalleryForm();context[_L]=PhotoForm()
	return render(request,template,context)
def photogallery_update(request,uuid):
	context={};context[_D]=_u;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.get()
	if request.method==_I:
		form=PhotoGalleryForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.save()
			if photo.is_valid():
				if request.POST.get(_H):print(_d);post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_H));print(_e)
			messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_u))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=PhotoGalleryForm(instance=post);context[_L]=PhotoForm(instance=post_photo)
	return render(request,template,context)
def photogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_u))
class VideoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'videogallery.html';return super(VideoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(VideoGalleryView,self).get_context_data(*(args),**kwargs);context[_D]=_z;return context
def videogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=VideoGallery.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(VideoGalleryTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_G));lang=obj.get_current_language();obj2=VideoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1)
		for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_f]=Truncator(i.title_id).chars(20);res[_g]=Truncator(i.title).chars(20);res['Embed']=Truncator(i.embed).chars(30);res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def videogallery_create(request):
	context={};context[_D]=_z;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=VideoGalleryForm(request.POST)
		if form.is_valid():post=VideoGallery.objects.language(_A).create(title=request.POST.get(_G),embed=request.POST.get('embed'));post.set_current_language(_K);post.title=request.POST.get(_G);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_z))
		else:print(_v);context[_F]=VideoGalleryForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=VideoGalleryForm()
	return render(request,template,context)
def videogallery_update(request,uuid):
	context={};context[_D]=_z;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=VideoGalleryForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_G);obj.embed=request.POST.get('embed');obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_z))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=VideoGalleryForm(instance=post)
	return render(request,template,context)
def videogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_z))
class RelatedLinkView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'relatedlink.html';return super(RelatedLinkView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(RelatedLinkView,self).get_context_data(*(args),**kwargs);context[_D]=_A0;return context
def relatedlink_ajax(request):
	site_id=get_site_id(request);lst=[];obj=RelatedLink.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(RelatedLinkTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));lang=obj.get_current_language();obj2=RelatedLink.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1)
		for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_A4]=Truncator(i.name_id).chars(20);res[_A5]=Truncator(i.name).chars(20);res[_A3]=Truncator(i.link).chars(30);res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def relatedlink_create(request):
	context={};context[_D]=_A0;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=RelatedLinkForm(request.POST)
		if form.is_valid():post=RelatedLink.objects.language(_A).create(name=request.POST.get(_E),link=request.POST.get(_h));post.set_current_language(_K);post.name=request.POST.get(_E);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_A0))
		else:print(_v);context[_F]=RelatedLinkForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=RelatedLinkForm()
	return render(request,template,context)
def relatedlink_update(request,uuid):
	context={};context[_D]=_A0;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=RelatedLinkForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_E);obj.link=request.POST.get(_h);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_A0))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=RelatedLinkForm(instance=post)
	return render(request,template,context)
def relatedlink_delete(request,uuid):context={};site_id=get_site_id(request);data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A0))
class DocumentView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_B);self.template_name=template+'document.html';return super(DocumentView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DocumentView,self).get_context_data(*(args),**kwargs);context[_D]=_A1;return context
def document_ajax(request):
	site_id=get_site_id(request);lst=[];obj=Document.objects.all()
	if obj:
		obj=obj[0];obj.set_current_language(_K);subquery1=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_A),language_code=_A).values(_E));lang=obj.get_current_language();obj2=Document.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1)
		for i in obj2:res={};res[_N]=_C;res[_O]=i.uuid;res[_P]=i.updated_at;res[_A4]=Truncator(i.name_id).chars(20);res[_A5]=Truncator(i.name).chars(20);res[_A3]=Truncator(i.link).chars(30);res[_Q]=get_natural_datetime(i.updated_at);res[_R]=_C;lst.append(res)
	return JsonResponse(lst,safe=_B)
def document_create(request):
	context={};context[_D]=_A1;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_S
	if request.method==_I:
		form=DocumentForm(request.POST)
		if form.is_valid():post=Document.objects.language(_A).create(name=request.POST.get(_E),link=request.POST.get(_h));post.set_current_language(_K);post.name=request.POST.get(_E);post.save();messages.info(request,mMsgBox.get(_T,request.POST.get(_E)));return redirect(reverse_lazy(_A1))
		else:print(_v);context[_F]=DocumentForm()
	else:messages.info(request,mMsgBox.get(_U));context[_F]=DocumentForm()
	return render(request,template,context)
def document_update(request,uuid):
	context={};context[_D]=_A1;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_B)+_V;data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=DocumentForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_Z);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_E);obj.link=request.POST.get(_h);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_E)));return redirect(reverse_lazy(_A1))
	else:messages.info(request,mMsgBox.get(_X));context[_F]=DocumentForm(instance=post)
	return render(request,template,context)
def document_delete(request,uuid):context={};site_id=get_site_id(request);data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A1))