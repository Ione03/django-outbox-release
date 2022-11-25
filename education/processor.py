from django.contrib.sites.models import Site
from django_outbox.common import get_site_id
from datetime import datetime
from django.utils.translation import gettext as _
def context_outbox(request):D=get_site_id(request);B=Site.objects.filter(id=D).values_list('name',flat=True);print('site = ',B);E=B[0]if B else'Outbox Website';A=datetime.today();F=_(A.strftime('%A'));C=A.strftime('%d');G=_(A.strftime('%B'));H=A.strftime('%Y');C=C+' '+G+' '+H;return{'title':E,'hari':F,'tgl':C}