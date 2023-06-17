_B8='expired_date'
_B7='is_active'
_B6='is_frontend'
_B5='site name updated'
_B4='Description (en)'
_B3='Description (id)'
_B2='is_external'
_B1='Parent Menu'
_B0='file_path = '
_A_='select2_update'
_Az='Access From Menu cannot empty!'
_Ay='/pages/detail/'
_Ax='Access From Menu'
_Aw='order Item'
_Av='file_exists'
_Au='agency_id'
_At='/accounts/logout/'
_As='count'
_Ar='%d %b %y'
_Aq='end_date='
_Ap='start_date='
_Ao='sites'
_An='why us'
_Am='model list'
_Al='template_owner'
_Ak='template list'
_Aj='template owner'
_Ai='is_visibled'
_Ah='order_menu'
_Ag='related link'
_Af='video gallery'
_Ae='photo gallery'
_Ad='how it works'
_Ac='social media'
_Ab='designation'
_Aa='daily alert'
_AZ='slide show'
_AY='result'
_AX='email'
_AW='file_path_doc'
_AV='embed'
_AU='fail_add'
_AT='select2'
_AS='sub_title'
_AR='Header Text'
_AQ='one_record_only'
_AP='whyus'
_AO='site'
_AN='modellist'
_AM='template'
_AL='templateowner'
_AK='related_link'
_AJ='video_gallery'
_AI='photo_gallery'
_AH='how_it_works'
_AG='social_media'
_AF='select2_menu'
_AE='daily_alert'
_AD='Link'
_AC='slide_show'
_AB='Name (en)'
_AA='Name (id)'
_A9='notes'
_A8='address'
_A7='dashboard'
_A6='description'
_A5='alert'
_A4='Name'
_A3='form not valid '
_A2='user'
_A1='document'
_A0='banner'
_z='product'
_y='pages'
_x='greeting'
_w='link'
_v='events'
_u='article'
_t='news'
_s='is_header_text'
_r='fasilities'
_q='announcement'
_p='logo'
_o='service'
_n='Content (en)'
_m='Content (id)'
_l='location'
_k='agency'
_j='Foto'
_i='file_path'
_h='Title (en)'
_g='Title (id)'
_f='categories'
_e='tags'
_d='language'
_c='Status'
_b=True
_a='save_add'
_Z='Update'
_Y='delete'
_X='form_edit'
_W='save_edit'
_V='update.html'
_U='form_add'
_T='create.html'
_S='Action'
_R='updated_at'
_Q='uuid'
_P='icon'
_O='str_file_path'
_N='status'
_M='photo'
_L='en'
_K='content'
_J='active_page_url'
_I='POST'
_H='name'
_G='form'
_F='title'
_E='active_page'
_D='menu'
_C=None
_B='id'
_A=False
import calendar,datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.db import transaction
from django.db.models import Count,F,OuterRef,Subquery
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import Truncator
from django.views.generic import TemplateView
from hitcount.models import Hit,HitCount
from menu.menus import Menus
from menu.models import *
from parler.utils import get_active_language_choices
from core.forms import *
from core.models import *
from core.send_email import send_email
from core.tokens import account_activation_token
from core.views import download_image
from django_outbox import msgbox
from django_outbox.common import *
from education.models import *
from .decorator import group_required
from .forms import *
User=get_user_model()
mMsgBox=msgbox.ClsMsgBox()
def save_tags(tag_list,obj_master):
	i=0
	while i<len(tag_list):tag=Tags.objects.get(id=tag_list[i]);obj_master.tags.add(tag);i+=1
class PostLoginView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);self.template_name='allauth/account/'+'post_login.html';return super(PostLoginView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PostLoginView,self).get_context_data(*(args),**kwargs);context[_E]=get_translated_active_page(_A7);return context
def get_menu_caches(request,caches_name,site_id,active_page,kinds=2):
	print('siteID',site_id);caches_timeout=getattr(settings,'CACHES_TIMEOUT',12*60*60);menu=cache.get(f"{caches_name}_{kinds}",version=site_id);menu_class=cache.get(f"{caches_name}_class_{kinds}",version=site_id)
	if menu_class is _C:
		print('load menu from DB');menu_list=[];group_id=0
		if kinds==2:
			user_id=request.user.id;obj=User.objects.get(id=user_id);group_id=obj.groups.all()[:1]
			if group_id:group_id=group_id.get().id
			model_list=[];temp=Template.objects.filter(site__id=site_id,is_frontend=1)
			if temp:temp=temp.get().id;model_list=list(ModelListSetting.objects.filter(template_id=temp).values_list('model_list_id',flat=_b))
			if model_list:menu_list=list(ModelList.objects.filter(id__in=model_list).values_list('menu_id',flat=_b))
		elif kinds==1:
			group_id=MenuGroup.objects.filter(site_id=site_id,kind=kinds)
			if group_id:group_id=group_id[0].id
		if group_id:menu_class=Menus(group_id,kinds,menu_list);cache.set(f"{caches_name}_class_{kinds}",menu_class,timeout=caches_timeout,version=site_id)
		else:print('Group ID Not found!')
	else:print('load menu from Cache')
	if menu is _C:menu=menu_class.get_menus();cache.set(f"{caches_name}_{kinds}",menu,timeout=caches_timeout,version=site_id)
	active_page=active_page.replace('_',' ');menu_active=menu_class.get_active_menu_by_name(active_page);return{'my_menu':menu,'my_active':menu_active}
class IndexView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id(request)
		if self.site_id==-1:return redirect(reverse_lazy(_A7))
		elif self.site_id==-2:return redirect(_At)
		elif self.site_id==-3 or self.site_id==-31:return redirect(reverse_lazy('user_init_agency'))
		elif self.site_id==-4 or self.site_id==-41:return redirect(reverse_lazy('user_init_service',kwargs={_Au:get_agency_from(request)}))
		else:print('GOTO INDEX DASHBOARD');template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'index.html'
		return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(IndexView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_A7);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
@transaction.atomic
def user_init_agency(request):
	context={};template='backend/smart-admin-2/user_initialize_agency.html';user=User.objects.filter(id=request.user.id)
	if user:
		user=user.get();agency=user.agency.all();context[_k]=agency
		for i in agency:
			if i.is_default:print('FOUND SERVICE');return redirect(f"/dashboard/user/initialize/service/{i.id}")
	else:return redirect(_At)
	if request.method==_I:
		name=request.POST.get('agent-name');agency,created=Agency.objects.language(_B).get_or_create(name=name,defaults={'is_default':_b,_A8:'',_A9:''});agency.set_current_language(_L);agency.address='';agency.notes='';agency.save();print(f"DATA: {agency} - {created}")
		if created:print('ADD AGENCY TO USER');user.agency.add(agency);return redirect(reverse_lazy(_A7))
		else:messages.info(request,f'"{name}" sudah digunakan!')
	return render(request,template,context)
def user_init_agency_ajax(request,agency_id):
	print('agency_id_ajax',agency_id);user=User.objects.get(id=request.user.id)
	for i in user.agency.filter(is_default=_b):i.is_default=_A;i.save()
	agency=user.agency.filter(id=agency_id)
	if agency:agency=agency.get();agency.is_default=_b;agency.save()
	return JsonResponse({_AY:_b},safe=_A)
def user_init_service_ajax(request,agency_id,service_id):
	print('REAL service_id_ajax',agency_id,service_id);mfound=_A;user=User.objects.get(id=request.user.id);agency=user.agency.filter(is_default=_b)[:1]
	if agency:
		agency=agency.get()
		if agency.id==agency_id:print('OKE PARAMETER BENAR');mfound=_b
	if mfound:
		print('clear all is_default service');service=Service.objects.filter(agency_id=agency.id,is_default=_b)
		for i in service:i.is_default=_A;i.save()
		service=Service.objects.filter(id=service_id,agency_id=agency.id)
		if service:service=service.get();service.is_default=_b;service.save()
		return JsonResponse({_AY:_b},safe=_A)
	return JsonResponse({_AY:_A},safe=_A)
