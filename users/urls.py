from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.ProfileView.as_view(), name='login'),
    path('create', views.SignUpView.as_view(), name='signup'),
]
