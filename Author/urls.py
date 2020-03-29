from django.urls import path,include
from . import views

app_name = 'Author'
urlpatterns = [
    path('',views.index,name='index'),
    path('Profile/',views.Profile,name='Profile'),
    path('add_NewBlog/',views.newBlog,name='NewBlog'),
    path('Authors_Blogs/',views.Personal_Blogs,name='Personal_Blogs'),
    path('Editblog/<int:id>',views.editBlog,name="Editblog"),
    path("DeletePost/<int:id>/",views.deletePost,name="DeletePost"),
    path('Update_Profile',views.Profile,name="Update_Profile"),
    path("Approve-comments/<int:id>/<t>",views.approveComment,name="Approve"),
    path("Pending-comments/<int:id>/<t>",views.pendingComment,name="Pending"),
    path("Reject-comments/<int:id>/<t>",views.rejectComment,name="Reject"),
    #path("Preview",views.preview,name="Preview"),
    path("dv/",views.getDataByDate),
]
