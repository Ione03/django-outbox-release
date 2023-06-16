_C='condition'
_B='defaults'
_A='id'
import json,os
from .models import Template,TemplateOwner,ModelList,ModelListSetting
from menu.models import MenuGroup,Menu
def create_template_owner(file_path):
	A=[]
	with open(os.path.join(file_path,'template_owner.json'),'r')as C:A=json.load(C)
	for B in A:D,E=TemplateOwner.objects.update_or_create(id=B[_C][_A],defaults=B[_B])
	print('Done Write data Template Owner to database!')
def create_template(file_path):
	A=[]
	with open(os.path.join(file_path,'template.json'),'r')as C:A=json.load(C)
	for B in A:D,E=Template.objects.update_or_create(id=B[_C][_A],defaults=B[_B])
	print('Done Write data Template to database!')
def create_menu(file_path):
	E='translation';C='name';D=[]
	with open(os.path.join(file_path,'menu.json'),'r')as F:D=json.load(F)
	for A in D:
		B,I=Menu.objects.language(_A).update_or_create(id=A[_C][_A],defaults=A[_B]);print('process menu',A[_B][C]);B.menu_group.clear()
		for G in A['m2m']['menu_group']:H=MenuGroup.objects.get(id=G);B.menu_group.add(H)
		B.save();B.set_current_language('en');B.name=A[E][C]if A[E][C]else'';B.save()
	print('Done Write data Menu to database!')
def create_model_list(file_path):
	A=[]
	with open(os.path.join(file_path,'model_list.json'),'r')as C:A=json.load(C)
	for B in A:D,E=ModelList.objects.update_or_create(id=B[_C][_A],defaults=B[_B])
	print('Done Write data Model List to database!')
def create_model_list_setting(file_path):
	A=[]
	with open(os.path.join(file_path,'model_list_setting.json'),'r')as C:A=json.load(C)
	for B in A:D,E=ModelListSetting.objects.update_or_create(id=B[_C][_A],defaults=B[_B])
	print('Done Write data Model List Setting to database!')
def create_core_data(apps,schema_monitor):A='db';create_template_owner(A);create_template(A);create_menu(A);create_model_list(A);create_model_list_setting(A);print('ALL Done...!')