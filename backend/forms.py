_S='address'
_R='whatsapp'
_Q='is_external'
_P='is_visibled'
_O='order_menu'
_N='file_path_doc'
_M='designation'
_L='location'
_K='embed'
_J='priority'
_I='tags'
_H='link'
_G='categories'
_F='content'
_E='name'
_D='title'
_C='post'
_B='status'
_A='form-group col-md-12 mb-0'
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column,Layout,Row
from django import forms
from django.forms import ModelForm
from education.models import *
from parler.forms import TranslatableModelForm
from menu.models import Menu
from core.models import Agency
class TagsForm(TranslatableModelForm):
	class Meta:model=Tags;fields=[_E,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column(_B,css_class=_A)))
class LogoForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=300);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=48);save_as_png=forms.CharField(widget=forms.TextInput(),initial=1)
	class Meta:model=Logo;fields=[_E]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A)))
class AnnouncementForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Announcement;fields=[_D,_F,_G,_I,_J,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_F,css_class=_A),Column(_G,css_class=_A),Column(_J,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class NewsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=News;fields=[_D,_F,_G,_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_F,css_class=_A),Column(_G,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class ArticleForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Article;fields=[_D,_F,_G,_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_F,css_class=_A),Column(_G,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class EventsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Events;fields=[_D,_L,'date','time',_F,_G,_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_L,css_class=_A),Column('date',css_class=_A),Column('time',css_class=_A),Column(_F,css_class=_A),Column(_G,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class SlideShowForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=873);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=424)
	class Meta:model=SlideShow;fields=[_D,_F,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_F,css_class=_A),Column(_B,css_class=_A)))
class DailyAlertForm(TranslatableModelForm):
	class Meta:model=DailyAlert;fields=['alert',_H,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column('alert',css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class GreetingForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=164);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=201)
	class Meta:model=Greeting;fields=[_D,_E,_M,_F,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_M,css_class=_A),Column(_F,css_class=_A),Column(_B,css_class=_A)))
class PagesForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Pages;fields=[_D,_F,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_F,css_class=_A),Column(_B,css_class=_A)))
class SocialMediaForm(ModelForm):
	class Meta:model=SocialMedia;fields=['kind',_H,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column('kind',css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class PhotoGalleryForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=1000);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=496)
	class Meta:model=PhotoGallery;fields=[_D,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_B,css_class=_A)))
class VideoGalleryForm(TranslatableModelForm):
	class Meta:model=VideoGallery;fields=[_D,_K,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_K,css_class=_A),Column(_B,css_class=_A)))
class RelatedLinkForm(TranslatableModelForm):
	class Meta:model=RelatedLink;fields=[_E,_H,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class DocumentForm(TranslatableModelForm):
	class Meta:model=Document;fields=[_E,_F,_N,_G,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column(_F,css_class=_A),Column(_N,css_class=_A),Column(_G,css_class=_A),Column(_B,css_class=_A)))
class MenuForm(TranslatableModelForm):
	class Meta:model=Menu;fields=[_E,_H,_O,'icon',_P,_Q]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column(_H,css_class=_A),Column(_O,css_class=_A),Column('icon',css_class=_A),Column(_P,css_class=_A),Column(_Q,css_class=_A)))
class AgencyForm(TranslatableModelForm):
	class Meta:model=Agency;fields=[_E,'email','phone','fax',_R,_S,'notes']
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column('email',css_class=_A),Column('phone',css_class=_A),Column('fax',css_class=_A),Column(_R,css_class=_A),Column(_S,css_class=_A),Column('notes',css_class=_A)))
class CategoriesForm(TranslatableModelForm):
	class Meta:model=Categories;fields=[_E,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column(_B,css_class=_A)))
class BannerForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=267);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=417)
	class Meta:model=Banner;fields=[_J,_H]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_J,css_class=_A),Column(_H,css_class=_A)))
class LocationForm(TranslatableModelForm):
	class Meta:model=Location;fields=[_D,_K,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_K,css_class=_A),Column(_B,css_class=_A)))