@transaction.atomic
def user_init_service(request,agency_id):
	context={};template='backend/smart-admin-2/user_initialize_service.html';context['service_opt']=OptServiceType.choices;service_existing=Service.objects.filter(agency_id=agency_id).order_by('kind');context[_o]=service_existing;context[_Au]=agency_id
	if request.method==_I:
		print('posting data Service ......');service=request.POST.get('select_service');main_domain=getattr(settings,'MAIN_DOMAIN',request.get_host());user=User.objects.get(id=request.user.id);name=user.email.split('@')[0];subdomain=f"{name}.{main_domain}";tgl_exp=datetime.now();tgl_exp=add_months(tgl_exp,1);created=_A;mcount=1;tmp=subdomain;site=_C
		while not created:
			site,created=Site.objects.get_or_create(domain=tmp,defaults={_H:name})
			if not created:tmp=f"{name+str(mcount)}.{main_domain}";mcount+=1
		subdomain=tmp;print('Begin Create SUB DOMAIN = ',subdomain);debug_mode=getattr(settings,'DEBUG',_A)
		if not debug_mode:create_sub_domain(subdomain)
		srv=Service.objects.create(site_id=site.id,kind=service,agency_id=agency_id,expired_date=tgl_exp,is_active=_b,is_default=_b);template_id=_C;temp=Template.objects.filter(is_frontend=_b)
		for i in temp:
			if service in i.service_option:i.site.add(site);i.save();break
		temp=Template.objects.filter(is_frontend=_A)
		for i in temp:
			if service in i.service_option:i.site.add(site);i.save();break
		print('subdomain',subdomain);group,created=Group.objects.get_or_create(name=subdomain);print(group,created)
		if created:menu_group,created=MenuGroup.objects.get_or_create(site_id=site.id,group_id=group.id)
		group,created=Group.objects.get_or_create(name='Admin');user.groups.add(group);user.save();return redirect(reverse_lazy(_A7))
	return render(request,template,context)
def service_change_ajax(request,service_id):
	print('service_id=',service_id);lst=[];temp=Template.objects.filter(is_frontend=_b)
	for i in temp:
		if service_id in i.service_option:res={};res[_B]=i.id;res['text']=i.name;lst.append(res)
	print('res',lst);return JsonResponse({'results':lst},safe=_A)
class TagsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'tags.html';return super(TagsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(TagsView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_e);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def tags_ajax(request):
	site_id=get_site_id(request);obj=Tags();obj.set_current_language(_L);subquery=Subquery(TagsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));lang=obj.get_current_language();obj2=Tags.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_AA]=Truncator(i.name_id).chars(50);res[_AB]=Truncator(i.name).chars(50);res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def tags_create(request):
	context={};context[_J]=_e;active_page=get_translated_active_page(_e);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=TagsForm(request.POST)
		if form.is_valid():
			tmp=Tags.objects.filter(translations__name=request.POST.get(_H),site_id=site_id)
			if tmp:messages.info(request,mMsgBox.get(_Av));context[_G]=TagsForm()
			else:post=Tags.objects.language(_B).create(name=request.POST.get(_H),status=request.POST.get(_N));post.set_current_language(_L);post.name=request.POST.get(_H);post.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_e))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=TagsForm()
	return render(request,template,context)
def tags_update(request,uuid):
	context={};context[_J]=_e;active_page=get_translated_active_page(_e);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=TagsForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.status=request.POST.get(_N);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_e))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=TagsForm(instance=post)
	return render(request,template,context)
def tags_delete(request,uuid):context={};site_id=get_site_id(request);data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_e))
class LogoView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'logo.html';return super(LogoView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(LogoView,self).get_context_data(*(args),**kwargs);context[_AQ]=_b;active_page=get_translated_active_page(_p);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def logo_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_p).values(_i)[:1]);obj2=Logo.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_A4]=Truncator(i.name).chars(50);res[_j]=i.file_path;res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def logo_create(request):
	context={};context[_J]=_p;active_page=get_translated_active_page(_p);context[_E]=active_page;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_T;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu)
	if request.method==_I:
		form=LogoForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=form.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_p))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=LogoForm();context[_M]=PhotoForm()
	return render(request,template,context)
def logo_update(request,uuid):
	context={};context[_J]=_p;active_page=get_translated_active_page(_p);context[_E]=active_page;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_V;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=LogoForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save()
			if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O));print('DOne')
			messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_p))
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=LogoForm(instance=post)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def logo_delete(request,uuid):context={};site_id=get_site_id(request);data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_p))
class AnnouncementView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'announcement.html';return super(AnnouncementView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(AnnouncementView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_q);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def announcement_ajax(request):
	site_id=get_site_id(request);obj=Announcement();obj.set_current_language(_L);subquery1=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_q).values(_i)[:1]);lang=obj.get_current_language();obj2=Announcement.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_m]=Truncator(i.content_id).chars(50);res[_n]=Truncator(i.content).chars(50);res[_j]=i.file_path;res['Priority']=i.get_priority_display();res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def announcement_create(request):
	context={};context[_J]=_q;active_page=get_translated_active_page(_q);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=AnnouncementForm(request.POST,site_id=site_id);photo=PhotoForm(request.POST)
		if form.is_valid():post=Announcement.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),categories_id=request.POST.get(_f),priority=request.POST.get('priority'),status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.save();save_tags(request.POST.getlist(_e),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_q))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=AnnouncementForm(site_id=site_id);context[_M]=PhotoForm()
	return render(request,template,context)
def announcement_update(request,uuid):
	context={};context[_J]=_q;active_page=get_translated_active_page(_q);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=AnnouncementForm(request.POST,instance=post,site_id=site_id);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.categories_id=request.POST.get(_f);obj.status=request.POST.get(_N);obj.priority=request.POST.get('priority');obj.save();obj.tags.clear();save_tags(request.POST.getlist(_e),obj)
			if photo.is_valid():
				if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_q))
	else:
		context[_G]=AnnouncementForm(instance=post,site_id=site_id)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
		messages.info(request,mMsgBox.get(_X))
	return render(request,template,context)
def announcement_delete(request,uuid):context={};site_id=get_site_id(request);data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_q))
class FasilitiesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'fasilities.html';return super(FasilitiesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(FasilitiesView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_r);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def fasilities_ajax(request):
	site_id=get_site_id(request);obj=Fasilities();obj.set_current_language(_L);subquery1=Subquery(FasilitiesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(FasilitiesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_r).values(_i)[:1]);lang=obj.get_current_language();obj2=Fasilities.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_m]=Truncator(i.content_id).chars(50);res[_n]=Truncator(i.content).chars(50);res[_j]=i.file_path;res[_AR]=i.is_header_text;res[_Aw]=i.order_item;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def fasilities_create(request):
	context={};context[_J]=_r;active_page=get_translated_active_page(_r);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=FasilitiesForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			post=Fasilities.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),is_header_text=form.cleaned_data[_s],status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.is_header_text=form.cleaned_data[_s];post.save()
			if request.POST.get(_O):Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
			messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_r))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=FasilitiesForm();context[_M]=PhotoForm()
	return render(request,template,context)
def fasilities_update(request,uuid):
	context={};context[_J]=_r;active_page=get_translated_active_page(_r);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Fasilities.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=FasilitiesForm(request.POST,instance=post)
		if post_photo:photo=PhotoForm(request.POST,instance=post_photo)
		else:photo=PhotoForm(request.POST)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.is_header_text=form.cleaned_data[_s];obj.status=request.POST.get(_N);obj.save()
			if photo.is_valid():
				if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_r))
	else:
		context[_G]=FasilitiesForm(instance=post)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
		messages.info(request,mMsgBox.get(_X))
	return render(request,template,context)
