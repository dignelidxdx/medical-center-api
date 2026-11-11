from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import Appointment
from .services import validate_appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
    def validate(self, attrs):
        instance = self.instance or Appointment()
        previous_status = self.instance.status if self.instance else None
        for field, value in attrs.items():
            setattr(instance, field, value)
        if previous_status in {Appointment.Status.CANCELLED, Appointment.Status.COMPLETED} and instance.status != previous_status:
            raise serializers.ValidationError("Cancelled or completed appointments cannot change status")
        try: validate_appointment(instance)
        except DjangoValidationError as exc: raise serializers.ValidationError(exc.messages)
        return attrs

