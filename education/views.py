from core.common import get_agency_info
from django.views.generic import TemplateView
from django_outbox.common import get_site_id,get_template
from .models import *
from django.db.models import OuterRef,Subquery
class IndexView(TemplateView):
	site_id=None
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id);self.template_name=template+'index.html';return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		A='announcement';context=super(IndexView,self).get_context_data(*(args),**kwargs);agency=get_agency_info(self.site_id);context.update(agency);logo=Logo.objects.filter(site_id=self.site_id)[:1]
		if logo:
			logo=logo.get();photo=logo.photo.all()
			if photo:photo=photo.get();context['logo']=photo.file_path
		subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef('id'),content_type__model=A).values('file_path'));obj=Announcement.objects.all()[0];lang=obj.get_current_language();announcement=Announcement.objects.language(lang).filter(site_id=self.site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by('-updated_at')[:3]
		if announcement:context[A]=announcement
		return context