def fasilities_delete(request,uuid):context={};site_id=get_site_id(request);data=Fasilities.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_r))
class NewsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'news.html';return super(NewsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(NewsView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_t);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def news_ajax(request):
	site_id=get_site_id(request);obj=News();obj.set_current_language(_L);subquery1=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_t).values(_i)[:1]);lang=obj.get_current_language();obj2=News.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_m]=Truncator(i.content_id).chars(50);res[_n]=Truncator(i.content).chars(50);res[_j]=i.file_path;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def news_create(request):
	context={};context[_J]=_t;active_page=get_translated_active_page(_t);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=NewsForm(request.POST,site_id=site_id);photo=PhotoForm(request.POST)
		if form.is_valid():post=News.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),categories_id=request.POST.get(_f),status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.save();save_tags(request.POST.getlist(_e),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_t))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=NewsForm(site_id=site_id);context[_M]=PhotoForm()
	return render(request,template,context)
def news_update(request,uuid):
	context={};context[_J]=_t;active_page=get_translated_active_page(_t);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=NewsForm(request.POST,instance=post,site_id=site_id);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.categories_id=request.POST.get(_f);obj.status=request.POST.get(_N);obj.save();obj.tags.clear();save_tags(request.POST.getlist(_e),obj)
			if photo.is_valid():
				if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_t))
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=NewsForm(instance=post,site_id=site_id)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def news_delete(request,uuid):context={};site_id=get_site_id(request);data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_t))
class ArticleView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'article.html';return super(ArticleView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(ArticleView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_u);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def article_ajax(request):
	site_id=get_site_id(request);obj=Article();obj.set_current_language(_L);subquery1=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_u).values(_i)[:1]);lang=obj.get_current_language();obj2=Article.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_m]=Truncator(i.content_id).chars(50);res[_n]=Truncator(i.content).chars(50);res[_j]=i.file_path;res[_AR]=i.is_header_text;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def article_create(request):
	context={};context[_J]=_u;active_page=get_translated_active_page(_u);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=ArticleForm(request.POST,site_id=site_id);photo=PhotoForm(request.POST)
		if form.is_valid():post=Article.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),categories_id=request.POST.get(_f),status=request.POST.get(_N),is_header_text=form.cleaned_data[_s]);post.set_current_language(_L);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.save();save_tags(request.POST.getlist(_e),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_u))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=ArticleForm(site_id=site_id);context[_M]=PhotoForm()
	return render(request,template,context)
def article_update(request,uuid):
	context={};context[_J]=_u;active_page=get_translated_active_page(_u);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=ArticleForm(request.POST,instance=post,site_id=site_id);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.categories_id=request.POST.get(_f);obj.status=request.POST.get(_N);obj.is_header_text=form.cleaned_data[_s];obj.save();obj.tags.clear();save_tags(request.POST.getlist(_e),obj)
			if photo.is_valid():
				if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_u))
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=ArticleForm(instance=post,site_id=site_id)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def article_delete(request,uuid):context={};site_id=get_site_id(request);data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_u))
class EventsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'events.html';return super(EventsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(EventsView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_v);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def events_ajax(request):
	site_id=get_site_id(request);obj=Events();obj.set_current_language(_L);subquery1=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_v).values(_i)[:1]);lang=obj.get_current_language();obj2=Events.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_m]=Truncator(i.content_id).chars(50);res[_n]=Truncator(i.content).chars(50);res[_j]=i.file_path;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def events_create(request):
	context={};context[_J]=_v;active_page=get_translated_active_page(_v);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=EventsForm(request.POST,site_id=site_id);photo=PhotoForm(request.POST)
		if form.is_valid():post=Events.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),location=request.POST.get(_l),categories_id=request.POST.get(_f),status=request.POST.get(_N),date=request.POST.get('date'),time=request.POST.get('time'));post.set_current_language(_L);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.location=request.POST.get(_l);post.save();save_tags(request.POST.getlist(_e),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_v))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=EventsForm(site_id=site_id);context[_M]=PhotoForm()
	return render(request,template,context)
def events_update(request,uuid):
	context={};context[_J]=_v;active_page=get_translated_active_page(_v);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=EventsForm(request.POST,instance=post,site_id=site_id);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.location=request.POST.get(_l);obj.categories_id=request.POST.get(_f);obj.status=request.POST.get(_N);obj.date=request.POST.get('date');obj.time=request.POST.get('time');obj.save();obj.tags.clear();save_tags(request.POST.getlist(_e),obj)
			if photo.is_valid():
				if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_v))
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=EventsForm(instance=post,site_id=site_id)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def events_delete(request,uuid):context={};site_id=get_site_id(request);data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_v))
class SlideShowView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'slide_show.html';return super(SlideShowView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SlideShowView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_AZ);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def slideshow_ajax(request):
	site_id=get_site_id(request);lst=[];obj=SlideShow();obj.set_current_language(_L);subquery1=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery3=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_AS));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model='slideshow').values(_i)[:1]);lang=obj.get_current_language();obj2=SlideShow.objects.language(lang).filter(site_id=site_id).distinct().annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(sub_title_id=subquery3).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res['Sub Title (id)']=Truncator(i.sub_title_id).chars(50);res['Sub Title (en)']=Truncator(i.sub_title).chars(50);res[_m]=Truncator(i.content_id).chars(50);res[_n]=Truncator(i.content).chars(50);res[_j]=i.file_path;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def slideshow_create(request):
	context={};context[_J]=_AC;active_page=get_translated_active_page(_AZ);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=SlideShowForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=SlideShow.objects.language(_B).create(title=request.POST.get(_F),sub_title=request.POST.get(_AS),content=request.POST.get(_K),status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);sub_title=request.POST.get(_AS);post.content=request.POST.get(_K);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_AC))
		else:print(_A3);context[_G]=SlideShowForm();context[_M]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_U));context[_G]=SlideShowForm();context[_M]=PhotoForm()
	return render(request,template,context)
def slideshow_update(request,uuid):
	context={};context[_J]=_AC;active_page=get_translated_active_page(_AZ);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.first()
	if request.method==_I:
		form=SlideShowForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_AS);obj.content=request.POST.get(_K);obj.status=request.POST.get(_N);obj.save()
			if request.POST.get(_O):obj.photo.clear();Photo.objects.create(content_object=obj,file_path=request.POST.get(_O))
			else:print('photo not valid')
			messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_AC))
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=SlideShowForm(instance=post)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def slideshow_delete(request,uuid):context={};site_id=get_site_id(request);data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AC))
class DailyAlertView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'daily_alert.html';return super(DailyAlertView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DailyAlertView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_Aa);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def dailyalert_ajax(request):
	site_id=get_site_id(request);lst=[];obj=DailyAlert();obj.set_current_language(_L);subquery1=Subquery(DailyAlertTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_A5));lang=obj.get_current_language();obj2=DailyAlert.objects.language(lang).filter(site_id=site_id).annotate(alert_id=subquery1)
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res['Alert (id)']=Truncator(i.alert_id).chars(50);res['Alert (en)']=Truncator(i.alert).chars(50);res[_AD]=Truncator(i.link).chars(50);res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def dailyalert_create(request):
	context={};context[_J]=_AE;active_page=get_translated_active_page(_Aa);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=DailyAlertForm(request.POST)
		if form.is_valid():post=DailyAlert.objects.language(_B).create(alert=request.POST.get(_A5),link=request.POST.get(_w),status=request.POST.get(_N));post.set_current_language(_L);post.alert=request.POST.get(_A5);post.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_A5)));return redirect(reverse_lazy(_AE))
		else:print(_A3);context[_G]=DailyAlertForm()
	else:messages.info(request,mMsgBox.get(_U));context[_G]=DailyAlertForm()
	return render(request,template,context)
def dailyalert_update(request,uuid):
	context={};context[_J]=_AE;active_page=get_translated_active_page(_Aa);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=DailyAlertForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.alert=request.POST.get(_A5);obj.link=request.POST.get(_w);obj.status=request.POST.get(_N);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_A5)));return redirect(reverse_lazy(_AE))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=DailyAlertForm(instance=post)
	return render(request,template,context)
