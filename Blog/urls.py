from django.urls import path
from Blog import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('blogs/', views.Blogs.as_view())
]
