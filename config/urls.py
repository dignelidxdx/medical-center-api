from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.response import Response
from rest_framework.views import APIView

class HealthView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        return Response({"status": "ok"})

urlpatterns = [path("admin/", admin.site.urls), path("health/", HealthView.as_view()), path("api/schema/", SpectacularAPIView.as_view()), path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")), path("api/v1/specialties/", include("specialists.urls_specialties")), path("api/v1/specialists/", include("specialists.urls")), path("api/v1/patients/", include("patients.urls")), path("api/v1/offices/", include("facilities.urls")), path("api/v1/schedules/", include("scheduling.urls")), path("api/v1/appointments/", include("appointments.urls"))]