def dailyalert_delete(request,uuid):context={};site_id=get_site_id(request);data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.alert;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AE))
class GreetingView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'greeting.html';return super(GreetingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(GreetingView,self).get_context_data(*(args),**kwargs);context[_AQ]=_b;active_page=get_translated_active_page(_x);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def greeting_ajax(request):
	site_id=get_site_id(request);obj=Greeting();obj.set_current_language(_L);subquery1=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_x).values(_i)[:1]);lang=obj.get_current_language();obj2=Greeting.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_m]=Truncator(i.content_id).chars(50);res[_n]=Truncator(i.content).chars(50);res[_j]=i.file_path;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def greeting_create(request):
	context={};context[_J]=_x;active_page=get_translated_active_page(_x);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=GreetingForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Greeting.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),name=request.POST.get(_H),designation=request.POST.get(_Ab),status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.name=request.POST.get(_H);post.designation=request.POST.get(_Ab);post.save();save_tags(request.POST.getlist(_e),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_x))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=GreetingForm();context[_M]=PhotoForm()
	return render(request,template,context)
def greeting_update(request,uuid):
	context={};context[_J]=_x;active_page=get_translated_active_page(_x);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=GreetingForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.name=request.POST.get(_H);obj.designation=request.POST.get(_Ab);obj.status=request.POST.get(_N);obj.save()
			if photo.is_valid():
				if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_x))
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=GreetingForm(instance=post)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def greeting_delete(request,uuid):context={};site_id=get_site_id(request);data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_x))
class PagesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'pages.html';return super(PagesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PagesView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_y);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def pages_ajax(request):
	site_id=get_site_id(request);obj=Pages();obj.set_current_language(_L);subquery1=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_y).values(_i)[:1]);lang=obj.get_current_language();obj2=Pages.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_m]=Truncator(i.content_id).chars(50);res[_n]=Truncator(i.content).chars(50);res[_j]=i.file_path;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def menu_already_used(site_id,menu_id):
	A='translations__title';lang=get_active_language_choices()[0];pages=Pages.objects.language(lang).filter(site_id=site_id,menu_id=menu_id).values(A)
	if pages:return pages[0][A]
	return _C
def pages_create(request):
	context={};context[_J]=_y;active_page=get_translated_active_page(_y);context[_E]=active_page;context[_AT]=_Ax;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=PagesForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			menu_id=request.POST.get(_AF)
			if menu_id:
				menu_name_already_used=menu_already_used(site_id,menu_id)
				if not menu_name_already_used:post=Pages.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),menu_id=menu_id,status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.save();save_tags(request.POST.getlist(_e),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_O));obj=Menu.objects.get(id=menu_id);obj.link=_Ay+post.slug;obj.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_y))
				else:messages.info(request,mMsgBox.get(_AU,'Menu already used by '+menu_name_already_used));context[_G]=PagesForm(request.POST);context[_M]=PhotoForm(request.POST)
			else:messages.info(request,mMsgBox.get(_AU,_Az));context[_G]=PagesForm(request.POST);context[_M]=PhotoForm(request.POST)
	else:messages.info(request,mMsgBox.get(_U));context[_G]=PagesForm();context[_M]=PhotoForm()
	return render(request,template,context)
def pages_update(request,uuid):
	context={};context[_J]=_y;active_page=get_translated_active_page(_y);context[_E]=active_page;context[_AT]=_Ax;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	select2_update={_B:post.menu_id,'text':post.menu.name if post.menu else _C};context[_A_]=select2_update
	if request.method==_I:
		form=PagesForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			menu_id=request.POST.get(_AF)
			if menu_id:
				lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.menu_id=menu_id;obj.status=request.POST.get(_N);obj.save();obj.tags.clear();save_tags(request.POST.getlist(_e),obj)
				if photo.is_valid():
					if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
				obj=Menu.objects.get(id=menu_id);obj.link=_Ay+post.slug;obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_y))
			else:
				messages.info(request,mMsgBox.get(_AU,_Az));context[_G]=PagesForm(request.POST,instance=post)
				if post_photo:context[_M]=PhotoForm(request.POST,instance=post_photo)
				else:context[_M]=PhotoForm()
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=PagesForm(instance=post)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def pages_delete(request,uuid):context={};site_id=get_site_id(request);data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_y))
class SocialMediaView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'social_media.html';return super(SocialMediaView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(SocialMediaView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_Ac);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def socialmedia_ajax(request):
	site_id=get_site_id(request);obj2=SocialMedia.objects.filter(site_id=site_id);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res['Kind']=i.get_kind_display();res[_AD]=Truncator(i.link).chars(70);res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def socialmedia_create(request):
	context={};context[_J]=_AG;active_page=get_translated_active_page(_Ac);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=SocialMediaForm(request.POST)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_w)));return redirect(reverse_lazy(_AG))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=SocialMediaForm()
	return render(request,template,context)
def socialmedia_update(request,uuid):
	context={};context[_J]=_AG;active_page=get_translated_active_page(_Ac);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=SocialMediaForm(request.POST,instance=post)
		if form.is_valid():post=form.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_w)));return redirect(reverse_lazy(_AG))
	else:
		messages.info(request,mMsgBox.get(_X))
		if post:context[_G]=SocialMediaForm(instance=post)
	return render(request,template,context)
def socialmedia_delete(request,uuid):context={};site_id=get_site_id(request);data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.link;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AG))
class HowItWorksView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'how_it_works.html';return super(HowItWorksView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(HowItWorksView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_Ad);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def howitworks_ajax(request):
	site_id=get_site_id(request);obj=HowItWorks();subquery=Subquery(HowItWorksTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(HowItWorksTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));lang=obj.get_current_language();obj2=HowItWorks.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery).annotate(content_id=subquery2);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(70);res[_h]=Truncator(i.title).chars(70);res[_m]=Truncator(i.content_id).chars(70);res[_n]=Truncator(i.content).chars(70);res['Icon']=i.icon;res[_AR]=i.is_header_text;res[_Aw]=i.order_item;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def howitworks_create(request):
	context={};context[_J]=_AH;active_page=get_translated_active_page(_Ad);print(_E,active_page);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=HowItWorksForm(request.POST)
		if form.is_valid():post=HowItWorks.objects.language(_B).create(icon=request.POST.get(_P),title=request.POST.get(_F),content=request.POST.get(_K),is_header_text=form.cleaned_data[_s],status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_AH))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=HowItWorksForm()
	return render(request,template,context)
def howitworks_update(request,uuid):
	context={};context[_J]=_AH;active_page=get_translated_active_page(_Ad);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=HowItWorks.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=HowItWorksForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.icon=request.POST.get(_P);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.is_header_text=form.cleaned_data[_s];obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_AH))
	else:
		messages.info(request,mMsgBox.get(_X))
		if post:context[_G]=HowItWorksForm(instance=post)
	return render(request,template,context)
def howitworks_delete(request,uuid):context={};site_id=get_site_id(request);data=HowItWorks.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AH))
class PhotoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'photo_gallery.html';return super(PhotoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PhotoGalleryView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_Ae);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def photogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=PhotoGallery();obj.set_current_language(_L);subquery1=Subquery(PhotoGalleryTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model='photogallery').values(_i)[:1]);lang=obj.get_current_language();obj2=PhotoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_j]=i.file_path;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def photogallery_create(request):
	context={};context[_J]=_AI;active_page=get_translated_active_page(_Ae);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=PhotoGalleryForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=PhotoGallery.objects.language(_B).create(title=request.POST.get(_F),status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_AI))
		else:print(_A3);context[_G]=PhotoGalleryForm();context[_M]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_U));context[_G]=PhotoGalleryForm();context[_M]=PhotoForm()
	return render(request,template,context)
def photogallery_update(request,uuid):
	context={};context[_J]=_AI;active_page=get_translated_active_page(_Ae);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=PhotoGalleryForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.status=request.POST.get(_N);obj.save()
			if photo.is_valid():
				if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_AI))
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=PhotoGalleryForm(instance=post)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def photogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AI))
def get_video_id(url_video):
	tmp=url_video.split('/')
	if tmp:return tmp[len(tmp)-1]
