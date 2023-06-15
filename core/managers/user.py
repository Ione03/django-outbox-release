_B='is_superuser'
_A=None
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
class UserQuerySet(models.QuerySet):
	def get_user(A,user_id):return A.filter(id=user_id)
	def get_user_company(A,user_id,company_id):return A.filter(id=user_id).filter(company__id=company_id)
class UserManager(BaseUserManager):
	use_in_migrations=True
	def _create_user(B,email,password,**D):
		C=email
		if not C:raise ValueError('The given email must be set')
		A=B.model(email=C,**D);A.set_password(password);A.save(using=B._db);return A
	def create_user(B,email,password=_A,**A):A.setdefault(_B,False);return B._create_user(email,password,**A)
	def create_superuser(B,email,password,**A):
		A.setdefault(_B,True)
		if A.get(_B)is not True:raise ValueError('Superuser must have is_superuser=True.')
		return B._create_user(email,password,**A)
	def get_queryset(A):return UserQuerySet(A.model,using=A._db)
	def get_first_company_name(B,user_id):
		A=B.get_queryset().get_user(user_id).first()
		if A.company.name:return A.company.name
		return _A
	def is_first_enter(A,user_id):B=A.get_queryset().get_user(user_id).first();return B.is_first_enter
	def set_first_enter(B,user_id,value):A=B.get_queryset().get_user(user_id).first();A.is_first_enter=value;A.save()
	def get_user_data(B,user_id):
		A=B.get_queryset().get_user(user_id)
		if A:return A.first()
		return _A
	def get_user_data_by_company(B,user_id,company_id):
		A=B.get_queryset().get_user_company(user_id,company_id)
		if A:return A.first()
		return _A