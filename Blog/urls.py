from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from Blog import views


urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    # path('blogs/<int>/', views.ManageBlogs.as_view()),
]

router = DefaultRouter()
router.register('test', views.ManageBlogs)

urlpatterns += router.urls
