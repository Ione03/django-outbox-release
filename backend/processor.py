from django_outbox.common import get_site_id
from django.utils.translation import gettext as _
from core.models import User
from django.conf import settings
def get_menu_group(user_id):
	A=User.objects.filter(id=user_id)
	if A:
		if A[0].menu_group:return A[0].menu_group.id
	return 0
def context_outbox(request):A=request;B=get_site_id(A);return{'menugroup':get_menu_group(A.user.id)}
def get_main_domain(request):A=request.scheme+'://';return{'main_domain':A+settings.MAIN_DOMAIN}
def site_id(request):return{'site_id':get_site_id(request)}