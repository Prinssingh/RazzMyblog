from django.urls import path,include
from . import views
from main.models import *

app_name="MyAdmin"
urlpatterns = [
   path('',views.index,name="index"),
   path("tables/",views.tables,name='tables'),




   path("preview",views.preview,name="Preview"),
   path("Delete-Function",views.delfunction,name="delfunction"),
   path("Update-User",views.updateUser,name="updateUser"),
   path('Send-message',views.messageAuthor,name="Message"),
   
    
]