from django.urls import include , re_path, path
from ParentApp import views

from django.conf.urls.static import static
from django.conf import settings

from ParentApp.views import RegisterView, LoginView, UserView, LogoutView

urlpatterns=[
    re_path(r'^games$',views.gamesApi),
    re_path(r'^games/([0-9]+)$',views.gamesApi),

    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),

    re_path(r'^users$',views.usersApi),
    re_path(r'^users/([0-9]+)$',views.usersApi),

    re_path(r'^users/savefile',views.SaveFile),
    re_path(r'^predict/([0-9]+)$',views.predictApi)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)