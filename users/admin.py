from django.contrib import admin
from .models import (
    User, Role, Permission, Group, AcademicYear, Position, Major, Subject,
    StaffDetail, TeacherDetail, StudentDetail, Class, TeacherSubject,
    UserGroupMembership, RolePermission
)

# Register models to admin site
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Group)
admin.site.register(AcademicYear)
admin.site.register(Position)
admin.site.register(Major)
admin.site.register(Subject)
admin.site.register(StaffDetail)
admin.site.register(TeacherDetail)
admin.site.register(StudentDetail)
admin.site.register(Class)
admin.site.register(TeacherSubject)
admin.site.register(UserGroupMembership)
admin.site.register(RolePermission)
