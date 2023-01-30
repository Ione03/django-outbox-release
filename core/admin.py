_L='description'
_K='last_login'
_J='groups'
_I='is_superuser'
_H='kind'
_G='is_staff'
_F='is_active'
_E='-updated_at'
_D='updated_at'
_C='email'
_B='fields'
_A='name'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from .models import *
admin.site.register(Agency,TranslatableAdmin)
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_B:(_C,'password')}),(_('Personal info'),{_B:(_A,)}),(_('Permissions'),{_B:(_F,_G,_I,_J,'user_permissions')}),(_('Important dates'),{_B:(_K,)});add_fieldsets=(None,{'classes':('wide',),_B:(_C,_A,'password1','password2')}),;list_display=_C,_A,_G,_K;list_filter=_G,_I,_F,_J;search_fields=_C,_A;ordering=_C,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_H,;list_display=[_H,'agency',_F,'expired_date',_D];search_fields=_H,;ordering=_E,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path',_D];search_fields=_A,;ordering=_E,
admin.site.register(Template,TemplateAdmin)
class TemplateOwnerAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,_D];search_fields=_A,;ordering=_E,
admin.site.register(TemplateOwner,TemplateOwnerAdmin)
class ModelListAdmin(admin.ModelAdmin):list_filter=_A,_L,'status';list_display=[_A,_L,_D];search_fields=_A,;ordering=_E,
admin.site.register(ModelList,ModelListAdmin)