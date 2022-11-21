from core.common import get_agency_info
from django.views.generic import TemplateView
from django_outbox.common import get_site_id,get_template
from .models import *
from django.db.models import OuterRef,Subquery
class IndexView(TemplateView):
	site_id=None
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id);self.template_name=template+'index.html';return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		I='news';H='photogallery';G='events';F='greeting';E='slideshow';D='announcement';C='file_path';B='id';A='-updated_at';context=super(IndexView,self).get_context_data(*(args),**kwargs);agency=get_agency_info(self.site_id);context.update(agency);logo=Logo.objects.filter(site_id=self.site_id)[:1]
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