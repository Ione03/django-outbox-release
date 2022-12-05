_V='base_url'
_U='socialmedia'
_T='document'
_S='relatedlink'
_R='menugroup'
_Q='/admin'
_P="service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_O='Halaman tidak ditemukan!'
_N='videogallery'
_M='banner'
_L='/dashboard'
_K='article'
_J='news'
_I='photogallery'
_H='events'
_G='name'
_F='logo'
_E='greeting'
_D='slideshow'
_C='announcement'
_B=None
_A='-updated_at'
from core.common import get_agency_info
from django.views.generic import TemplateView
from django_outbox.common import get_site_id,get_template
from .models import *
from django.db.models import OuterRef,Subquery,Count
from django_outbox.views import service_exists
from django.http import Http404
from django.contrib.sites.models import Site
from django.apps import apps
import datetime,calendar,random
from menu.models import MenuGroup
from parler.utils import get_active_language_choices
from django.utils.text import slugify
from hitcount.models import HitCount,Hit
from hitcount.views import HitCountMixin
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
def get_menu_group(site_id):
	menugroup=MenuGroup.objects.filter(site_id=site_id,kind=1)
	if menugroup:return menugroup[0].id
	else:raise Http404("Menu Group belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_L)
def get_photo(model_name):return Subquery(Photo.objects.filter(object_id=OuterRef('id'),content_type__model=model_name).values('file_path')[:1])
def get_logo(site_id):
	subquery_foto=get_photo(_F);logo=Logo.objects.filter(site_id=site_id).values(_G).annotate(file_path=subquery_foto)[:1]
	if logo:return logo
def get_base_url(request):
	A='/';my_path=request.path.split(A)
	if my_path:
		if len(my_path)>2:return my_path[0]+A+my_path[1]+A+my_path[2]
def add_months(sourcedate,months):month=sourcedate.month-1+months;year=sourcedate.year+month//12;month=month%12+1;day=min(sourcedate.day,calendar.monthrange(year,month)[1]);return datetime.date(year,month,day)
def get_statistic(site_id,is_cache=False):
	C='user_agent';B=')';A='load from DB (';context={};tgl=datetime.datetime.now();content_type_id=ContentType.objects.get(app_label='sites',model='site');content_type_id=content_type_id.id if content_type_id else _B;hitcount_id=HitCount.objects.filter(content_type_id=content_type_id,object_pk=site_id).first();hitcount_id=hitcount_id.id if hitcount_id else _B;jam00=datetime.datetime(tgl.year,tgl.month,tgl.day+1,0,1,0);timeout=(jam00-tgl).seconds;selisih=0;tmp='hit_today';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _B):print(A+tmp+B);hit_today=Hit.objects.filter(hitcount_id=hitcount_id,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day);tmp_cache=hit_today.count()if hit_today else 1;cache.set(tmp,tmp_cache,timeout,version=site_id);context[tmp]=tmp_cache
	else:hit_today=Hit.objects.filter(hitcount_id=hitcount_id,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day);context[tmp]=hit_today.count()if hit_today else 1;selisih=context[tmp]-tmp_cache;print('selisih = ',selisih)
	tmp='hit_yesterday';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _B):print(A+tmp+B);start_date=tgl+datetime.timedelta(days=-1);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__year=start_date.year,created__month=start_date.month,created__day=start_date.day).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	context[tmp]=tmp_cache;tmp='hit_this_week';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _B):print(A+tmp+B);start_date=tgl+datetime.timedelta(days=-7);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=datetime.datetime(tgl.year,tgl.month,tgl.day,23,59,59);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__range=(start_date,end_date)).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	tmp_cache+=selisih;context[tmp]=tmp_cache;tmp='hit_last_week';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _B):print(A+tmp+B);start_date=tgl+datetime.timedelta(days=-14);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=tgl+datetime.timedelta(days=-7);end_date=datetime.datetime(end_date.year,end_date.month,end_date.day,23,59,59);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__range=(start_date,end_date)).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	context[tmp]=tmp_cache;tmp='hit_this_month';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _B):print(A+tmp+B);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__year=tgl.year,created__month=tgl.month).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	tmp_cache+=selisih;context[tmp]=tmp_cache;tmp='hit_last_month';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _B):print(A+tmp+B);start_date=add_months(tgl,-1);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__year=start_date.year,created__month=start_date.month).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	context[tmp]=tmp_cache;start_date=tgl+datetime.timedelta(hours=-5);start_date=datetime.datetime(start_date.year,start_date.month,start_date.day,start_date.hour,0,0);end_date=datetime.datetime(tgl.year,tgl.month,tgl.day,tgl.hour,59,59);hit_online=Hit.objects.filter(hitcount_id=hitcount_id,created__range=(start_date,end_date)).values(C).order_by(C).distinct();context['hit_online']=hit_online.count()if hit_online else 1;hit_count=HitCount.objects.filter(object_pk=site_id,content_type_id=content_type_id);context['hit_all']=hit_count[0].hits if hit_count else 1;return context
