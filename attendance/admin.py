from django.contrib import admin
from .models import (
    AttendancePlatform, SchoolHolidaysOrEvents, AbsenceRequests, 
    AbsenceRequestsAttachments, Attendances
)

@admin.register(AttendancePlatform)
class AttendancePlatformAdmin(admin.ModelAdmin):
    list_display = ('status_code', 'status_name', 'is_agent_approval', 'created_at', 'updated_at')
    search_fields = ('status_code', 'status_name')
    list_filter = ('is_agent_approval',)

@admin.register(SchoolHolidaysOrEvents)
class SchoolHolidaysOrEventsAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date_start', 'event_date_end', 'is_school_off', 'target_audience_type', 'academic_year')
    search_fields = ('event_name', 'description')
    list_filter = ('is_school_off', 'target_audience_type', 'academic_year')
    date_hierarchy = 'event_date_start'

@admin.register(AbsenceRequests)
class AbsenceRequestsAdmin(admin.ModelAdmin):
    list_display = ('requester_user', 'absence_type_status', 'start_date', 'end_date', 'approval_status', 'submitted_at', 'approved_by_user')
    search_fields = ('requester_user__username', 'reason', 'approval_notes')
    list_filter = ('approval_status', 'absence_type_status', 'start_date')
    autocomplete_fields = ('requester_user', 'approved_by_user', 'absence_type_status')
    date_hierarchy = 'submitted_at'

@admin.register(AbsenceRequestsAttachments)
class AbsenceRequestsAttachmentsAdmin(admin.ModelAdmin):
    list_display = ('absence_request', 'file_name_original', 'file_mime_type', 'uploaded_at')
    search_fields = ('absence_request__requester_user__username', 'file_name_original')
    autocomplete_fields = ('absence_request',)

@admin.register(Attendances)
class AttendancesAdmin(admin.ModelAdmin):
    list_display = ('employee_user', 'attendance_date', 'attendance_status', 'clock_in_time', 'clock_out_time', 'event', 'recorded_by_user')
    search_fields = ('employee_user__username', 'notes')
    list_filter = ('attendance_status', 'attendance_date', 'event')
    autocomplete_fields = ('employee_user', 'attendance_status', 'event', 'recorded_by_user', 'absence_request')
    date_hierarchy = 'attendance_date'