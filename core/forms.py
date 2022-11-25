_A='file_path'
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column,Layout,Row
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Photo
class PhotoForm(ModelForm):
	str_file_path=forms.CharField(widget=forms.HiddenInput())
	class Meta:model=Photo;fields=[_A]
	def __init__(A,*B,**C):super().__init__(*(B),**C);A.helper=FormHelper();A.helper.form_method='post';A.helper.layout=Layout(Row(Column(_A,css_class='form-group col-md-12 mb-0')))
class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):fields=UserCreationForm.Meta.fields+('email',)