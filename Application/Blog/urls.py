from rest_framework.routers import DefaultRouter
from Application.Blog import views

urlpatterns = [
]

router = DefaultRouter()
router.register('', views.Blogs)

urlpatterns += router.urls
