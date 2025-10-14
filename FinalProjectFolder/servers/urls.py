from django.urls import path

from . import views

app_name = 'servers'

urlpatterns = [
    path('', views.index, name='index'),
    path('hosts/', views.host_sheet, name='host_sheet'),
    path('sas/', views.sa_sheet, name='sa_sheet'),
    path('export/', views.export_teamsheet, name='export_teamsheet'),
]
