_K='-updated_at'
_J='updated_at'
_I='last_login'
_H='groups'
_G='is_superuser'
_F='kind'
_E='is_staff'
_D='is_active'
_C='email'
_B='fields'
_A='name'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from .models import Agency,User,Service,Template
admin.site.register(Agency,TranslatableAdmin)
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_B:(_C,'password')}),(_('Personal info'),{_B:(_A,)}),(_('Permissions'),{_B:(_D,_E,_G,_H,'user_permissions')}),(_('Important dates'),{_B:(_I,)});add_fieldsets=(None,{'classes':('wide',),_B:(_C,_A,'password1','password2')}),;list_display=_C,_A,_E,_I;list_filter=_E,_G,_D,_H;search_fields=_C,_A;ordering=_C,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_F,;list_display=[_F,'agency',_D,'expired_date',_J];search_fields=_F,;ordering=_K,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path',_J];search_fields=_A,;ordering=_K,
admin.site.register(Template,TemplateAdmin)