from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('account/', views.AccountView.as_view(), name='account'),
]


