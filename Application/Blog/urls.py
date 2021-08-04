from rest_framework.routers import DefaultRouter
from Application.Blog import views

urlpatterns = [
]

router = DefaultRouter()
router.register('blog', views.Blogs)
router.register('comment', views.Comments)
urlpatterns += router.urls
