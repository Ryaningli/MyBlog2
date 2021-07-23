from django.urls import path, include

urlpatterns = [
    path('user/', include('Application.User.urls')),
    path('blog/', include('Application.Blog.urls'))
]