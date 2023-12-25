from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('v1/sinup/', views.UserSinupApi.as_view(), name='sinup-user'),
    # path('v1/change-password/', views.UserChangePasswordApi.as_view(), name='change-password-user'),
    path('v1/login/', obtain_auth_token, name='login'),
    path('v1/list/', views.ListCreateListApi.as_view(), name='create-list'),
    path('v1/listmanager/<slug:slug>', views.ListManager.as_view(), name='list-manager'),
]