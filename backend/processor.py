from django.contrib.sites.models import Site
from django_outbox.common import get_site_id
from datetime import datetime
from django.utils.translation import gettext as _
from core.models import User
from django.http import Http404
def get_menu_group(user_id):
	A=User.objects.filter(id=user_id);print('menugroup = ',A)
	if A:print('menugroup[0].id = ',A[0].menu_group.id);return A[0].menu_group.id
def context_outbox(request):A=request;B=get_site_id(A);return{'menugroup':get_menu_group(A.user.id)}