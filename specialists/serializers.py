from rest_framework import serializers
from .models import Specialty, Specialist
class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = "__all__"
class SpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = "__all__"

