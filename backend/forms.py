_R='address'
_Q='whatsapp'
_P='is_external'
_O='is_visibled'
_N='order_menu'
_M='parent'
_L='file_path_doc'
_K='designation'
_J='location'
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
	class Meta:model=Tags;fields=[_E]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A)))
class LogoForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=300);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=48)
	class Meta:model=Logo;fields=[_E]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A)))
class AnnouncementForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=Announcement;fields=[_D,_F,_G,_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_F,css_class=_A),Column(_G,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class NewsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=270);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=233)
	class Meta:model=News;fields=[_D,_F,_G,_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_F,css_class=_A),Column(_G,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class ArticleForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=Article;fields=[_D,_F,_G,_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_F,css_class=_A),Column(_G,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class EventsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=370);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=233)
	class Meta:model=Events;fields=[_D,_J,'date','time',_F,_G,_I,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_J,css_class=_A),Column('date',css_class=_A),Column('time',css_class=_A),Column(_F,css_class=_A),Column(_G,css_class=_A),Column(_I,css_class=_A),Column(_B,css_class=_A)))
class SlideShowForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=873);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=424)
	class Meta:model=SlideShow;fields=[_D,_H,_F,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_H,css_class=_A),Column(_F,css_class=_A),Column(_B,css_class=_A)))
class DailyAlertForm(TranslatableModelForm):
	class Meta:model=DailyAlert;fields=['alert',_H,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column('alert',css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class GreetingForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=164);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=201)
	class Meta:model=Greeting;fields=[_D,_E,_K,_F,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_E,css_class=_A),Column(_K,css_class=_A),Column(_F,css_class=_A),Column(_B,css_class=_A)))
class PagesForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=Pages;fields=[_D,'menu',_F,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column('menu',css_class=_A),Column(_F,css_class=_A),Column(_B,css_class=_A)))
class SocialMediaForm(ModelForm):
	class Meta:model=SocialMedia;fields=['kind',_H,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column('kind',css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class PhotoGalleryForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=496);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=496)
	class Meta:model=PhotoGallery;fields=[_D,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column(_B,css_class=_A)))
class VideoGalleryForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=VideoGallery;fields=[_D,'embed',_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_D,css_class=_A),Column('embed',css_class=_A),Column(_B,css_class=_A)))
class RelatedLinkForm(TranslatableModelForm):
	class Meta:model=RelatedLink;fields=[_E,_H,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class DocumentForm(TranslatableModelForm):
	class Meta:model=Document;fields=[_E,_F,_L,_G,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column(_F,css_class=_A),Column(_L,css_class=_A),Column(_G,css_class=_A),Column(_B,css_class=_A)))
class MenuForm(ModelForm):
	class Meta:model=Menu;fields=[_E,_M,_H,_N,'icon',_O,_P]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column(_M,css_class=_A),Column(_H,css_class=_A),Column(_N,css_class=_A),Column('icon',css_class=_A),Column(_O,css_class=_A),Column(_P,css_class=_A)))
class AgencyForm(TranslatableModelForm):
	class Meta:model=Agency;fields=[_E,'email','phone','fax',_Q,_R,'notes']
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A),Column('email',css_class=_A),Column('phone',css_class=_A),Column('fax',css_class=_A),Column(_Q,css_class=_A),Column(_R,css_class=_A),Column('notes',css_class=_A)))
class CategoriesForm(TranslatableModelForm):
	class Meta:model=Categories;fields=[_E]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_C;self.helper.layout=Layout(Row(Column(_E,css_class=_A)))