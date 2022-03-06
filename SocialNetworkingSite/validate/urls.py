from django.urls import path, include
from . import views as v_views
from karamel import views as k_views
urlpatterns = [
    path('', v_views.index, name="index"),
    path('login', v_views.login, name="login"),
    path('signup', v_views.signup, name="signup"),
    path('about', v_views.about, name="about"),
    path('register', v_views.register, name="register"),
    path("auth", v_views.auth, name="auth"),
    path('setup', v_views.setup, name="setup"),
    path('karamel', k_views.karamel, name="karamel"),
    path('blogform/', k_views.blogform, name="blogform"),
    path('blogform/uploadblog', k_views.uploadblog, name="uploadblog"),
    path('blogfeed', k_views.blogfeed, name="blogfeed"),
    path('updateform', k_views.updateform, name="updateform"),
    path('changeprofile', k_views.changeprofile, name="changeprofile"),
    path('addfriend', k_views.addfriend, name="addfriend"),
    path('linkfriend', k_views.linkfriend, name="linkfriend"),
    path('friend', k_views.friend, name="friend"),
    path('managereq', k_views.managereq, name="managereq"),
        
]
