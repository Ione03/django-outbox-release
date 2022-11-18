_J='education'
_I='photo'
_H='link'
_G='content'
_F='site'
_E='-'
_D=False
_C='--'
_B='title'
_A=True
import random
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import Photo
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt
from django_outbox.common import get_site_id
from menu.models import Menu
from parler.models import TranslatableModel,TranslatedFields
from .abstract import BaseAbstractModel
User=get_user_model()
exposed_request=None
class Logo(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);name=models.CharField(_('logo name'),max_length=100);photo=GenericRelation(Photo)
	class Meta:verbose_name=_('logo');verbose_name_plural=_('logos')
	def __str__(A):return A.name
	def save(A,*B,**C):A.slug=slugify(A.name)+_C+str(A.site_id);A.site_id=get_site_id(exposed_request);super(Logo,A).save(*(B),**C)
class OptStatusPublish(models.IntegerChoices):DRAFT=1;PUBLISHED=2
class OptSocialMediaKinds(models.IntegerChoices):FACEBOOK=1;TWITTER=2;PINTEREST=3;YOUTUBE=4;INSTAGRAM=5
class Tags(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);translations=TranslatedFields(name=models.CharField(_('tags name'),max_length=50));slug=models.SlugField(max_length=50,default='',unique=_A,blank=_A,editable=_D)
	class Meta:verbose_name=_('tag');verbose_name_plural=_('tags')
	def __str__(A):return A.name
	def save(A,*B,**C):A.slug=A.get_current_language()+_E+slugify(A.name)+_C+str(A.site_id);A.site_id=get_site_id(exposed_request);super(Tags,A).save(*(B),**C)
class BaseContentModel(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);view_count=models.PositiveIntegerField(_('view count'),default=0,editable=_D);share_count=models.PositiveIntegerField(_('share count'),default=0,editable=_D);slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A,editable=_D);photo=GenericRelation(Photo,verbose_name=_(_I));tags=models.ManyToManyField(Tags,verbose_name=_('tags'));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:app_label=_J;abstract=_A
class Announcement(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_B),max_length=500)),content=encrypt(RichTextUploadingField(_(_G),blank=_A,null=_A)))
	class Meta:verbose_name=_('announcement');verbose_name_plural=_('announcements')
	def __str__(A):return A.title
	def save(A,*B,**C):A.slug=A.get_current_language()+_E+slugify(A.title)+_C+str(A.id);A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(Announcement,A).save(*(B),**C)
class News(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_B),max_length=500)),content=encrypt(RichTextUploadingField(_(_G),blank=_A,null=_A)))
	class Meta:verbose_name=_('news');verbose_name_plural=_('news')
	def __str__(A):return A.title
	def save(A,*B,**C):A.slug=A.get_current_language()+_E+slugify(A.title)+_C+str(A.id);A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(News,A).save(*(B),**C)
class Article(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_B),max_length=500)),content=encrypt(RichTextUploadingField(_(_G),blank=_A,null=_A)))
	class Meta:verbose_name=_('article');verbose_name_plural=_('articles')
	def __str__(A):return A.title
	def save(A,*B,**C):A.slug=A.get_current_language()+_E+slugify(A.title)+_C+str(A.id);A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(Article,A).save(*(B),**C)
class Events(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_B),max_length=500)),content=encrypt(RichTextUploadingField(_(_G),blank=_A,null=_A)),location=encrypt(models.CharField(_('location'),max_length=255,null=_A,blank=_A)));date=models.DateField(_('date'));time=models.TimeField(_('time'))
	class Meta:verbose_name=_('event');verbose_name_plural=_('events')
	def __str__(A):return A.title
	def save(A,*B,**C):A.slug=A.get_current_language()+_E+slugify(A.title)+_C+str(A.id);A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(Events,A).save(*(B),**C)
