from django.urls import path,include
from . import views
app_name = 'Blog'
urlpatterns = [
    path("",views.index,name='index'),
    path("<int:p>",views.index,name='index'),
    path("Post-By-Category/<slug:slug>/<int:c>/<int:p>",views.categoryPost,name='categoryPost'),
    path("Post-By-Tag/<slug:slug>/<int:t>/<int:p>",views.tagedPost,name='tagPost'),
    path('BlogDetail/<int:id>/<slug:slug>',views.postDetails,name='PostDetails'),
    path('About-Prins-Singh',views.About,name="PrinsSingh"),
    path('Contact-Page',views.contact,name='Contact'),
    path('Login-Page',views.login,name="Login"),
    path("User-Profile",views.Profile,name="Profile"),
    path('logout',views.logout,name="Logout"),
    path('Registration-Page',views.register,name='Register'),
    path("Forget-Password",views.forgetPassword,name="ForgetPassword"),
    path('Reset-Your-Password',views.resetPassword,name="ResetPassword"),
    path("OTP-confirmation-Page",views.confirmOTP,name="confirmOTP"),
    path("Resend-OTP/<email>",views.resendOTP,name="resendOTP"),
    path("Comment",views.commentOnPost,name="comment"),
    path("Like/<int:uid>/<int:pid>",views.PostLike,name="Like"),
    path("dis-like/<int:uid>/<int:pid>",views.PostDisLike,name="DisLike"),
    path("Subscribe",views.subscribe,name='subscribe'),
    path("search",views.search,name="search"),
     path("search/<int:p>",views.search,name="search"),
]
