import json,os
from allauth.socialaccount.models import SocialApp
from django.core.management.base import BaseCommand
from django.db.models import OuterRef,Subquery
from menu.models import Menu,MenuTranslation
from core.auto_insert_core_data import update_core_data
from core.models import ModelList,ModelListSetting,Template,TemplateOwner
class Command(BaseCommand):
	help='Load data from file to database';file_path='db'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):update_core_data()