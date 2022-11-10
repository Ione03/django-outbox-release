_K='last_login'
_J='groups'
_I='is_superuser'
_H='kind'
_G='is_staff'
_F='is_active'
_E='-updated_at'
_D='updated_at'
_C='fields'
_B='email'
_A='name'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Agency,User,Service,Template
class AgencyAdmin(admin.ModelAdmin):list_filter=_A,_B;list_display=[_A,'province','regency','sub_district','urban_village','address','phone','notes',_D];search_fields=_A,_B;ordering=_E,
admin.site.register(Agency,AgencyAdmin)
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_C:(_B,'password')}),(_('Personal info'),{_C:(_A,)}),(_('Permissions'),{_C:(_F,_G,_I,_J,'user_permissions')}),(_('Important dates'),{_C:(_K,)});add_fieldsets=(None,{'classes':('wide',),_C:(_B,_A,'password1','password2')}),;list_display=_B,_A,_G,_K;list_filter=_G,_I,_F,_J;search_fields=_B,_A;ordering=_B,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_H,;list_display=[_H,'agency',_F,'expired_date',_D];search_fields=_H,;ordering=_E,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path',_D];search_fields=_A,;ordering=_E,
admin.site.register(Template,TemplateAdmin)