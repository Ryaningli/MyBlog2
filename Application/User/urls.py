from django.urls import path
from Application.User import views

urlpatterns = [
    path('login/', views.Login.as_view()),
    path('register/', views.Register.as_view())
]