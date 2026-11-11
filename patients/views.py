from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("last_name", "first_name")
    serializer_class = PatientSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get("search")
        if search: qs = qs.filter(first_name__icontains=search) | qs.filter(last_name__icontains=search) | qs.filter(document_number__icontains=search)
        return qs
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])