def download_thumbnail(request,video_id):download_url='https://img.youtube.com/vi/'+video_id+'/mqdefault.jpg';return download_image(request,download_url)
class VideoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'video_gallery.html';return super(VideoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(VideoGalleryView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_Af);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def videogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=VideoGallery();obj.set_current_language(_L);subquery1=Subquery(VideoGalleryTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model='videogallery').values(_i));lang=obj.get_current_language();obj2=VideoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_j]=i.file_path;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def videogallery_create(request):
	context={};context[_J]=_AJ;active_page=get_translated_active_page(_Af);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=VideoGalleryForm(request.POST)
		if form.is_valid():post=VideoGallery.objects.language(_B).create(title=request.POST.get(_F),embed=request.POST.get(_AV),status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.save();video_id=get_video_id(post.embed_video);file_path=download_thumbnail(request,video_id);Photo.objects.create(content_object=post,file_path=file_path);messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_AJ))
		else:print(_A3);context[_G]=VideoGalleryForm()
	else:messages.info(request,mMsgBox.get(_U));context[_G]=VideoGalleryForm()
	return render(request,template,context)
def videogallery_update(request,uuid):
	context={};context[_J]=_AJ;active_page=get_translated_active_page(_Af);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=VideoGalleryForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.embed=request.POST.get(_AV);obj.status=request.POST.get(_N);obj.save();video_id=get_video_id(obj.embed_video);file_path=download_thumbnail(request,video_id);obj.photo.clear();Photo.objects.create(content_object=obj,file_path=file_path);messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_AJ))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=VideoGalleryForm(instance=post)
	return render(request,template,context)
def videogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AJ))
class RelatedLinkView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'related_link.html';return super(RelatedLinkView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(RelatedLinkView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_Ag);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def relatedlink_ajax(request):
	site_id=get_site_id(request);lst=[];obj=RelatedLink();obj.set_current_language(_L);subquery1=Subquery(RelatedLinkTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));lang=obj.get_current_language();obj2=RelatedLink.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1)
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_AA]=Truncator(i.name_id).chars(50);res[_AB]=Truncator(i.name).chars(50);res[_AD]=Truncator(i.link).chars(70);res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def relatedlink_create(request):
	context={};context[_J]=_AK;active_page=get_translated_active_page(_Ag);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=RelatedLinkForm(request.POST)
		if form.is_valid():post=RelatedLink.objects.language(_B).create(name=request.POST.get(_H),link=request.POST.get(_w),status=request.POST.get(_N));post.set_current_language(_L);post.name=request.POST.get(_H);post.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_AK))
		else:print(_A3);context[_G]=RelatedLinkForm()
	else:messages.info(request,mMsgBox.get(_U));context[_G]=RelatedLinkForm()
	return render(request,template,context)
def relatedlink_update(request,uuid):
	context={};context[_J]=_AK;active_page=get_translated_active_page(_Ag);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=RelatedLinkForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.link=request.POST.get(_w);obj.status=request.POST.get(_N);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_AK))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=RelatedLinkForm(instance=post)
	return render(request,template,context)
def relatedlink_delete(request,uuid):context={};site_id=get_site_id(request);data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AK))
class DocumentView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'document.html';return super(DocumentView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DocumentView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_A1);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def document_ajax(request):
	site_id=get_site_id(request);lst=[];obj=Document();obj.set_current_language(_L);subquery1=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));subquery2=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));lang=obj.get_current_language();obj2=Document.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1).annotate(content_id=subquery2)
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_AA]=Truncator(i.name_id).chars(20);res[_AB]=Truncator(i.name).chars(20);res['content (id)']=Truncator(i.content_id).chars(30);res['content (en)']=Truncator(i.content).chars(30);res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def document_create(request):
	context={};context[_J]=_A1;active_page=get_translated_active_page(_A1);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=DocumentForm(request.POST,request.FILES);print('form=',form)
		if form.is_valid():print('categories = ',request.POST.get(_f));print('file = ',request.FILES.get(_AW));post=Document.objects.language(_B).create(name=request.POST.get(_H),content=request.POST.get(_K),file_path_doc=request.FILES.get(_AW),categories_id=request.POST.get(_f),status=request.POST.get(_N));post.set_current_language(_L);post.name=request.POST.get(_H);post.content=request.POST.get(_K);post.save();print(_B0,post.file_path_doc.path);post.size=os.stat(post.file_path_doc.path).st_size;post.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_A1))
		else:messages.info(request,mMsgBox.get('form_fail'));context[_G]=DocumentForm()
	else:messages.info(request,mMsgBox.get(_U));context[_G]=DocumentForm()
	return render(request,template,context)
def document_update(request,uuid):
	context={};context[_J]=_A1;active_page=get_translated_active_page(_A1);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=DocumentForm(request.POST,request.FILES,instance=post)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.content=request.POST.get(_K)
			if request.FILES.get(_AW):obj.file_path_doc=request.FILES.get(_AW)
			obj.status=request.POST.get(_N);obj.categories_id=request.POST.get(_f);obj.save();print(_B0,obj.file_path_doc.path);obj.size=os.stat(obj.file_path_doc.path).st_size;obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_A1))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=DocumentForm(instance=post)
	return render(request,template,context)
def document_delete(request,uuid):context={};site_id=get_site_id(request);data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A1))
class MenuView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'menu.html';return super(MenuView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(MenuView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_D);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def get_menu_group(site_id):
	A='Frontend Site ';site_name=Site.objects.get(pk=site_id).domain;menugroup=MenuGroup.objects.filter(site=site_id,kind=1);print('menugroup = ',menugroup)
	if menugroup:return menugroup[0].id
	else:
		lang1=get_active_language_choices()[0];lang2=_B
		if lang1==_B:lang2=_L
		post=MenuGroup.objects.language(lang1).create(site_id=site_id,kind=1,name=A+site_name);post.set_current_language(lang2);post.name=A+site_name;post.save();return post.id
def menu_ajax(request):
	A='Name (';site_id=get_site_id(request);group_id=get_menu_group(site_id);print('group_id = ',group_id);lst=[]
	if group_id:
		lang=get_active_language_choices()[0];lang2=_B
		if lang==_B:lang2=_L
		menu=Menus(menu_group=group_id,kinds=1)
		if menu:
			obj2=menu.get_menus()
			for i in obj2:
				tmp='';lvl=i['level']
				while lvl>0:tmp+='<i class="fa fa-long-arrow-right"></i> &nbsp;&nbsp;&nbsp;&nbsp; ';lvl-=1
				res={};res[_P]=_C;res[_Q]=i[_Q];res[_R]=_C;res[A+lang+')']=Truncator(i[_H]).chars(50);res[A+lang2+')']=Menu.objects.language(lang2).get(pk=i[_B]).name;res['Tree']=tmp+Truncator(i[_H]).chars(70);res[_AD]=Truncator(i[_w]).chars(70);res['Order']=i[_Ah];res['Icon']=Truncator(i[_P]).chars(50);res['Visibled']=Truncator(i[_Ai]).chars(50);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def menu_create(request):
	context={};context[_J]=_D;active_page=get_translated_active_page(_D);context[_E]=active_page;context[_AT]=_B1;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);group_id=get_menu_group(site_id);menu_group=MenuGroup.objects.get(id=group_id);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=MenuForm(request.POST)
		if form.is_valid():form_clean=form.cleaned_data;print('select2_menu = ',request.POST.get(_AF));post=Menu.objects.language(_B).create(name=form_clean[_H],parent_id=request.POST.get(_AF),link=form_clean[_w],order_menu=form_clean[_Ah],icon=form_clean[_P],is_visibled=form_clean[_Ai],is_external=form_clean[_B2]);post.menu_group.add(menu_group);post.set_current_language(_L);post.name=form_clean[_H];post.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_D))
		else:print(_A3);context[_G]=MenuForm()
	else:messages.info(request,mMsgBox.get(_U));context[_G]=MenuForm()
	return render(request,template,context)
