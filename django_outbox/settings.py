_b='MAIN_DOMAIN'
_a='youtube'
_Z='plain-text'
_Y='extraPlugins'
_X='pasteFilter'
_W='toolbarCanCollapse'
_V='toolbar'
_U='bootstrap4'
_T='/post-login/'
_S='MEDIA_ROOT'
_R='STATIC_ROOT'
_Q='DB_NAME'
_P='DB_ENGINE'
_O='ENGINE'
_N='templates'
_M='allauth'
_L='ALLOWED_HOSTS'
_K='SECRET_KEY'
_J='DB_PASSWORD'
_I='key'
_H='secret'
_G='client_id'
_F='APP'
_E='default'
_D='id'
_C='NAME'
_B=False
_A=True
from pathlib import Path
import os
BASE_DIR=Path(__file__).resolve().parent.parent
from encryption import OutboxEncryption
lib=OutboxEncryption(BASE_DIR)
lib.set_keyword_local('django-outbox-dev')
lib.set_keyword_local('outbox')
lib.set_keyword_local('env_outbox')
lib.set_keyword_local('django_outbox_release_v2:3.8')
mplaint_key=[_J,_K]
mplaint_list=[_L]
key=lib.decrypt_environ(mplaint_key,mplaint_list)
if not key:raise Exception('No data found in environment, activate environment first!')
SECRET_KEY=key[_K]
DEBUG=key['DEBUG']
UNDER_CONSTRUCTION=key['UNDER_CONSTRUCTION']
ALLOWED_HOSTS=key[_L]
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','django.contrib.sites','django.contrib.humanize','core','education','region','menu','ckeditor','ckeditor_uploader','parler','hitcount','crispy_forms','corsheaders',_M,'allauth.account','allauth.socialaccount','allauth.socialaccount.providers.google','allauth.socialaccount.providers.facebook','allauth.socialaccount.providers.github']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.locale.LocaleMiddleware','corsheaders.middleware.CorsMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware','education.request_exposer.RequestExposerMiddleware','hitcount.request_exposer.RequestExposerMiddleware']
ROOT_URLCONF='django_outbox.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[os.path.join(BASE_DIR,_N),os.path.join(BASE_DIR,_N,_M)],'APP_DIRS':_A,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages','education.processor.context_outbox','backend.processor.context_outbox','backend.processor.get_main_domain','backend.processor.site_id']}}]
WSGI_APPLICATION='django_outbox.wsgi.application'
DB_TYPE=key['DB_TYPE']
found=_B
if DB_TYPE:
	if DB_TYPE=='sqlite':found=_A;DATABASES={_E:{_O:key[_P],_C:key[_Q]}}
if not found:DATABASES={_E:{_O:key[_P],_C:key[_Q],'USER':key['DB_USER'],'PASSWORD':key[_J],'HOST':key['DB_HOST'],'PORT':key['DB_PORT']}}
AUTH_PASSWORD_VALIDATORS=[{_C:'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{_C:'django.contrib.auth.password_validation.MinimumLengthValidator'},{_C:'django.contrib.auth.password_validation.CommonPasswordValidator'},{_C:'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE=_D
TIME_ZONE='Asia/Makassar'
USE_I18N=_A
USE_L10N=_A
USE_TZ=_B
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
STATIC_URL='/static/'
tmp=key.get(_R)
STATIC_ROOT=key[_R]if tmp else os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
MEDIA_URL='/media/'
tmp=key.get(_S)
MEDIA_ROOT=key[_S]if tmp else os.path.join(BASE_DIR,'media')
SITE_ID=1
LOGIN_REDIRECT_URL=_T
LOGOUT_REDIRECT_URL=_T
IMPORT_EXPORT_USE_TRANSACTIONS=_A
EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend'
AUTH_USER_MODEL='core.User'
EMAIL_USE_TLS=_A
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='auto.email.activation@gmail.com'
EMAIL_PORT=587
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS=_B
ACCOUNT_LOGIN_ON_PASSWORD_RESET=_A
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE=_A
ACCOUNT_USERNAME_MIN_LENGTH=4
ACCOUNT_SESSION_REMEMBER=_A
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=1
ACCOUNT_EMAIL_REQUIRED=_A
ACCOUNT_LOGIN_ATTEMPTS_LIMIT=5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT=86400
ACCOUNT_LOGOUT_REDIRECT_URL='/id/accounts/login/'
ACCOUNT_AUTHENTICATION_METHOD='email'
ACCOUNT_UNIQUE_EMAIL=_A
ACCOUNT_USER_MODEL_USERNAME_FIELD=None
ACCOUNT_USERNAME_REQUIRED=_B
ACCOUNT_LOGOUT_ON_GET=_A
SOCIALACCOUNT_LOGIN_ON_GET=_B
ACCOUNT_FORMS={'login':'core.forms.UserLoginForm','reset_password':'core.forms.UserResetPasswordForm','signup':'core.forms.UserSignupForm'}
CRISPY_TEMPLATE_PACK=_U
CKEDITOR_UPLOAD_PATH='uploads/'
CKEDITOR_BASEPATH='/static/ckeditor/ckeditor/'
CKEDITOR_RESTRICT_BY_USER=_A
CKEDITOR_CONFIGS={_E:{'width':'100%',_V:'full',_W:_A,_X:_Z,'removePlugins':('exportpdf','scayt'),_Y:','.join(['texttransform','html5audio','html5video','wordcount',_a,'embedsemantic','autolink','codesnippet','previewgoogledrive','previewdocument'])},'embed_video':{_Y:','.join([_a]),_W:_A,_X:_Z,_V:'Custom','toolbar_Custom':[['Source','Iframe'],['Youtube']]}}
SOCIALACCOUNT_PROVIDERS={'github':{_F:{_G:'297aaf765b5b4ecdb287',_H:'f3fc63d61e37371c81d0a10463c810aa16736847',_I:''}},'facebook':{_F:{_G:'1582129178867576',_H:'6edc1f622ef5ba62ec8d8e54d8228ef8',_I:''}},'google':{_F:{_G:'921195599940-a4ft11sk9m64oop9vr1amjkvu8g192af.apps.googleusercontent.com',_H:'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',_I:''},'AUTH_PARAMS':{'access_type':'online'}}}
from django.utils.translation import gettext_lazy as _
LANGUAGES=(_D,_('Indonesia')),('en',_('English'))
LOCALE_PATHS=[os.path.join(BASE_DIR,'locale')]
PARLER_DEFAULT_LANGUAGE_CODE=_D
PARLER_LANGUAGES={1:({'code':_D},{'code':'en'}),_E:{'fallbacks':[_D],'hide_untranslated':_B}}
CRISPY_TEMPLATE_PACK=_U
HITCOUNT_KEEP_HIT_IN_DATABASE={'months':3}
HITCOUNT_KEEP_HIT_ACTIVE={'hours':1}
AUTHENTICATION_BACKENDS=['allauth.account.auth_backends.AuthenticationBackend']
tmp=key.get(_b)
MAIN_DOMAIN=key[_b]if tmp else'127.0.0.1:8000'