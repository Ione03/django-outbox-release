_P='template'
_O='description'
_N='last_login'
_M='groups'
_L='is_superuser'
_K='file_path'
_J='model_list'
_I='kind'
_H='is_staff'
_G='is_active'
_F='agency'
_E='email'
_D='fields'
_C='-updated_at'
_B='updated_at'
_A='name'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from .models import *
from .forms import *
from django.contrib.auth import get_user_model
User=get_user_model()
admin.site.register(Agency,TranslatableAdmin)
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_D:(_E,'password')}),(_('Personal info'),{_D:(_A,_F)}),(_('Permissions'),{_D:(_G,_H,_L,_M,'user_permissions')}),(_('Important dates'),{_D:(_N,)});add_fieldsets=(None,{'classes':('wide',),_D:(_E,_A,'password1','password2',_F)}),;list_display=_E,_A,_H,_N;list_filter=_H,_L,_G,_M;search_fields=_E,_A;ordering=_E,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_I,;list_display=[_I,_F,_G,'site','expired_date',_B];search_fields=_I,;ordering=_C,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path',_B];search_fields=_A,;ordering=_C,
admin.site.register(Template,TemplateAdmin)
class TemplateOwnerAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,_B];search_fields=_A,;ordering=_C,
admin.site.register(TemplateOwner,TemplateOwnerAdmin)
class ModelListAdmin(admin.ModelAdmin):list_filter=_A,_O,'status';list_display=[_A,_O,_B];search_fields=_A,;ordering=_C,
admin.site.register(ModelList,ModelListAdmin)
class ModelListSettingAdmin(admin.ModelAdmin):list_filter=_J,_P;list_display=[_J,_P,_B];search_fields=_J,;ordering=_C,
admin.site.register(ModelListSetting,ModelListSettingAdmin)
class PhotoAdmin(admin.ModelAdmin):list_filter=_K,;list_display=[_K,_B];search_fields=_K,;ordering=_C,
admin.site.register(Photo,PhotoAdmin)