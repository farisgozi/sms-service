from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AttendancePlatformViewSet, SchoolHolidaysOrEventsViewSet,
    AbsenceRequestsViewSet, AbsenceRequestsAttachmentsViewSet,
    AttendancesViewSet
)

router = DefaultRouter()
router.register(r'platforms', AttendancePlatformViewSet, basename='attendanceplatform')
router.register(r'holidays-events', SchoolHolidaysOrEventsViewSet, basename='schoolholidaysorevents')
router.register(r'absence-requests', AbsenceRequestsViewSet, basename='absencerequests')
router.register(r'absence-request-attachments', AbsenceRequestsAttachmentsViewSet, basename='absencerequestsattachments')
router.register(r'records', AttendancesViewSet, basename='attendances')

urlpatterns = [
    path('', include(router.urls)),
]