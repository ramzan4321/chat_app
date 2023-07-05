
from django.urls import path, include
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
 
 
urlpatterns = [
    # path("", chat_views.index, name="index"),
    path("", chat_views.chatPage, name="chat-page"),
 
    # login-section
    path("register/", chat_views.register, name="register"),
    path("edit_profile/", chat_views.editprofile, name="editprofile"),
    # path("auth/login/", LoginView.as_view
    #      (template_name="chat/LoginPage.html"), name="login-user"),
    path("login/", chat_views.login_user, name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path("getmessages/", chat_views.get_messages, name="get_message")
]