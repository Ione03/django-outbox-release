_E='abcdefghkmnprwxy2345678'
_D='email'
_C='name'
_B=False
_A=True
import shortuuid
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt
from menu.models import MenuGroup
from parler.models import TranslatableModel,TranslatedFields
from region.models import Country,Province,Regency,SubDistrict,UrbanVillage
from shortuuid.django_fields import ShortUUIDField
from .abstract import BaseAbstractModel
from .managers import *
import os
class OptBillingType(models.IntegerChoices):TRANSACTION_BASE=1,_('Transaction Base');TIME_BASE=2,_('Time Base');ADVERTISE_BASE=3,_('Advertise Base')
class OptServiceType(models.IntegerChoices):EDUCATION=1,_('Education');TRAVEL=2,_('Travel')
class Photo(BaseAbstractModel):
	file_path=models.ImageField();content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE);object_id=models.PositiveIntegerField();content_object=GenericForeignKey()
	class Meta:verbose_name=_('photo');verbose_name_plural=_('photos')
	def __str__(self):return self.file_path.url
class Agency(BaseAbstractModel,TranslatableModel):
	name=models.CharField(_(_C),max_length=100);shortuuid=ShortUUIDField(length=4,max_length=10,alphabet=_E,null=_A,blank=_A,editable=_B);email=encrypt(models.EmailField(_(_D),null=_A,blank=_A));phone=encrypt(models.CharField(_('phone'),max_length=20,null=_A,blank=_A));fax=encrypt(models.CharField(_('fax'),max_length=20,null=_A,blank=_A));whatsapp=encrypt(models.CharField(_('whatsapp'),max_length=20,null=_A,blank=_A));country=models.ForeignKey(Country,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('country'));province=models.ForeignKey(Province,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('province'));regency=models.ForeignKey(Regency,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('regency'));sub_district=models.ForeignKey(SubDistrict,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('sub district'));urban_village=models.ForeignKey(UrbanVillage,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('urban village'));billing_type=models.SmallIntegerField(_('billing type'),choices=OptBillingType.choices,default=OptBillingType.TIME_BASE,blank=_A);conversion=models.FloatField(default=0,blank=_A,editable=_B);translations=TranslatedFields(address=encrypt(models.CharField(_('address'),max_length=255,null=_A,blank=_A)),notes=encrypt(RichTextUploadingField(_('description'),null=_A,blank=_A)))
	class Meta:verbose_name=_('agency');verbose_name_plural=_('agencies')
	def __str__(self):return self.name
class User(AbstractBaseUser,PermissionsMixin):
	email=models.EmailField(_('email address'),max_length=100,unique=_A);name=models.CharField(_(_C),max_length=100,blank=_A);is_active=models.BooleanField(_('active'),default=_A);is_staff=models.BooleanField(_('staff'),default=_A);is_superuser=models.BooleanField(_('super user'),default=_B);avatar=GenericRelation(Photo);agency=models.ManyToManyField(Agency);menu_group=models.ForeignKey(MenuGroup,on_delete=models.PROTECT,blank=_A,null=_A,verbose_name=_('menu group'));is_main_user=models.BooleanField(default=_B,blank=_A);is_first_enter=models.BooleanField(default=_A,blank=_A);is_management=models.BooleanField(default=_A,blank=_A);date_joined=models.DateTimeField(_('date joined'),auto_now_add=_A,editable=_B);last_login=models.DateTimeField(_('last login'),null=_A,blank=_A);objects=UserManager();USERNAME_FIELD=_D;EMAIL_FIELD=_D;REQUIRED_FIELDS=[]
	class Meta:verbose_name=_('user');verbose_name_plural=_('users')
	def __str__(self):return self.email
	def get_absolute_url(self):return'/users/%i/'%self.pk
class Service(BaseAbstractModel):
	site=models.OneToOneField(Site,on_delete=models.CASCADE);kind=models.SmallIntegerField(choices=OptServiceType.choices);agency=models.ForeignKey(Agency,on_delete=models.PROTECT,blank=_A,null=_A,related_name='service_agencies');is_active=models.BooleanField(default=_B,blank=_A);expired_date=models.DateTimeField()
	class Meta:verbose_name=_('service');verbose_name_plural=_('services')
	def __str__(self):return'EDUCATION'if self.kind==1 else''
class Template(BaseAbstractModel):
	site=models.ManyToManyField(Site,related_name='templates_site');name=models.CharField(_(_C),max_length=50);rel_path=models.CharField(_('relative path'),max_length=255);is_frontend=models.BooleanField(default=_A)
	class Meta:verbose_name=_('template');verbose_name_plural=_('templates')
	def __str__(self):return self.name
class UserLog(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);user=models.ForeignKey(User,on_delete=models.CASCADE,blank=_A,null=_A);user_agent=models.CharField(max_length=255,editable=_B);ip_address=models.CharField(max_length=40,editable=_B);is_expired=models.BooleanField(default=_B);social_media=models.CharField(max_length=20)
	class Meta:verbose_name=_('userlog');verbose_name_plural=_('userlogs')
	def __str__(self):return self.social_media
@receiver(signals.post_save,sender=Agency)
def _update_shortuuid(sender,instance,**kwargs):
	tmp=str(instance.id);print(tmp);lebar=len(tmp)
	if lebar>4:tmp=tmp[lebar-4:];print(tmp)
	else:
		while lebar<4:tmp='0'+tmp;lebar=len(tmp)
		print(tmp)
	tmp+=shortuuid.ShortUUID(alphabet=_E).random(length=4);sender.objects.filter(id=instance.id).update(shortuuid=tmp)
@receiver(models.signals.post_delete,sender=Photo)
def auto_delete_file_on_delete(sender,instance,**kwargs):
	if instance.file_path:
		if os.path.isfile(instance.file_path.path):os.remove(instance.file_path.path)
@receiver(models.signals.pre_save,sender=Photo)
def auto_delete_file_on_change(sender,instance,**kwargs):
	if not instance.pk:return _B
	try:old_file=sender.objects.get(pk=instance.pk).file_path
	except sender.DoesNotExist:return _B
	new_file=instance.file_path
	if not old_file==new_file:
		if os.path.isfile(old_file.path):os.remove(old_file.path)