#from django.urls import path
#---------------------------------------
from django.urls import path, include
from django.contrib import admin
#--------------------------------------
from . import views

app_name = 'servers'

urlpatterns = [
    path('', views.index, name='index'),
    path('export/', views.export_teamsheet, name='export_teamsheet'),
    # path('',blog_views.show_post,name="show_post"), #Added by: Derek Gerry to show all servers at one time
    #_________________________________
    path('admin/', admin.site.urls),
    #path('', include('servers.urls')),
    #_________________________________
]
