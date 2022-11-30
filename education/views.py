_V='base_url'
_U='socialmedia'
_T='document'
_S='relatedlink'
_R='priority'
_Q='menugroup'
_P='menugroup = '
_O="service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_N='news'
_M='events'
_L="Menu Group '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_K='kind'
_J='photogallery'
_I='greeting'
_H='slideshow'
_G='name'
_F='logo'
_E='announcement'
_D='/admin'
_C='-updated_at'
_B='file_path'
_A='id'
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
class IndexView(TemplateView):
	site_id=None
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id(request);service=service_exists(request)
		if not service:raise Http404(_O%(request.get_host(),_D))
		print('request.session.session_key = ',request.session.session_key)
		if request.session.session_key:obj=Site.objects.get(id=self.site_id);hit_count=HitCount.objects.get_for_object(request,obj);hit_count_response=HitCountMixin.hit_count(request,hit_count)
		template=get_template(self.site_id);self.template_name=template+'index.html';return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		A='banner';context=super(IndexView,self).get_context_data(*(args),**kwargs);menugroup=MenuGroup.objects.filter(site=self.site_id,kind=1);print(_P,menugroup)
		if menugroup:context[_Q]=int(menugroup[0].id)
		else:raise Http404(_L%(self.request.get_host(),_D))
		agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.request);context.update(statistic);subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_F).values(_B)[:1]);logo=Logo.objects.filter(site_id=self.site_id).values(_G).annotate(file_path=subquery_foto)[:1]
		if logo:context[_F]=logo
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=A).values(_B)[:1]);banner=Banner.objects.filter(site_id=self.site_id).annotate(file_path=subquery_foto)[:1]
		if banner:context[A]=banner
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_E).values(_B)[:1]);lang=get_active_language_choices()[0];announcement=Announcement.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_R,_C)[:4]
		if announcement:context[_E]=announcement
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_H).values(_B)[:1]);slideshow=SlideShow.objects.filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)
		if slideshow:context[_H]=slideshow
		dailyalert=DailyAlert.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:10]
		if dailyalert:context['dailyalert']=dailyalert
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_I).values(_B)[:1]);greeting=Greeting.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:1]
		if greeting:context[_I]=greeting
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_M).values(_B)[:1]);events=Events.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:7]
		if events:context[_M]=events
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_J).values(_B)[:1]);photogallery=PhotoGallery.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:10]
		if photogallery:context[_J]=photogallery
		relatedlink=RelatedLink.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:10]
		if relatedlink:context[_S]=relatedlink
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_N).values(_B)[:1]);news=News.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:7]
		if news:context[_N]=news
		document=Document.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:7]
		if document:context[_T]=document
		socialmedia=SocialMedia.objects.filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by(_K)
		if socialmedia:context[_U]=socialmedia
		my_path=self.request.path;my_path=my_path.split('/')
		if my_path:context[_V]=my_path[0]+'/'+my_path[1]+'/'+my_path[2]
		return context
def add_months(sourcedate,months):month=sourcedate.month-1+months;year=sourcedate.year+month//12;month=month%12+1;day=min(sourcedate.day,calendar.monthrange(year,month)[1]);return datetime.date(year,month,day)
def get_statistic(request):
	C='hit_all';B='hit_online';A='hit_today';context={};tgl=datetime.datetime.now();Domain=request.get_host();site_id=get_site_id(request);end_date=datetime.datetime(tgl.year,tgl.month,tgl.day,23,59,59);hit_today=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day)
	if hit_today:context[A]=hit_today.count()
	else:context[A]=1
	start_date=tgl+datetime.timedelta(days=-1);context['hit_yesterday']=Hit.objects.filter(domain=Domain,created__year=start_date.year,created__month=start_date.month,created__day=start_date.day).count();start_date=tgl+datetime.timedelta(days=-7);start_date=datetime.date(start_date.year,start_date.month,start_date.day);context['hit_this_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();start_date=tgl+datetime.timedelta(days=-14);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=tgl+datetime.timedelta(days=-7);end_date=datetime.datetime(end_date.year,end_date.month,end_date.day,23,59,59);context['hit_last_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();context['hit_this_month']=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month).count();start_date=add_months(tgl,-1);context['hit_last_month']=Hit.objects.filter(domain=Domain,created__year=start_date.year,created__month=start_date.month).count();start_date=tgl+datetime.timedelta(hours=-3);start_date=datetime.datetime(start_date.year,start_date.month,start_date.day,start_date.hour,0,0);end_date=tgl;end_date=datetime.datetime(end_date.year,end_date.month,end_date.day,end_date.hour,59,59);hit_online=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date))
	if hit_online:context[B]=hit_online.count()
	else:context[B]=1
	content_type=ContentType.objects.filter(model='site').first();hit_count=HitCount.objects.filter(object_pk=site_id,content_type_id=content_type.id,domain=Domain)
	if hit_count:context[C]=hit_count[0].hits
	else:context[C]=1
	return context
