from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, RoleViewSet, PermissionViewSet, GroupViewSet,
    AcademicYearViewSet, PositionViewSet, MajorViewSet, SubjectViewSet,
    StaffDetailViewSet, TeacherDetailViewSet, StudentDetailViewSet,
    ClassViewSet, TeacherSubjectViewSet, UserGroupMembershipViewSet,
    RolePermissionViewSet
)

from attendance.urls import router as attendance_router

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'majors', MajorViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'staff-details', StaffDetailViewSet)
router.register(r'teacher-details', TeacherDetailViewSet)
router.register(r'student-details', StudentDetailViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'teacher-subjects', TeacherSubjectViewSet)
router.register(r'user-group-memberships', UserGroupMembershipViewSet)
router.register(r'role-permissions', RolePermissionViewSet)

# Gabungkan router dari attendance
for prefix, viewset, basename in attendance_router.registry:
    router.register(prefix, viewset, basename)

urlpatterns = [
    path('', include(router.urls)),
    # Endpoint khusus untuk autentikasi
    path('auth/', include('rest_framework.urls')),
]