_S='youtube'
_R='plain-text'
_Q='extraPlugins'
_P='pasteFilter'
_O='toolbarCanCollapse'
_N='toolbar'
_M='bootstrap4'
_L='SECRET_KEY'
_K='DB_PASSWORD'
_J='/dashboard'
_I=False
_H='default'
_G='key'
_F='secret'
_E='client_id'
_D='APP'
_C='id'
_B='NAME'
_A=True
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
from encryption import OutboxEncryption
lib=OutboxEncryption(BASE_DIR)
lib.set_keyword_local('django-outbox-dev')
mplaint_key=[_K,_L]
key=lib.decrypt_environ(mplaint_key)
SECRET_KEY=key[_L]
DEBUG=key['DEBUG']
UNDER_CONSTRUCTION=key['UNDER_CONSTRUCTION']
ALLOWED_HOSTS=['127.0.0.1','localhost','outbox.pythonanywhere.com']
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','django.contrib.sites','django.contrib.humanize','core','education','region','menu','ckeditor','ckeditor_uploader','parler','hitcount','crispy_forms']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.locale.LocaleMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware','education.request_exposer.RequestExposerMiddleware']
ROOT_URLCONF='django_outbox.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':_A,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages','education.processor.context_outbox','backend.processor.context_outbox']}}]
WSGI_APPLICATION='django_outbox.wsgi.application'
DATABASES={_H:{'ENGINE':key['DB_ENGINE'],_B:key['DB_NAME'],'USER':key['DB_USER'],'PASSWORD':key[_K],'HOST':key['DB_HOST'],'PORT':key['DB_PORT']}}
AUTH_PASSWORD_VALIDATORS=[{_B:'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{_B:'django.contrib.auth.password_validation.MinimumLengthValidator'},{_B:'django.contrib.auth.password_validation.CommonPasswordValidator'},{_B:'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE=_C
TIME_ZONE='Asia/Makassar'
USE_I18N=_A
USE_L10N=_A
USE_TZ=_I
STATIC_URL='static/'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
STATIC_ROOT=BASE_DIR/'staticfiles'
STATICFILES_DIRS=[BASE_DIR/'static']
MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR/'media'
SITE_ID=1
LOGIN_REDIRECT_URL=_J
LOGOUT_REDIRECT_URL=_J
IMPORT_EXPORT_USE_TRANSACTIONS=_A
EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend'
AUTH_USER_MODEL='core.User'
EMAIL_USE_TLS=_A
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='auto.email.activation@gmail.com'
EMAIL_PORT=587
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=1
ACCOUNT_EMAIL_REQUIRED=_A
ACCOUNT_LOGIN_ATTEMPTS_LIMIT=5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT=86400
ACCOUNT_LOGOUT_REDIRECT_URL='/accounts/login/'
ACCOUNT_LOGIN_REDIRECT_URL=_J
ACCOUNT_AUTHENTICATION_METHOD='email'
ACCOUNT_UNIQUE_EMAIL=_A
ACCOUNT_USER_MODEL_USERNAME_FIELD=None
ACCOUNT_USERNAME_REQUIRED=_I
ACCOUNT_LOGOUT_ON_GET=_A
CRISPY_TEMPLATE_PACK=_M
CKEDITOR_UPLOAD_PATH='uploads/'
CKEDITOR_BASEPATH='/static/ckeditor/ckeditor/'
CKEDITOR_RESTRICT_BY_USER=_A
CKEDITOR_CONFIGS={_H:{'width':'100%',_N:'full',_O:_A,_P:_R,'removePlugins':('exportpdf','scayt'),_Q:','.join(['texttransform','html5audio','html5video','wordcount',_S,'embedsemantic','autolink','codesnippet','previewgoogledrive','previewdocument'])},'embed_video':{_Q:','.join([_S]),_O:_A,_P:_R,_N:'Custom','toolbar_Custom':[['Source','Iframe'],['Youtube']]}}
SOCIALACCOUNT_PROVIDERS={'github':{'SCOPE':['user','repo','read:org'],_D:{_E:'85c0e07e059b13f51fa7',_F:'864b498f57989b0c9673d4c26ece9639da235799',_G:''}},'facebook':{_D:{_E:'1599138133769755',_F:'fce558238cc11cfb1e321e24dbdb808a',_G:''}},'instagram':{_D:{_E:'1661150634264663',_F:'d230d65cf872859e0b9c57d07491ed84',_G:''}},'google':{_D:{_E:'52853440607-t3jdk23e1ku0ic77r4fgkekgr7vpd75b.apps.googleusercontent.com',_F:'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',_G:''}}}
from django.utils.translation import gettext_lazy as _
LANGUAGES=(_C,_('Indonesia')),('en',_('English'))
LOCALE_PATHS=[BASE_DIR/'locale/']
PARLER_DEFAULT_LANGUAGE_CODE=_C
PARLER_LANGUAGES={1:({'code':_C},{'code':'en'}),_H:{'fallbacks':[_C],'hide_untranslated':_I}}
CRISPY_TEMPLATE_PACK=_M
HITCOUNT_KEEP_HIT_IN_DATABASE={'days':60}
HITCOUNT_KEEP_HIT_ACTIVE={'days':1}