def menu_update(request,uuid):
	context={};context[_J]=_D;active_page=get_translated_active_page(_D);context[_E]=active_page;context[_AT]=_B1;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Menu.objects.filter(uuid=uuid);post=get_object_or_404(data);select2_update={_B:post.parent_id,'text':post.parent.name if post.parent else _C};context[_A_]=select2_update
	if request.method==_I:
		form=MenuForm(request.POST,instance=post)
		if form.is_valid():form_clean=form.cleaned_data;lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.name=form_clean[_H];obj.parent_id=request.POST.get(_AF);obj.link=form_clean[_w];obj.order_menu=form_clean[_Ah];obj.icon=form_clean[_P];obj.is_visibled=form_clean[_Ai];obj.is_external=form_clean[_B2];obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_D))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=MenuForm(instance=post)
	return render(request,template,context)
def menu_delete(request,uuid):context={};site_id=get_site_id(request);data=Menu.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_D))
def site_name_update(site_id,name):site=Site.objects.get(id=site_id);site.name=name;site.save()
def get_translated_active_page(active_page):
	ret=active_page;lang=get_active_language_choices()[0];obj=Menu.objects.language(lang).filter(translations__name__iexact=active_page)
	if obj:ret=obj[0].name
	ret=ret.replace(' ','_');ret=ret.lower();print('get_translated_active_page = ',ret);return ret
class AgencyView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'agency.html';return super(AgencyView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(AgencyView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_k);context[_E]=active_page;context[_AQ]=_b;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def agency_ajax(request):
	site_id=get_site_id(request);obj=Agency();obj.set_current_language(_L);service=Service.objects.filter(site_id=site_id).values_list(_k,flat=_b);subquery1=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_A8));subquery2=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_A9));lang=obj.get_current_language();obj2=Agency.objects.language(lang).filter(id=service[0]).annotate(address_id=subquery1).annotate(notes_id=subquery2);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_A4]=Truncator(i.name).chars(50);res['Address (id)']=Truncator(i.address_id).chars(50);res['Address (en)']=Truncator(i.address).chars(50);res[_B3]=Truncator(i.notes_id).chars(50);res[_B4]=Truncator(i.notes).chars(50);res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def agency_create(request):
	context={};context[_J]=_k;active_page=get_translated_active_page(_k);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=AgencyForm(request.POST)
		if form.is_valid():post=Agency.objects.language(_B).create(address=request.POST.get(_A8),notes=request.POST.get(_A9),name=request.POST.get(_H),email=request.POST.get(_AX),phone=request.POST.get('phone'),fax=request.POST.get('fax'),whatsapp=request.POST.get('whatsapp'));post.set_current_language(_L);post.address=request.POST.get(_A8);post.notes=request.POST.get(_A9);post.save();site_name_update(site_id,request.POST.get(_H));print(_B5);messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_k))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=AgencyForm()
	return render(request,template,context)
def agency_update(request,uuid):
	context={};context[_J]=_k;active_page=get_translated_active_page(_k);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=AgencyForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.address=request.POST.get(_A8);obj.notes=request.POST.get(_A9);obj.name=request.POST.get(_H);obj.email=request.POST.get(_AX);obj.phone=request.POST.get('phone');obj.fax=request.POST.get('fax');obj.whatsapp=request.POST.get('whatsapp');obj.status=request.POST.get(_N);obj.save();print('site name begin update');site_name_update(site_id,request.POST.get(_H));print(_B5);messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_k))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=AgencyForm(instance=post)
	return render(request,template,context)
def agency_delete(request,uuid):context={};site_id=get_site_id(request);data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_k))
class CategoriesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'categories.html';return super(CategoriesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(CategoriesView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_f);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def categories_ajax(request):
	site_id=get_site_id(request);obj=Categories();obj.set_current_language(_L);subquery1=Subquery(CategoriesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));lang=obj.get_current_language();obj2=Categories.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_AA]=Truncator(i.name_id).chars(50);res[_AB]=Truncator(i.name).chars(50);res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def categories_create(request):
	context={};context[_J]=_f;active_page=get_translated_active_page(_f);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=CategoriesForm(request.POST)
		if form.is_valid():post=Categories.objects.language(_B).create(name=request.POST.get(_H),status=request.POST.get(_N));post.set_current_language(_L);post.name=request.POST.get(_H);post.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_f))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=CategoriesForm()
	return render(request,template,context)
def categories_update(request,uuid):
	context={};context[_J]=_f;active_page=get_translated_active_page(_f);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=CategoriesForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.status=request.POST.get(_N);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_f))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=CategoriesForm(instance=post)
	return render(request,template,context)
def categories_delete(request,uuid):context={};site_id=get_site_id(request);data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_f))
class ProductView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'product.html';return super(ProductView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(ProductView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_z);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def product_ajax(request):
	site_id=get_site_id(request);obj=Product();obj.set_current_language(_L);subquery1=Subquery(ProductTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));subquery2=Subquery(ProductTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery3=Subquery(ProductTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_z).values(_i)[:1]);lang=obj.get_current_language();obj2=Product.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1).annotate(title_id=subquery2).annotate(content_id=subquery3).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_AA]=Truncator(i.name_id).chars(50);res[_AB]=Truncator(i.name).chars(50);res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_m]=Truncator(i.content_id).chars(50);res[_n]=Truncator(i.content).chars(50);res[_AR]=i.is_header_text;res[_j]=i.file_path;res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def product_create(request):
	context={};context[_J]=_z;active_page=get_translated_active_page(_z);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		photo=PhotoForm(request.POST);form=ProductForm(request.POST)
		if form.is_valid():post=Product.objects.language(_B).create(name=request.POST.get(_H),title=request.POST.get(_F),content=request.POST.get(_K),is_header_text=form.cleaned_data[_s],status=request.POST.get(_N));post.set_current_language(_L);post.name=request.POST.get(_H);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_z))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=ProductForm();context[_M]=PhotoForm()
	return render(request,template,context)
def product_update(request,uuid):
	context={};context[_J]=_z;active_page=get_translated_active_page(_z);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Product.objects.filter(uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	photo=_C
	if request.method==_I:
		if post_photo:photo=PhotoForm(request.POST,instance=post_photo)
		form=ProductForm(request.POST,instance=post)
		if form.is_valid():
			lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.is_header_text=form.cleaned_data[_s];obj.status=request.POST.get(_N);obj.save();print('photo file path',request.POST.get(_O))
			if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O))
			messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_z))
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=ProductForm(instance=post)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def product_delete(request,uuid):context={};site_id=get_site_id(request);data=Product.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_z))
def menu_lookup_ajax(request):
	A='translations__name';lang=get_active_language_choices()[0];site_id=get_site_id(request);group_id=get_menu_group(site_id);print('menugroup=',group_id,lang);search=request.GET.get('search')
	if search:object_list=Menu.objects.translated(lang).filter(menu_group__id=group_id).filter(translations__name__icontains=search).values(_B,text=F(A))
	else:object_list=Menu.objects.translated(lang).filter(menu_group__id=group_id).values(_B,text=F(A))
	return JsonResponse({'results':list(object_list),'pagination':{'more':_b}},safe=_A)
class TemplateOwnerView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'template_owner.html';return super(TemplateOwnerView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(TemplateOwnerView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_Aj);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def templateowner_ajax(request):
	site_id=get_site_id(request);obj2=TemplateOwner.objects.all();lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_A4]=Truncator(i.name).chars(50);res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def templateowner_create(request):
	context={};context[_J]=_AL;active_page=get_translated_active_page(_Aj);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=TemplateOwnerForm(request.POST)
		if form.is_valid():post=TemplateOwner.objects.create(name=request.POST.get(_H));messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_AL))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=TemplateOwnerForm()
	return render(request,template,context)
def templateowner_update(request,uuid):
	context={};context[_J]=_AL;active_page=get_translated_active_page(_Aj);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=TemplateOwner.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=TemplateOwnerForm(request.POST,instance=post)
		if form.is_valid():obj=data.get();obj.name=request.POST.get(_H);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_AL))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=TemplateOwnerForm(instance=post)
	return render(request,template,context)
