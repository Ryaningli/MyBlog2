from django.urls import path
from rest_framework.routers import DefaultRouter
from Application.Blog import views

urlpatterns = [
    path('like/', views.Likes.as_view())
]

router = DefaultRouter()
router.register('blog', views.Blogs)
router.register('comment', views.Comments)
urlpatterns += router.urls
