from django.urls import path
from Blog import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('blogs/', views.ManageBlogs.as_view())
]
