from django.contrib import admin
from .models import (
    User, Role, Permission, Group, AcademicYear, Position, Major, Subject,
    StaffDetail, TeacherDetail, StudentDetail, Class, TeacherSubject,
    UserGroupMembership, RolePermission
)

# Register models to admin site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'status', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'role__role_name')
    list_filter = ('status', 'is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('address', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'role')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
        ('Status', {'fields': ('status',)}),
    )
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    ordering = ('username',)

# admin.site.register(User) # Komentari atau hapus ini karena sudah menggunakan @admin.register(User)
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