def get_banner(site_id):subquery_foto=get_photo(_M);return Banner.objects.filter(site_id=site_id).annotate(file_path=subquery_foto)[:5]
def get_announcement(site_id,lang,max_data):subquery_foto=get_photo(_C);return Announcement.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by('priority',_A)[:max_data]
def get_slideshow(site_id,lang):subquery_foto=get_photo(_D);return SlideShow.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_A)[:10]
def get_dailyalert(site_id,lang):return DailyAlert.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_A)[:10]
def get_greeting(site_id,lang):subquery_foto=get_photo(_E);return Greeting.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_A)[:1]
def get_events(site_id,lang):subquery_foto=get_photo(_H);return Events.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_A)[:7]
def get_photogallery(site_id,lang):subquery_foto=get_photo(_I);return PhotoGallery.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_A)[:10]
def get_videogallery(site_id,lang):subquery_foto=get_photo(_N);return VideoGallery.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_A)[:6]
def get_relatedlink(site_id,lang):return RelatedLink.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_A)[:10]
def get_news(site_id,lang):subquery_foto=get_photo(_J);return News.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_A)[:7]
def get_article(site_id,lang):subquery_foto=get_photo(_K);return Article.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_A)[:6]
def get_document(site_id,lang):return Document.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_A)[:7]
def get_socialmedia(site_id):return SocialMedia.objects.filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_A)[:6]
def get_categories_list(site_id,lang,max_data,model):
	C='count';B='name_slugify';A='categories_id';subquery=Subquery(Categories.objects.translated(lang).filter(id=OuterRef(A)).values('translations__name')[:1]);categories_list=[];obj=model.objects.filter(site_id=site_id).values(A).annotate(count=Count(A)).annotate(name=subquery).order_by(A)[:max_data]
	if obj:
		all=0
		for i in obj:i[B]=slugify(i[_G]);all+=i[C]
		categories_list.append(obj[0]);categories_all={A:0,C:all,_G:'All',B:'all'};categories_list.insert(0,categories_all);return categories_list
def get_latest_model(site_id,lang,max_data,model,kind,slug):subquery_foto=get_photo(kind);return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).exclude(slug=slug).order_by(_A)[:max_data]
def get_related_model(site_id,lang,max_data,model,kind,slug):
	subquery_foto=get_photo(kind);req_no_of_random_items=max_data;qs=model.objects.translated(lang).filter(site_id=site_id).exclude(slug=slug)
	if qs:possible_ids=list(qs.values_list('id',flat=True));possible_ids=random.choices(possible_ids,k=req_no_of_random_items);random_paint=qs.filter(pk__in=possible_ids).annotate(file_path=subquery_foto);return random_paint
def get_content_detail(site_id,lang,model,kind,slug):
	subquery_foto=get_photo(kind);obj=model.objects.translated(lang).filter(site_id=site_id,slug=slug).annotate(file_path=subquery_foto)
	if obj:return obj.get()
	else:raise Http404(_O)
def get_location(site_id,lang):return Location.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED)[:1]
class IndexView(TemplateView):
	site_id=_B
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id(request);service=service_exists(request)
		if not service:raise Http404(_P%(request.get_host(),_Q))
		print('request.session.session_key = ',request.session.session_key)
		if request.session.session_key:obj=Site.objects.get(id=self.site_id);hit_count=HitCount.objects.get_for_object(request,obj);hit_count_response=HitCountMixin.hit_count(request,hit_count)
		template=get_template(self.site_id);self.template_name=template+'index.html';return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(IndexView,self).get_context_data(*(args),**kwargs);context[_R]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.site_id,True);context.update(statistic);context[_F]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_M]=get_banner(self.site_id);context[_C]=get_announcement(self.site_id,lang,4);context[_D]=get_slideshow(self.site_id,lang);context['dailyalert']=get_dailyalert(self.site_id,lang);context[_E]=get_greeting(self.site_id,lang);context[_H]=get_events(self.site_id,lang);context[_I]=get_photogallery(self.site_id,lang);context[_N]=get_videogallery(self.site_id,lang);context[_S]=get_relatedlink(self.site_id,lang);context[_J]=get_news(self.site_id,lang);context[_K]=get_article(self.site_id,lang);context[_T]=get_document(self.site_id,lang);context[_U]=get_socialmedia(self.site_id);context['location']=get_location(self.site_id,lang);context[_V]=get_base_url(self.request);return context
class DetailView(TemplateView):
	site_id=_B
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id(request);service=service_exists(request)
		if not service:raise Http404(_P%(request.get_host(),_Q))
		template=get_template(self.site_id);self.template_name=template+'detail.html';return super(DetailView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		B='kind';A='pages';context=super(DetailView,self).get_context_data(*(args),**kwargs);context[_R]=get_menu_group(self.site_id);slug=self.kwargs['slug']
		if not slug:raise Http404("Menu Group '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(self.request.get_host(),_L))
		agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.site_id,True);context.update(statistic);context[_F]=get_logo(self.site_id);lang=get_active_language_choices()[0];kinds=[_C,_J,_K,_H,_T,_E,A,_D];kind=self.kwargs[B]
		if kind in kinds:context[B]=kind
		else:raise Http404(_O)
		context[_C]=get_announcement(self.site_id,lang,6);model=apps.get_model('education',kind)
		if kind not in[A,_E,_D]:context['categories_list']=get_categories_list(self.site_id,lang,10,model);context['latest_kind']=get_latest_model(self.site_id,lang,3,model,kind,slug);context['random_paint']=get_related_model(self.site_id,lang,5,model,kind,slug)
		print('detail model = ',model,kind);content_detail=get_content_detail(self.site_id,lang,model,kind,slug);context['content_detail']=content_detail;hit_count=HitCount.objects.get_for_object(self.request,content_detail);hit_count_response=HitCountMixin.hit_count(self.request,hit_count);context[_I]=get_photogallery(self.site_id,lang);context[_S]=get_relatedlink(self.site_id,lang);context[_U]=get_socialmedia(self.site_id);context[_V]=get_base_url(self.request);return context