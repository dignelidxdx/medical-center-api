from rest_framework.routers import DefaultRouter
from .views import SpecialistViewSet
router = DefaultRouter()
router.register("", SpecialistViewSet, basename="specialist")
urlpatterns = router.urls

