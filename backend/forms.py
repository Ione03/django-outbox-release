_J='file_path'
_I='location'
_H='link'
_G='tags'
_F='name'
_E='post'
_D='content'
_C='title'
_B='status'
_A='form-group col-md-12 mb-0'
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column,Layout,Row
from django import forms
from django.forms import ModelForm
from education.models import *
from parler.forms import TranslatableModelForm
class TagsForm(TranslatableModelForm):
	class Meta:model=Tags;fields=[_F]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_F,css_class=_A)))
class LogoForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=400);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=64)
	class Meta:model=Logo;fields=[_F]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_F,css_class=_A)))
class AnnouncementForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=Announcement;fields=[_C,_D,_G,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_C,css_class=_A),Column(_D,css_class=_A),Column(_G,css_class=_A),Column(_B,css_class=_A)))
class NewsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=News;fields=[_C,_D,_G,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_C,css_class=_A),Column(_D,css_class=_A),Column(_G,css_class=_A),Column(_B,css_class=_A)))
class ArticleForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=Article;fields=[_C,_D,_G,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_C,css_class=_A),Column(_D,css_class=_A),Column(_G,css_class=_A),Column(_B,css_class=_A)))
class EventsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=Events;fields=[_C,_I,'date','time',_D,_G,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_C,css_class=_A),Column(_I,css_class=_A),Column('date',css_class=_A),Column('time',css_class=_A),Column(_D,css_class=_A),Column(_G,css_class=_A),Column(_B,css_class=_A)))
class SlideShowForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=SlideShow;fields=[_C,_H,_D,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_C,css_class=_A),Column(_H,css_class=_A),Column(_D,css_class=_A),Column(_B,css_class=_A)))
class DailyAlertForm(TranslatableModelForm):
	class Meta:model=DailyAlert;fields=['alert',_H,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column('alert',css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class GreetingForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=Greeting;fields=[_C,_D,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_C,css_class=_A),Column(_D,css_class=_A),Column(_B,css_class=_A)))
class PagesForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=Pages;fields=[_C,'menu',_D,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_C,css_class=_A),Column('menu',css_class=_A),Column(_D,css_class=_A),Column(_B,css_class=_A)))
class SocialMediaForm(ModelForm):
	class Meta:model=SocialMedia;fields=['kind',_H,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column('kind',css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class PhotoGalleryForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=PhotoGallery;fields=[_C,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_C,css_class=_A),Column(_B,css_class=_A)))
class VideoGalleryForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=68);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=68)
	class Meta:model=VideoGallery;fields=[_C,'embed',_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_C,css_class=_A),Column('embed',css_class=_A),Column(_B,css_class=_A)))
class RelatedLinkForm(TranslatableModelForm):
	class Meta:model=RelatedLink;fields=[_F,_H,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_F,css_class=_A),Column(_H,css_class=_A),Column(_B,css_class=_A)))
class DocumentForm(TranslatableModelForm):
	class Meta:model=Document;fields=[_F,_D,_J,_B]
	def __init__(self,*args,**kwargs):super().__init__(*(args),**kwargs);self.helper=FormHelper();self.helper.form_method=_E;self.helper.layout=Layout(Row(Column(_F,css_class=_A),Column(_D,css_class=_A),Column(_J,css_class=_A),Column(_B,css_class=_A)))