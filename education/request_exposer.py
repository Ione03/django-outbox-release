from .  import models
def RequestExposerMiddleware(get_response):
	def A(request):A=request;models.exposed_request=A;B=get_response(A);return B
	return A