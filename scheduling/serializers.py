from rest_framework import serializers
from .models import WorkingSchedule
class WorkingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingSchedule
        fields = "__all__"
    def validate(self, attrs):
        if attrs["start_time"] >= attrs["end_time"]: raise serializers.ValidationError("end_time must be after start_time")
        return attrs

