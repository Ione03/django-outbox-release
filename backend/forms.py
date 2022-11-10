_B='form-group col-md-12 mb-0'
_A='name'
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column,Layout,Row
from django import forms
from django.forms import ModelForm
from education.models import Logo,Tags
from parler.forms import TranslatableModelForm
class TagsForm(TranslatableModelForm):
	class Meta:model=Tags;fields=[_A]
	def __init__(A,*B,**C):super().__init__(*(B),**C);A.helper=FormHelper();A.helper.form_method='post';A.helper.layout=Layout(Row(Column(_A,css_class=_B)))
class LogoForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=400);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=64)
	class Meta:model=Logo;fields=[_A]
	def __init__(A,*B,**C):super().__init__(*(B),**C);A.helper=FormHelper();A.helper.form_method='post';A.helper.layout=Layout(Row(Column(_A,css_class=_B)))