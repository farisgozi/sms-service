from rest_framework import serializers
from .models import (
    AttendancePlatform, SchoolHolidaysOrEvents, AbsenceRequests, 
    AbsenceRequestsAttachments, Attendances
)

class AttendancePlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendancePlatform
        fields = '__all__'

class SchoolHolidaysOrEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHolidaysOrEvents
        fields = '__all__'

class AbsenceRequestsAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceRequestsAttachments
        fields = '__all__'

class AbsenceRequestsSerializer(serializers.ModelSerializer):
    attachments = AbsenceRequestsAttachmentsSerializer(many=True, read_only=True)
    # Jika Anda ingin bisa membuat attachment saat membuat AbsenceRequest, Anda perlu custom create method
    # atau menggunakan nested writable serializer jika DRF versi Anda mendukungnya dengan baik.

    class Meta:
        model = AbsenceRequests
        fields = '__all__'
        read_only_fields = ('submitted_at', 'approval_timestamp', 'created_at', 'updated_at')

class AttendancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendances
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')