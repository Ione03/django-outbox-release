from django.conf import settings
from django.utils.translation import gettext as _
from core.models import User
from django_outbox.common import get_site_id_front
def get_menu_group(user_id):
	A=User.objects.filter(id=user_id)
	if A:
		B=A[0].groups.all()
		if B:return B[0].id
	return 0
def context_outbox(request):return{'menugroup':get_menu_group(request.user.id)}
def get_main_domain(request):return{'main_domain':settings.MAIN_DOMAIN}
def site_id(request):return{'site_id':get_site_id_front(request)}