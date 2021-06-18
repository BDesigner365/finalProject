from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('gallery/', views.gallery),
    path('newUser/', views.users),
    path('register/', views.newUser),
    path('logout/', views.logout),
    path('menu/', views.menu),
    path('like/<int:id>', views.add_like),
    path('editProfile/<int:user_id>/updateProfile', views.updateProfile),
    path('editProfile/', views.editProfile),
    path('userProfile/', views.userProfile),
]
