_C='defaults'
_B='condition'
_A='id'
import json,os
from allauth.socialaccount.models import SocialApp
from menu.models import Menu,MenuGroup
from .models import ModelList,ModelListSetting,Template,TemplateOwner
def create_template_owner(file_path):
	A=[]
	with open(os.path.join(file_path,'template_owner.json'),'r')as C:A=json.load(C)
	for B in A:D,E=TemplateOwner.objects.update_or_create(id=B[_B][_A],defaults=B[_C])
	print('Done Write data Template Owner to database!')
def create_template(file_path):
	A=[]
	with open(os.path.join(file_path,'template.json'),'r')as C:A=json.load(C)
	for B in A:D,E=Template.objects.update_or_create(id=B[_B][_A],defaults=B[_C])
	print('Done Write data Template to database!')
def create_menu(file_path):
	E='name';D='translation';C=[]
	with open(os.path.join(file_path,'menu.json'),'r')as F:C=json.load(F)
	for B in C:
		A,I=Menu.objects.language(_A).update_or_create(id=B[_B][_A],defaults=B[_C]);A.menu_group.clear()
		for G in B['m2m']['menu_group']:H=MenuGroup.objects.get(id=G);A.menu_group.add(H)
		A.save();A.set_current_language('en');A.name=B[D][E]if B[D][E]else'';A.save()
	print('Done Write data Menu to database!')
def create_model_list(file_path):
	A=[]
	with open(os.path.join(file_path,'model_list.json'),'r')as C:A=json.load(C)
	for B in A:D,E=ModelList.objects.update_or_create(id=B[_B][_A],defaults=B[_C])
	print('Done Write data Model List to database!')
def create_model_list_setting(file_path):
	A=[]
	with open(os.path.join(file_path,'model_list_setting.json'),'r')as C:A=json.load(C)
	ModelListSetting.objects.all().delete()
	for B in A:D,E=ModelListSetting.objects.update_or_create(id=B[_B][_A],defaults=B[_C])
	print('Done Write data Model List Setting to database!')
def create_social_app(file_path):
	A=[]
	with open(os.path.join(file_path,'social_app.json'),'r')as C:A=json.load(C)
	for B in A:D,E=SocialApp.objects.update_or_create(id=B[_B][_A],defaults=B[_C])
	print('Done Write data Social App to database!')
def create_core_data(apps,schema_monitor):A='db';create_template_owner(A);create_template(A);create_menu(A);create_model_list(A);create_model_list_setting(A);create_social_app(A);print('ALL Done...!')
def update_core_data():A='db';create_template_owner(A);create_template(A);create_menu(A);create_model_list(A);create_model_list_setting(A);create_social_app(A);print('ALL Data Updated...!')