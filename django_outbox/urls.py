from ckeditor_uploader import views as ckeditor_views
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include,path
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import redirect_service
urlpatterns=[path(_('secret-admin/'),admin.site.urls),path('',include('core.urls'))]
urlpatterns+=i18n_patterns(path('',redirect_service),path('ckeditor/',include('ckeditor_uploader.urls')),path('ckeditor/upload/',login_required(ckeditor_views.upload),name='ckeditor_upload'),path('ckeditor/browse/',never_cache(login_required(ckeditor_views.browse)),name='ckeditor_browse'),path(_('edu/'),include('education.urls')),path(_('dashboard/'),include('backend.urls')))
if settings.DEBUG:urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
else:urlpatterns+=staticfiles_urlpatterns()