_A='upload_photo'
from django.urls import include,path
from .views import upload_photo
urlpatterns=[path('dashboard/upload-photo/<int:width>/<int:height>/',upload_photo,name=_A),path('dashboard/upload-photo/<int:width>/<int:height>/<int:save_as_png>/',upload_photo,name=_A)]