class SlideShow(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=GenericRelation(Photo);translations=TranslatedFields(title=models.CharField(_(_B),max_length=500),content=encrypt(RichTextUploadingField(_(_G),blank=_A,null=_A)));link=models.CharField(_(_H),max_length=255,null=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('slide show');verbose_name_plural=_('slides show')
	def __str__(A):return A.title
	def save(A,*B,**C):A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(SlideShow,A).save(*(B),**C)
class DailyAlert(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);translations=TranslatedFields(alert=encrypt(models.CharField(_('alert'),max_length=500)));link=models.CharField(_(_H),max_length=255,null=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('daily alert');verbose_name_plural=_('daily alerts')
	def __str__(A):return A.alert
	def save(A,*B,**C):A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(DailyAlert,A).save(*(B),**C)
class Greeting(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=GenericRelation(Photo,verbose_name=_(_I));translations=TranslatedFields(title=models.CharField(_(_B),max_length=500),content=encrypt(RichTextUploadingField(_(_G),blank=_A,null=_A)));view_count=models.PositiveIntegerField(default=0,editable=_D);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('greeting');verbose_name_plural=_('greetings')
	def __str__(A):return A.title
	def save(A,*B,**C):A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(Greeting,A).save(*(B),**C)
class Pages(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_B),max_length=500)),content=encrypt(RichTextUploadingField(_(_G),blank=_A,null=_A)));menu=models.ForeignKey(Menu,on_delete=models.PROTECT,verbose_name='Access From Menu')
	class Meta:verbose_name=_('page');verbose_name_plural=_('pages')
	def __str__(A):return A.title
	def save(A,*B,**C):A.slug=A.get_current_language()+_E+slugify(A.title)+_C+str(A.id);A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(Pages,A).save(*(B),**C)
class SocialMedia(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));kind=models.SmallIntegerField(choices=OptSocialMediaKinds.choices,verbose_name=_('kind'));link=encrypt(models.URLField(_(_H),max_length=255));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return '{} - {}'.format(A.site.name,A.kind)
	def save(A,*B,**C):A.site_id=get_site_id(exposed_request);super(SocialMedia,A).save(*(B),**C)
class BaseGalleryModel(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);view_count=models.PositiveIntegerField(default=0,editable=_D);slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:app_label=_J;abstract=_A
class PhotoGallery(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_B),max_length=500)));photo=GenericRelation(Photo,verbose_name=_(_I))
	def __str__(A):return A.title
	def save(A,*B,**C):A.slug=A.get_current_language()+_E+slugify(A.title)+_C+str(A.id);A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(PhotoGallery,A).save(*(B),**C)
class VideoGallery(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_B),max_length=500)));embed=RichTextUploadingField(_('embed'),blank=_A,null=_A)
	def __str__(A):return A.title
	def save(A,*B,**C):A.slug=A.get_current_language()+_E+slugify(A.title)+_C+str(A.id);A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(VideoGallery,A).save(*(B),**C)
class RelatedLink(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,blank=_A,verbose_name=_(_F));link=encrypt(models.URLField(_(_H),max_length=255));translations=TranslatedFields(name=encrypt(models.CharField(_('name'),max_length=150)));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return A.name
	def save(A,*B,**C):A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(RelatedLink,A).save(*(B),**C)
class Document(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);file_path=models.FileField(verbose_name=_('file path'));translations=TranslatedFields(name=encrypt(models.CharField(_('name'),max_length=150)),content=encrypt(RichTextUploadingField(_(_G),blank=_A,null=_A)));size=models.BigIntegerField(_('size'),null=_A,blank=_A,default=0,editable=_D);hits=models.IntegerField(_('hits'),default=0,editable=_D);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return A.name
	def save(A,*B,**C):A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(Document,A).save(*(B),**C)
class Popup(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_F));admin=models.ForeignKey(User,on_delete=models.PROTECT);translations=TranslatedFields(title=encrypt(models.CharField(_(_B),max_length=500)));link=encrypt(models.URLField(_(_H),max_length=255,null=_A,blank=_A));photo=GenericRelation(Photo,verbose_name=_(_I));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return A.title
	def save(A,*B,**C):A.site_id=get_site_id(exposed_request);A.admin_id=exposed_request.user.id;super(Popup,A).save(*(B),**C)