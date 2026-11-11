from rest_framework.routers import DefaultRouter
from .views import WorkingScheduleViewSet
router = DefaultRouter()
router.register("", WorkingScheduleViewSet, basename="schedule")
urlpatterns = router.urls

