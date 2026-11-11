from rest_framework.routers import DefaultRouter
from .views import OfficeViewSet
router = DefaultRouter()
router.register("", OfficeViewSet, basename="office")
urlpatterns = router.urls

