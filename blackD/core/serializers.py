from datetime import timedelta
from rest_framework import serializers

from schedule.models import Event


class EventSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    tzoffset = serializers.IntegerField(required=False)

    def to_start(self):
        utc_offset = self.validated_data.get("tzoffset", 180)
        return self.validated_data["start"] + timedelta(minutes=utc_offset)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "start", "end", "tzoffset"]
        read_only_fields = ["id", "end"]


class CancelOccurrencesSerializer(serializers.Serializer):
    after_dt = serializers.DateTimeField(required=False, write_only=True)
