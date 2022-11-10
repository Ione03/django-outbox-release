from core.common import get_agency_info
from django.views.generic import TemplateView
from django_outbox.common import get_site_id,get_template
class IndexView(TemplateView):
	site_id=None
	def get(A,request,*C,**D):B=request;A.site_id=get_site_id(B);E=get_template(A.site_id);A.template_name=E+'index.html';return super(IndexView,A).get(B,*(C),**D)
	def get_context_data(A,*C,**D):B=super(IndexView,A).get_context_data(*(C),**D);E=get_agency_info(A.site_id);B.update(E);return B