def templateowner_delete(request,uuid):context={};site_id=get_site_id(request);data=TemplateOwner.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AL))
class TemplateView_(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'template.html';return super(TemplateView_,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(TemplateView_,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_Ak);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def template_ajax(request):
	site_id=get_site_id(request);obj2=Template.objects.all();lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_A4]=Truncator(i.name).chars(50);res['Relative Path']=Truncator(i.rel_path).chars(50);res['Template Owner']=Truncator(i.template_owner).chars(50);res['Frontend']=Truncator(i.is_frontend).chars(50);res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def template_create(request):
	context={};context[_J]=_AM;active_page=get_translated_active_page(_Ak);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=TemplateForm(request.POST)
		if form.is_valid():tmp=request.POST.get(_Al);post=Template.objects.create(name=request.POST.get(_H),rel_path=request.POST.get('rel_path'),is_frontend=bool(request.POST.get(_B6)),template_owner_id=tmp if tmp else _C);messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_AM))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=TemplateForm()
	return render(request,template,context)
def template_update(request,uuid):
	context={};context[_J]=_AM;active_page=get_translated_active_page(_Ak);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Template.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=TemplateForm(request.POST,instance=post)
		if form.is_valid():
			obj=data.get();tmp=request.POST.get(_Al);obj.name=request.POST.get(_H);obj.rel_path=request.POST.get('rel_path');obj.is_frontend=bool(request.POST.get(_B6))
			if tmp:obj.template_owner_id=request.POST.get(_Al)
			obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_AM))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=TemplateForm(instance=post)
	return render(request,template,context)
def template_delete(request,uuid):context={};site_id=get_site_id(request);data=Template.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AM))
class ModelListView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'model_list.html';return super(ModelListView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(ModelListView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_Am);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def modellist_ajax(request):
	site_id=get_site_id(request);obj2=ModelList.objects.all();lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_A4]=Truncator(i.name).chars(50);res['Description']=Truncator(i.description).chars(50);res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def modellist_create(request):
	context={};context[_J]=_AN;active_page=get_translated_active_page(_Am);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=ModelListForm(request.POST)
		if form.is_valid():post=ModelList.objects.create(name=request.POST.get(_H),description=request.POST.get(_A6),status=request.POST.get(_N));messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_AN))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=ModelListForm()
	return render(request,template,context)
def modellist_update(request,uuid):
	context={};context[_J]=_AN;active_page=get_translated_active_page(_Am);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=ModelList.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=ModelListForm(request.POST,instance=post)
		if form.is_valid():obj=data.get();obj.name=request.POST.get(_H);obj.description=request.POST.get(_A6);obj.status=request.POST.get(_N);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_AN))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=ModelListForm(instance=post)
	return render(request,template,context)
def modellist_delete(request,uuid):context={};site_id=get_site_id(request);data=ModelList.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AN))
def is_have_group(request,*group_names):
	u=User.objects.filter(pk=request.user.id)
	if u:
		u=u.get()
		if bool(u.groups.filter(name__in=group_names))|u.is_superuser:return _b
	return _A
class ServiceView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'service.html';return super(ServiceView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(ServiceView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_o);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def service_ajax(request):
	is_super_admin=is_have_group(request,['Super Admin'])
	if is_super_admin:obj2=Service.objects.all()
	else:site_id=get_site_id(request);obj2=Service.objects.filter(site_id=site_id)
	lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res['Domain']=i.site.domain;res['Service Kind']=i.get_kind_display();res['Agency']=Truncator(i.agency).chars(50);res['Expired Date']=get_natural_datetime(i.expired_date);res['Active']=i.is_active;res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def service_create(request):
	context={};context[_J]=_o;active_page=get_translated_active_page(_o);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		print('request.post');form=ServiceForm(request.POST)
		if form.is_valid():print('form is valid');post=Service.objects.create(site_id=request.POST.get(_AO),kind=request.POST.get('kind'),agency_id=request.POST.get(_k),is_active=bool(request.POST.get(_B7)),expired_date=request.POST.get(_B8));print('post=',post);messages.info(request,mMsgBox.get(_a,request.POST.get(_H)));return redirect(reverse_lazy(_o))
		else:print('form-',form)
	else:print('else request.post');messages.info(request,mMsgBox.get(_U));context[_G]=ServiceForm()
	return render(request,template,context)
def service_update(request,uuid):
	context={};context[_J]=_o;active_page=get_translated_active_page(_o);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Service.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=ServiceForm(request.POST,instance=post)
		if form.is_valid():obj=data.get();obj.site_id=request.POST.get(_AO);obj.kind=request.POST.get('kind');obj.agency_id=request.POST.get(_k);obj.is_active=bool(request.POST.get(_B7));obj.expired_date=request.POST.get(_B8);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_o))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=ServiceForm(instance=post)
	return render(request,template,context)
def service_delete(request,uuid):context={};site_id=get_site_id(request);data=Service.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_o))
class BannerView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'banner.html';return super(BannerView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(BannerView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_A0);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def banner_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_A0).values(_i));obj2=Banner.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res['Priority']=i.get_priority_display();res[_j]=i.file_path;res[_AD]=Truncator(i.link).chars(70);res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def banner_create(request):
	context={};context[_J]=_A0;active_page=get_translated_active_page(_A0);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=BannerForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=form.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_O));messages.info(request,mMsgBox.get(_a,request.POST.get('position')));return redirect(reverse_lazy(_A0))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=BannerForm();context[_M]=PhotoForm()
	return render(request,template,context)
def banner_update(request,uuid):
	context={};context[_J]=_A0;active_page=get_translated_active_page(_A0);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Banner.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=BannerForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save()
			if request.POST.get(_O):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_O));print('DOne')
			messages.info(request,mMsgBox.get(_W,request.POST.get('position')));return redirect(reverse_lazy(_A0))
	else:
		messages.info(request,mMsgBox.get(_X));context[_G]=BannerForm(instance=post)
		if post_photo:context[_M]=PhotoForm(instance=post_photo)
		else:context[_M]=PhotoForm()
	return render(request,template,context)
def banner_delete(request,uuid):context={};site_id=get_site_id(request);data=Banner.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.position;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A0))
class LocationView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'location.html';return super(LocationView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(LocationView,self).get_context_data(*(args),**kwargs);context[_AQ]=_b;active_page=get_translated_active_page(_l);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def location_ajax(request):
	site_id=get_site_id(request);lst=[];obj=Location();obj.set_current_language(_L);subquery1=Subquery(LocationTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));lang=obj.get_current_language();obj2=Location.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1)
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);tmp=Truncator(i.embed).chars(100);tmp=tmp.replace('<',' ');tmp=tmp.replace('>',' ');res['Embed']=tmp;res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def location_create(request):
	context={};context[_J]=_l;active_page=get_translated_active_page(_l);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=LocationForm(request.POST)
		if form.is_valid():post=Location.objects.language(_B).create(title=request.POST.get(_F),embed=request.POST.get(_AV),status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_l))
		else:print(_A3);context[_G]=LocationForm()
	else:messages.info(request,mMsgBox.get(_U));context[_G]=LocationForm()
	return render(request,template,context)
def location_update(request,uuid):
	context={};context[_J]=_l;active_page=get_translated_active_page(_l);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=Location.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=LocationForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.embed=request.POST.get(_AV);obj.status=request.POST.get(_N);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_F)));return redirect(reverse_lazy(_l))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=LocationForm(instance=post)
	return render(request,template,context)
