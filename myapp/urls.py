
from django.urls import path
from . import views

urlpatterns = [
  path('',views.upload_view, name='upload'),
  path('dashboard/', views.dashboard,   name='dashboard'),
]
