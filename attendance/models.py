from django.db import models
from users.models import User, AcademicYear

class AttendancePlatform(models.Model):
    status_code = models.CharField(max_length=50, unique=True)
    status_name = models.CharField(max_length=100)
    is_agent_approval = models.BooleanField(default=False, help_text='Apakah status ini memerlukan persetujuan?')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status_name

    class Meta:
        db_table = 'Attendance_Platform'
        verbose_name = 'Attendance Platform'
        verbose_name_plural = 'Attendance Platforms'

class SchoolHolidaysOrEvents(models.Model):
    AUDIENCE_CHOICES = [
        ('Students_Only', 'Students Only'),
        ('Teachers_Only', 'Teachers Only'),
        ('All_Users', 'All Users'),
    ]
    event_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_date_start = models.DateField()
    event_date_end = models.DateField()
    is_school_off = models.BooleanField(default=False, help_text='Apakah pada hari ini sekolah libur?')
    target_audience_type = models.CharField(max_length=20, choices=AUDIENCE_CHOICES)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = 'School_Holidays_Or_Events'
        verbose_name = 'School Holiday or Event'
        verbose_name_plural = 'School Holidays or Events'

class AbsenceRequests(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    requester_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='absence_requests_made', help_text='User yang mengajukan izin (Siswa/Guru/Staff)')
    absence_type_status = models.ForeignKey(AttendancePlatform, on_delete=models.RESTRICT, help_text='Jenis izin, FK ke Attendance_Platform (misal: Sakit, Izin, Cuti)')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS_CHOICES, default='Pending')
    approved_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='absence_requests_approved', help_text='User yang menyetujui (atasan/admin)')
    approval_timestamp = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Absence request by {self.requester_user.username} for {self.absence_type_status.status_name}"

    class Meta:
        db_table = 'Absence_Requests'
        verbose_name = 'Absence Request'
        verbose_name_plural = 'Absence Requests'

class AbsenceRequestsAttachments(models.Model):
    absence_request = models.ForeignKey(AbsenceRequests, on_delete=models.CASCADE, related_name='attachments')
    file_url = models.CharField(max_length=255)
    file_name_original = models.CharField(max_length=255, blank=True, null=True)
    file_mime_type = models.CharField(max_length=100, blank=True, null=True)
    file_size_bytes = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.absence_request_id}"

    class Meta:
        db_table = 'Absence_Requests_Attachments'
        verbose_name = 'Absence Request Attachment'
        verbose_name_plural = 'Absence Request Attachments'

class Attendances(models.Model):
    employee_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances_taken', help_text='User yang melakukan absensi (Guru/Staff)')
    attendance_date = models.DateField()
    attendance_status = models.ForeignKey(AttendancePlatform, on_delete=models.RESTRICT, help_text='Status kehadiran, FK ke Attendance_Platform')
    clock_in_time = models.TimeField(null=True, blank=True)
    clock_out_time = models.TimeField(null=True, blank=True)
    clock_in_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    clock_in_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    clock_in_photo_url = models.CharField(max_length=255, blank=True, null=True)
    clock_out_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    clock_out_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    clock_out_photo_url = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    attachment_url = models.CharField(max_length=255, blank=True, null=True)
    event = models.ForeignKey(SchoolHolidaysOrEvents, on_delete=models.SET_NULL, null=True, blank=True, help_text='Jika hari ini adalah event/libur, FK ke School_Holidays_Or_Events')
    recorded_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendances_recorded', help_text='User yang mencatat absensi ini jika dilakukan manual oleh admin')
    absence_request = models.ForeignKey(AbsenceRequests, on_delete=models.SET_NULL, null=True, blank=True, help_text='Jika absensi ini terkait dengan permintaan izin, FK ke Absence_Requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Attendance for {self.employee_user.username} on {self.attendance_date}"

    class Meta:
        db_table = 'Attendances'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'