_B='name'
_A='site'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from .models import *
class LogoAdmin(admin.ModelAdmin):list_filter=_A,_B;list_display=[_A,_B];search_fields=_A,_B;ordering='-updated_at',
admin.site.register(Logo,LogoAdmin)
admin.site.register(Announcement,TranslatableAdmin)
admin.site.register(Article,TranslatableAdmin)
admin.site.register(DailyAlert,TranslatableAdmin)
admin.site.register(Document,TranslatableAdmin)
admin.site.register(Events,TranslatableAdmin)
admin.site.register(Greeting,TranslatableAdmin)
admin.site.register(News,TranslatableAdmin)
admin.site.register(Pages,TranslatableAdmin)
admin.site.register(PhotoGallery,TranslatableAdmin)
admin.site.register(VideoGallery,TranslatableAdmin)
admin.site.register(Popup,TranslatableAdmin)
admin.site.register(RelatedLink,TranslatableAdmin)
admin.site.register(SlideShow,TranslatableAdmin)
admin.site.register(SocialMedia,TranslatableAdmin)
admin.site.register(Tags,TranslatableAdmin)
admin.site.register(Categories,TranslatableAdmin)
admin.site.register(Banner)
admin.site.register(GoogleCalendar)
admin.site.register(GoogleCalendarDetail)
admin.site.register(HeroImage,TranslatableAdmin)
admin.site.register(WhyUs,TranslatableAdmin)
admin.site.register(AboutUs,TranslatableAdmin)
admin.site.register(HowItWorks,TranslatableAdmin)