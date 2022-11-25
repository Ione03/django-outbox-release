_A='/admin'
from core.common import get_agency_info
from django.views.generic import TemplateView
from django_outbox.common import get_site_id,get_template
from .models import *
from django.db.models import OuterRef,Subquery
from django_outbox.views import service_exists
from django.http import Http404
from django.contrib.sites.models import Site
import datetime,calendar
from menu.models import MenuGroup
from hitcount.models import HitCount,Hit
from hitcount.views import HitCountMixin
class IndexView(TemplateView):
	site_id=None
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id(request);service=service_exists(request)
		if not service:raise Http404("service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(request.get_host(),_A))
		if request.session.session_key:obj=Site.objects.get(id=self.site_id);hit_count=HitCount.objects.get_for_object(obj);hit_count_response=HitCountMixin.hit_count(request,hit_count)
		template=get_template(self.site_id);self.template_name=template+'index.html';return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		I='news';H='photogallery';G='events';F='greeting';E='slideshow';D='announcement';C='file_path';B='id';A='-updated_at';context=super(IndexView,self).get_context_data(*(args),**kwargs);menugroup=MenuGroup.objects.filter(site=self.site_id,kind=1);print('menugroup = ',menugroup)
		if menugroup:context['menugroup']=int(menugroup[0].id)
		else:raise Http404("Menu Group '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(self.request.get_host(),_A))
		agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.request);context.update(statistic);logo=Logo.objects.filter(site_id=self.site_id)[:1]
		if logo:
			logo=logo.get();photo=logo.photo.all()
			if photo:photo=photo.get();context['logo']=photo.file_path
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(B),content_type__model=D).values(C));obj=Announcement();lang=obj.get_current_language();announcement=Announcement.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(A)[:6]
		if announcement:context[D]=announcement
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(B),content_type__model=E).values(C));slideshow=SlideShow.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(A)
		if slideshow:context[E]=slideshow
		dailyalert=DailyAlert.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by(A)
		if dailyalert:context['dailyalert']=dailyalert
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(B),content_type__model=F).values(C));greeting=Greeting.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(A)
		if greeting:context[F]=greeting
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(B),content_type__model=G).values(C));events=Events.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(A)
		if events:context[G]=events
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(B),content_type__model=H).values(C));photogallery=PhotoGallery.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(A)
		if photogallery:context[H]=photogallery
		relatedlink=RelatedLink.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by(A)
		if relatedlink:context['relatedlink']=relatedlink
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(B),content_type__model=I).values(C));news=News.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(A)
		if news:context[I]=news
		document=Document.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by(A)
		if document:context['document']=document
		socialmedia=SocialMedia.objects.filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).order_by('kind')
		if socialmedia:context['socialmedia']=socialmedia
		return context
def add_months(sourcedate,months):month=sourcedate.month-1+months;year=sourcedate.year+month//12;month=month%12+1;day=min(sourcedate.day,calendar.monthrange(year,month)[1]);return datetime.date(year,month,day)
def get_statistic(request):
	B='hit_all';A='hit_online';context={};tgl=datetime.datetime.now();Domain=request.get_host();site_id=get_site_id(request);end_date=datetime.datetime(tgl.year,tgl.month,tgl.day,23,59,59);hit_today=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day)
	if hit_today:context['hit_today']=hit_today.count()
	start_date=tgl+datetime.timedelta(days=-1);context['hit_yesterday']=Hit.objects.filter(domain=Domain,created__year=start_date.year,created__month=start_date.month,created__day=start_date.day).count();start_date=tgl+datetime.timedelta(days=-7);start_date=datetime.date(start_date.year,start_date.month,start_date.day);context['hit_this_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();start_date=tgl+datetime.timedelta(days=-14);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=tgl+datetime.timedelta(days=-7);end_date=datetime.datetime(end_date.year,end_date.month,end_date.day,23,59,59);context['hit_last_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();context['hit_this_month']=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month).count();start_date=add_months(tgl,-1);context['hit_last_month']=Hit.objects.filter(domain=Domain,created__year=start_date.year,created__month=start_date.month).count();start_date=tgl+datetime.timedelta(hours=-3);start_date=datetime.datetime(start_date.year,start_date.month,start_date.day,start_date.hour,0,0);end_date=tgl;end_date=datetime.datetime(end_date.year,end_date.month,end_date.day,end_date.hour,59,59);hit_online=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date))
	if hit_online:context[A]=hit_online.count()
	else:context[A]=1
	content_type=ContentType.objects.filter(model='site').first();hit_count=HitCount.objects.filter(object_pk=site_id,content_type_id=content_type.id)
	if hit_count:context[B]=hit_count[0].hits
	else:context[B]=1
	return context