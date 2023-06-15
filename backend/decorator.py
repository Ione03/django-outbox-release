from django.contrib.auth.decorators import user_passes_test
def group_required(*A):
	def B(u):
		if u.is_authenticated:
			if bool(u.groups.filter(name__in=A))|u.is_superuser:return True
		return False
	return user_passes_test(B,login_url='/id/accounts/login/')