def location_delete(request,uuid):context={};site_id=get_site_id(request);data=Location.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_l))
class WhyUsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'why_us.html';return super(WhyUsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(WhyUsView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_An);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def whyus_ajax(request):
	site_id=get_site_id(request);obj=WhyUs();obj.set_current_language(_L);subquery=Subquery(WhyUsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(WhyUsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_A6));lang=obj.get_current_language();obj2=WhyUs.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery).annotate(description_id=subquery2);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res[_g]=Truncator(i.title_id).chars(50);res[_h]=Truncator(i.title).chars(50);res[_B3]=Truncator(i.description_id).chars(100);res[_B4]=Truncator(i.description).chars(100);res['Icon']=Truncator(i.icon).chars(20);res[_c]=i.get_status_display();res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def whyus_create(request):
	context={};context[_J]=_AP;active_page=get_translated_active_page(_An);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=WhyUsForm(request.POST)
		if form.is_valid():
			tmp=WhyUs.objects.filter(translations__title=request.POST.get(_F),site_id=site_id)
			if tmp:messages.info(request,mMsgBox.get(_Av));context[_G]=WhyUsForm()
			else:post=WhyUs.objects.language(_B).create(title=request.POST.get(_F),description=request.POST.get(_A6),icon=request.POST.get(_P),status=request.POST.get(_N));post.set_current_language(_L);post.title=request.POST.get(_F);post.description=request.POST.get(_A6);post.icon=request.POST.get(_P);post.save();messages.info(request,mMsgBox.get(_a,request.POST.get(_F)));return redirect(reverse_lazy(_AP))
	else:messages.info(request,mMsgBox.get(_U));context[_G]=WhyUsForm()
	return render(request,template,context)
def whyus_update(request,uuid):
	context={};context[_J]=_AP;active_page=get_translated_active_page(_An);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=WhyUs.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=WhyUsForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_d);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.description=request.POST.get(_A6);obj.icon=request.POST.get(_P);obj.status=request.POST.get(_N);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_AP))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=WhyUsForm(instance=post)
	return render(request,template,context)
def whyus_delete(request,uuid):context={};site_id=get_site_id(request);data=WhyUs.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_AP))
class UserView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'user.html';return super(UserView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(UserView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_A2);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def user_ajax(request):
	site_id=get_site_id(request);obj2=User.objects.filter(site_id=site_id);lst=[]
	for i in obj2:res={};res[_P]=_C;res[_Q]=i.uuid;res[_R]=i.updated_at;res['Email']=Truncator(i.email).chars(50);res[_A4]=Truncator(i.name).chars(50);res['Confirm']=i.email_confirmed;res['Site']=i.site.domain;res[_Z]=get_natural_datetime(i.updated_at);res[_S]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def user_create(request):
	context={};context[_J]=_A2;active_page=get_translated_active_page(_A2);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_T
	if request.method==_I:
		form=CustomUserCreationForm(request.POST)
		if form.is_valid():user=form.save(commit=_A);user.site_id=site_id;user.save();current_site=get_current_site(request);subject='Confirm Your Email Address';uid=urlsafe_base64_encode(force_bytes(user.pk));token=account_activation_token.make_token(user);message=render_to_string('account_activation_email.html',{_A2:user,'domain':current_site.domain,'uid':uid,'token':token});email_from=getattr(settings,'EMAIL_HOST_USER','noreply@gmail.com');send_email(email_from,'suratiwan03@gmail.com',subject,message);print('email send complete!');return redirect('account_activation_sent')
		else:messages.info(request,mMsgBox.get(_AU,request.POST.get(_AX)));context[_G]=CustomUserCreationForm(request.POST)
	else:messages.info(request,mMsgBox.get(_U));context[_G]=CustomUserCreationForm()
	return render(request,template,context)
def user_update(request,uuid):
	context={};context[_J]=_A2;active_page=get_translated_active_page(_A2);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_V;data=User.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=CustomUserChangeForm(request.POST,instance=post)
		if form.is_valid():obj=data.get();obj.name=request.POST.get(_H);obj.email=request.POST.get(_AX);obj.save();messages.info(request,mMsgBox.get(_W,request.POST.get(_H)));return redirect(reverse_lazy(_A2))
	else:messages.info(request,mMsgBox.get(_X));context[_G]=CustomUserChangeForm(instance=post)
	return render(request,template,context)
def user_delete(request,uuid):context={};site_id=get_site_id(request);data=User.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_Y,tmp));return redirect(reverse_lazy(_A2))
def get_hitcount_daily(request):
	A='created__date';lst=[];tgl=datetime.now();site_id=get_site_id(request);content_type_id=ContentType.objects.get(app_label=_Ao,model=_AO);content_type_id=content_type_id.id if content_type_id else _C;hitcount_id=HitCount.objects.filter(content_type_id=content_type_id,object_pk=site_id).first();hitcount_id=hitcount_id.id if hitcount_id else _C;start_date=add_months(tgl,-3);start_date=datetime(start_date.year,start_date.month,1,0,0,0);print(_Ap,start_date);res=calendar.monthrange(tgl.year,tgl.month);day=res[1];end_date=datetime(tgl.year,tgl.month,day,23,59,59);print(_Aq,end_date);hit=Hit.objects.filter(hitcount_id=hitcount_id,created__range=[start_date,end_date]).values(A).annotate(count=Count(_B)).order_by(A);cat=[];val=[]
	for i in hit:tmp=[];dtime=i[A];cat.append(dtime.strftime(_Ar));val.append(i[_As])
	lst.append(cat);lst.append(val);return lst
def get_hitcount_monthly(request):
	B='created__month';A='created__year';lst=[];tgl=datetime.now();site_id=get_site_id(request);content_type_id=ContentType.objects.get(app_label=_Ao,model=_AO);content_type_id=content_type_id.id if content_type_id else _C;hitcount_id=HitCount.objects.filter(content_type_id=content_type_id,object_pk=site_id).first();hitcount_id=hitcount_id.id if hitcount_id else _C;start_date=add_months(tgl,-3);start_date=datetime(start_date.year,start_date.month,1,0,0,0);print(_Ap,start_date);res=calendar.monthrange(tgl.year,tgl.month);day=res[1];end_date=datetime(tgl.year,tgl.month,day,23,59,59);print(_Aq,end_date);hit=Hit.objects.filter(hitcount_id=hitcount_id,created__range=[start_date,end_date]).values(A,B).annotate(count=Count(_B)).order_by(A,B);print(hit);cat=[];val=[]
	for i in hit:tmp=[];dtime=i[B];dtime_year=i[A];cat.append(calendar.month_abbr[dtime]+' '+str(dtime_year));val.append(i[_As])
	lst.append(cat);lst.append(val);return lst
def get_hitcount_weekly(request):
	lst=[];tgl=datetime.now();site_id=get_site_id(request);content_type_id=ContentType.objects.get(app_label=_Ao,model=_AO);content_type_id=content_type_id.id if content_type_id else _C;hitcount_id=HitCount.objects.filter(content_type_id=content_type_id,object_pk=site_id).first();hitcount_id=hitcount_id.id if hitcount_id else _C;start_date=add_months(tgl,-3);start_date=datetime(start_date.year,start_date.month,1,0,0,0);print(_Ap,start_date);res=calendar.monthrange(tgl.year,tgl.month);day=res[1];end_date=datetime(tgl.year,tgl.month,day,23,59,59);print(_Aq,end_date);hit=Hit.objects.filter(hitcount_id=hitcount_id,created__range=[start_date,end_date]);week_begin,week_end=get_week_date(tgl.year,tgl.month,tgl.day);cat=[];val=[]
	for i in range(13):
		week_begin_2=week_begin-timedelta(days=7*i);week_end_2=week_end-timedelta(days=7*i);week_end_2=datetime(week_end_2.year,week_end_2.month,week_end_2.day,23,59,59);hit_2=hit.filter(created__range=[week_begin_2,week_end_2]).values('domain').annotate(count=Count(_B))
		if hit_2:
			for j in hit_2:cat.insert(0,week_begin_2.strftime(_Ar)+' - '+week_end_2.strftime(_Ar));val.insert(0,j[_As])
	lst.append(cat);lst.append(val);return lst
def hitcount_ajax(request,period='2'):
	lst=[]
	if period=='2':lst=get_hitcount_daily(request)
	elif period=='3':lst=get_hitcount_weekly(request)
	elif period=='4':lst=get_hitcount_monthly(request)
	return JsonResponse(lst,safe=_A)