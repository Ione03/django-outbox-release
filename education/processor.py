from django.contrib.sites.models import Site
from django_outbox.common import get_site_id
from datetime import datetime
from django.utils.translation import gettext as _
def context_outbox(request):D=get_site_id(request);C=Site.objects.filter(id=D).values_list('name',flat=True);E=C[0]if C else'Outbox Website';A=datetime.today();F=_(A.strftime('%A'));B=A.strftime('%d');G=_(A.strftime('%B'));H=A.strftime('%Y');B=B+' '+G+' '+H;return{'title':E,'hari':F,'tgl':B}