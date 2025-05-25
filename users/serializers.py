from rest_framework import serializers
from .models import (
    User, Role, Permission, Group, AcademicYear, Position, Major, Subject,
    StaffDetail, TeacherDetail, StudentDetail, Class, TeacherSubject,
    UserGroupMembership, RolePermission
)

# Serializer untuk model Role
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

# Serializer untuk model Permission
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

# Serializer untuk model Group
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

# Serializer untuk model AcademicYear
class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

# Serializer untuk model Position
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

# Serializer untuk model Major
class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'

# Serializer untuk model Subject
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

# Serializer untuk model User
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'address', 'phone_number', 
                  'profile_picture', 'role', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Serializer untuk model StaffDetail
class StaffDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = StaffDetail
        fields = ['user', 'user_id', 'nip', 'position', 'department']

# Serializer untuk model TeacherDetail
class TeacherDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = TeacherDetail
        fields = ['user', 'user_id', 'nip', 'position', 'major', 'is_principal']

# Serializer untuk model Class
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

# Serializer untuk model StudentDetail
class StudentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = StudentDetail
        fields = ['user', 'user_id', 'nisn', 'class_field', 'major', 'entry_year', 
                  'parent_guardian_name', 'parent_guardian_phone']

# Serializer untuk model TeacherSubject
class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubject
        fields = '__all__'

# Serializer untuk model UserGroupMembership
class UserGroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroupMembership
        fields = '__all__'

# Serializer untuk model RolePermission
class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'

# Serializer untuk registrasi user
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    address = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'role',
                 'address', 'phone_number', 'profile_picture']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Serializer untuk login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()