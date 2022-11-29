from django.urls import path,include
from .views import IndexView,DetailView
urlpatterns=[path('',IndexView.as_view(),name='education_index'),path('<str:kind>/detail/<slug:slug>/',DetailView.as_view(),name='education_detail')]