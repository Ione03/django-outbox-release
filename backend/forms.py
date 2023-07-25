_a='address'
_Z='whatsapp'
_Y='is_external'
_X='is_visibled'
_W='order_menu'
_V='file_path_doc'
_U='designation'
_T='location'
_S='email'
_R='kind'
_Q='sub_title'
_P='description'
_O='embed'
_N='site_id'
_M='priority'
_L='order_item'
_K='icon'
_J='is_header_text'
_I='link'
_H='tags'
_G='categories'
_F='name'
_E='content'
_D='title'
_C='post'
_B='status'
_A='form-group col-md-12 mb-0'
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column,Layout,Row
from django import forms
from django.forms import ModelForm
from menu.models import Menu
from parler.forms import TranslatableModelForm
from core.models import *
from education.models import *
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
class TagsForm(TranslatableModelForm):
	class Meta:model=Tags;fields=[_F,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A),Column(_B,css_class=_A)))
class WhyUsForm(TranslatableModelForm):
	class Meta:model=WhyUs;fields=[_D,_K,_P,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_P,css_class=_A),Column(_K,css_class=_A),Column(_B,css_class=_A)))
class LogoForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=300);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=48);save_as_png=forms.CharField(widget=forms.HiddenInput(),initial=1)
	class Meta:model=Logo;fields=[_F]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A)))
class AnnouncementForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Announcement;fields=[_D,_E,_G,_H,_M,_B]
	def __init__(self,*args,**kwargs):
		site_id=kwargs.pop(_N);super().__init__(*(args),**kwargs)
		if site_id:self.fields[_H].queryset=Tags.objects.filter(site_id=site_id);self.fields[_G].queryset=Categories.objects.filter(site_id=site_id)
		self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_G,css_class=_A),Column(_M,css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class FasilitiesForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Fasilities;fields=[_D,_E,_L,_J,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_J,css_class=_A),Column(_B,css_class=_A)))
class OffersForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Offers;fields=[_D,_E,_L,_J,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_J,css_class=_A),Column(_B,css_class=_A)))
class NewsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=News;fields=[_D,_E,_G,_H,_B]
	def __init__(self,*args,**kwargs):
		site_id=kwargs.pop(_N);super().__init__(*(args),**kwargs)
		if site_id:self.fields[_H].queryset=Tags.objects.filter(site_id=site_id);self.fields[_G].queryset=Categories.objects.filter(site_id=site_id)
		self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_G,css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class ArticleForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Article;fields=[_D,_E,_G,_H,_J,_B]
	def __init__(self,*args,**kwargs):
		site_id=kwargs.pop(_N);super().__init__(*(args),**kwargs)
		if site_id:self.fields[_H].queryset=Tags.objects.filter(site_id=site_id);self.fields[_G].queryset=Categories.objects.filter(site_id=site_id)
		self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_G,css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class EventsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Events;fields=[_D,_T,'date','time',_E,_G,_H,_B]
	def __init__(self,*args,**kwargs):
		site_id=kwargs.pop(_N);super().__init__(*(args),**kwargs)
		if site_id:self.fields[_H].queryset=Tags.objects.filter(site_id=site_id);self.fields[_G].queryset=Categories.objects.filter(site_id=site_id)
		self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_T,css_class=_A),Column('date',css_class=_A),Column('time',css_class=_A),Column(_E,css_class=_A),Column(_G,css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class SlideShowForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=873);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=424)
	class Meta:model=SlideShow;fields=[_D,_Q,_E,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_Q,css_class=_A),Column(_E,css_class=_A),Column(_B,css_class=_A)))
class DailyAlertForm(TranslatableModelForm):
	class Meta:model=DailyAlert;fields=['alert',_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column('alert',css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class GreetingForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=164);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=201)
	class Meta:model=Greeting;fields=[_D,_F,_U,_E,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_F,css_class=_A),Column(_U,css_class=_A),Column(_E,css_class=_A),Column(_B,css_class=_A)))
class PagesForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Pages;fields=[_D,_E,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_B,css_class=_A)))
class SocialMediaForm(ModelForm):
	class Meta:model=SocialMedia;fields=[_R,_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_R,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class HowItWorksForm(TranslatableModelForm):
	class Meta:model=HowItWorks;fields=[_D,_E,_K,_L,_J,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_K,css_class=_A),Column(_L,css_class=_A),Column(_J,css_class=_A),Column(_B,css_class=_A)))
class AboutUsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=900);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=600)
	class Meta:model=AboutUs;fields=[_D,_Q,_E,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C
class PhotoGalleryForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=1000);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=496)
	class Meta:model=PhotoGallery;fields=[_D,_E,_L,_J,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_B,css_class=_A)))
class VideoGalleryForm(TranslatableModelForm):
	class Meta:model=VideoGallery;fields=[_D,_O,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_O,css_class=_A),Column(_B,css_class=_A)))
class RelatedLinkForm(TranslatableModelForm):
	class Meta:model=RelatedLink;fields=[_F,_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class DocumentForm(TranslatableModelForm):
	class Meta:model=Document;fields=[_F,_E,_V,_G,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A),Column(_E,css_class=_A),Column(_V,css_class=_A),Column(_G,css_class=_A),Column(_B,css_class=_A)))
class MenuForm(TranslatableModelForm):
	class Meta:model=Menu;fields=[_F,_I,_W,_K,_X,_Y,'exclude_menu']
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A),Column(_I,css_class=_A),Column(_W,css_class=_A),Column(_K,css_class=_A),Column(_X,css_class=_A),Column(_Y,css_class=_A)))
class AgencyForm(TranslatableModelForm):
	class Meta:model=Agency;fields=[_F,_S,'phone','fax',_Z,_a,'notes']
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A),Column(_S,css_class=_A),Column('phone',css_class=_A),Column('fax',css_class=_A),Column(_Z,css_class=_A),Column(_a,css_class=_A),Column('notes',css_class=_A)))
class CategoriesForm(TranslatableModelForm):
	class Meta:model=Categories;fields=[_F,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A),Column(_B,css_class=_A)))
class ProductForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Product;fields=[_F,_D,_K,_E,_L,_J,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C
class TemplateOwnerForm(ModelForm):
	class Meta:model=TemplateOwner;fields=[_F]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A)))
class ModelListForm(ModelForm):
	class Meta:model=ModelList;fields=[_F,_P,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A)))
class ServiceForm(ModelForm):
	class Meta:model=Service;fields=['site',_R,'agency','is_active','expired_date']
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A)))
class TemplateForm(ModelForm):
	class Meta:model=Template;fields=[_F,'rel_path','template_owner','is_frontend']
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_F,css_class=_A)))
class BannerForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=267);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=417)
	class Meta:model=Banner;fields=[_M,_I]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_M,css_class=_A),Column(_I,css_class=_A)))
class LocationForm(TranslatableModelForm):
	class Meta:model=Location;fields=[_D,_O,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_O,css_class=_A),Column(_B,css_class=_A)))
class CustomUserCreationForm(UserCreationForm):
	is_accept_terms=forms.BooleanField(required=True)
	class Meta(UserCreationForm.Meta):model=get_user_model();fields=_S,_F,'is_accept_terms'