class DetailView(TemplateView):
	site_id=None
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id(request);service=service_exists(request)
		if not service:raise Http404(_O%(request.get_host(),_D))
		template=get_template(self.site_id);self.template_name=template+'detail.html';return super(DetailView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		E='count';D='name_slugify';C='Halaman tidak ditemukan!';B='pages';A='categories_id';context=super(DetailView,self).get_context_data(*(args),**kwargs);menugroup=MenuGroup.objects.filter(site=self.site_id,kind=1);print(_P,menugroup)
		if menugroup:context[_Q]=int(menugroup[0].id)
		else:raise Http404(_L%(self.request.get_host(),_D))
		slug=self.kwargs['slug']
		if not slug:raise Http404(_L%(self.request.get_host(),_D))
		agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.request);context.update(statistic);subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_F).values(_B)[:1]);logo=Logo.objects.filter(site_id=self.site_id).values(_G).annotate(file_path=subquery_foto)[:1]
		if logo:context[_F]=logo
		lang=get_active_language_choices()[0];kinds=[_E,_N,'article',_M,_T,_I,B,_H];kind=self.kwargs[_K]
		if kind in kinds:context[_K]=kind
		else:raise Http404(C)
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_E).values(_B)[:1]);announcement=Announcement.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).exclude(slug=slug).annotate(file_path=subquery_foto).order_by(_R,_C)[:6]
		if announcement:context[_E]=announcement
		model=apps.get_model('education',kind)
		if kind not in[B,_I,_H]:
			subquery=Subquery(Categories.objects.translated(lang).filter(id=OuterRef(A)).values('translations__name')[:1]);categories_list=[];obj=model.objects.filter(site_id=self.site_id).values(A).annotate(count=Count(A)).annotate(name=subquery).order_by(A)
			if obj:
				all=0
				for i in obj:i[D]=slugify(i[_G]);all+=i[E]
				categories_list.append(obj[0]);categories_all={A:0,E:all,_G:'All',D:'all'};categories_list.insert(0,categories_all);context['categories_list']=categories_list
			subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=kind).values(_B)[:1]);obj=model.objects.translated(lang).filter(site_id=self.site_id).annotate(file_path=subquery_foto).exclude(slug=slug).order_by('-created_at')[:3];context['latest_kind']=obj;subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=kind).values(_B)[:1]);req_no_of_random_items=5;qs=model.objects.translated(lang).filter(site_id=self.site_id)
			if qs:possible_ids=list(qs.values_list(_A,flat=True));possible_ids=random.choices(possible_ids,k=req_no_of_random_items);random_paint=qs.filter(pk__in=possible_ids).annotate(file_path=subquery_foto);context['random_paint']=random_paint;print('random_paint = ',random_paint)
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=kind).values(_B)[:1]);obj=model.objects.translated(lang).filter(site_id=self.site_id,slug=slug).annotate(file_path=subquery_foto)
		if obj:context['content_detail']=obj[0]
		else:raise Http404(C)
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_A),content_type__model=_J).values(_B)[:1]);photogallery=PhotoGallery.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)
		if photogallery:context[_J]=photogallery
		relatedlink=RelatedLink.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)
		if relatedlink:context[_S]=relatedlink
		socialmedia=SocialMedia.objects.filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by(_K)
		if socialmedia:context[_U]=socialmedia
		my_path=self.request.path;my_path=my_path.split('/')
		if my_path:context[_V]=my_path[0]+'/'+my_path[1]+'/'+my_path[2]
		return context