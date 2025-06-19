from rest_framework import viewsets, permissions
from .models import (
    AttendancePlatform, SchoolHolidaysOrEvents, AbsenceRequests,
    AbsenceRequestsAttachments, Attendances
)
from .serializers import (
    AttendancePlatformSerializer, SchoolHolidaysOrEventsSerializer,
    AbsenceRequestsSerializer, AbsenceRequestsAttachmentsSerializer, 
    AttendancesSerializer
)

class AttendancePlatformViewSet(viewsets.ModelViewSet):
    queryset = AttendancePlatform.objects.all()
    serializer_class = AttendancePlatformSerializer
    # permission_classes = [permissions.IsAuthenticated] # Sesuaikan dengan kebutuhan

class SchoolHolidaysOrEventsViewSet(viewsets.ModelViewSet):
    queryset = SchoolHolidaysOrEvents.objects.all()
    serializer_class = SchoolHolidaysOrEventsSerializer
    # permission_classes = [permissions.IsAuthenticated]

class AbsenceRequestsViewSet(viewsets.ModelViewSet):
    queryset = AbsenceRequests.objects.all()
    serializer_class = AbsenceRequestsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # Anda mungkin ingin menambahkan logika custom di sini, 
    # misalnya untuk memfilter permintaan berdasarkan pengguna yang login,
    # atau untuk menangani proses approval.

class AbsenceRequestsAttachmentsViewSet(viewsets.ModelViewSet):
    queryset = AbsenceRequestsAttachments.objects.all()
    serializer_class = AbsenceRequestsAttachmentsSerializer
    # permission_classes = [permissions.IsAuthenticated]

class AttendancesViewSet(viewsets.ModelViewSet):
    queryset = Attendances.objects.all()
    serializer_class = AttendancesSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # Logika custom bisa ditambahkan di sini, misalnya untuk:
    # - Memfilter absensi berdasarkan pengguna.
    # - Validasi saat clock-in atau clock-out.
    # - Integrasi dengan SchoolHolidaysOrEvents atau AbsenceRequests.