_O='template'
_N='description'
_M='last_login'
_L='groups'
_K='is_superuser'
_J='file_path'
_I='model_list'
_H='kind'
_G='is_staff'
_F='is_active'
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
admin.site.register(Agency,TranslatableAdmin)
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_D:(_E,'password')}),(_('Personal info'),{_D:(_A,)}),(_('Permissions'),{_D:(_F,_G,_K,_L,'user_permissions')}),(_('Important dates'),{_D:(_M,)});add_fieldsets=(None,{'classes':('wide',),_D:(_E,_A,'password1','password2')}),;list_display=_E,_A,_G,_M;list_filter=_G,_K,_F,_L;search_fields=_E,_A;ordering=_E,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_H,;list_display=[_H,'agency',_F,'site','expired_date',_B];search_fields=_H,;ordering=_C,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path',_B];search_fields=_A,;ordering=_C,
admin.site.register(Template,TemplateAdmin)
class TemplateOwnerAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,_B];search_fields=_A,;ordering=_C,
admin.site.register(TemplateOwner,TemplateOwnerAdmin)
class ModelListAdmin(admin.ModelAdmin):list_filter=_A,_N,'status';list_display=[_A,_N,_B];search_fields=_A,;ordering=_C,
admin.site.register(ModelList,ModelListAdmin)
class ModelListSettingAdmin(admin.ModelAdmin):list_filter=_I,_O;list_display=[_I,_O,_B];search_fields=_I,;ordering=_C,
admin.site.register(ModelListSetting,ModelListSettingAdmin)
class PhotoAdmin(admin.ModelAdmin):list_filter=_J,;list_display=[_J,_B];search_fields=_J,;ordering=_C,
admin.site.register(Photo,PhotoAdmin)