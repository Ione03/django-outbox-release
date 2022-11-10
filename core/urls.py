from django.urls import include,path
from .views import upload_photo
urlpatterns=[path('dashboard/upload-photo/<int:width>/<int:height>/',upload_photo,name='upload_photo')]