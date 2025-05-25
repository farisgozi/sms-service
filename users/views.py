from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import (
    User, Role, Permission, Group, AcademicYear, Position, Major, Subject,
    StaffDetail, TeacherDetail, StudentDetail, Class, TeacherSubject,
    UserGroupMembership, RolePermission
)
from .serializers import (
    UserSerializer, RoleSerializer, PermissionSerializer, GroupSerializer,
    AcademicYearSerializer, PositionSerializer, MajorSerializer, SubjectSerializer,
    StaffDetailSerializer, TeacherDetailSerializer, StudentDetailSerializer,
    ClassSerializer, TeacherSubjectSerializer, UserGroupMembershipSerializer,
    RolePermissionSerializer, UserRegistrationSerializer, UserLoginSerializer
)

# ViewSet untuk model Role
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# ViewSet untuk model Permission
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

# ViewSet untuk model Group
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# ViewSet untuk model AcademicYear
class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer

# ViewSet untuk model Position
class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

# ViewSet untuk model Major
class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

# ViewSet untuk model Subject
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

# ViewSet untuk model User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['register', 'login']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Memastikan pengguna hanya dapat memperbarui data mereka sendiri
        if instance.id != request.user.id:
            return Response({
                'message': 'You do not have permission to update this user'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User updated successfully',
                'user': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                # Membuat atau mendapatkan token untuk user
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Login successful',
                    'user': UserSerializer(user).data,
                    'token': token.key
                })
            return Response({
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSet untuk model StaffDetail
class StaffDetailViewSet(viewsets.ModelViewSet):
    queryset = StaffDetail.objects.all()
    serializer_class = StaffDetailSerializer

# ViewSet untuk model TeacherDetail
class TeacherDetailViewSet(viewsets.ModelViewSet):
    queryset = TeacherDetail.objects.all()
    serializer_class = TeacherDetailSerializer

# ViewSet untuk model Class
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

# ViewSet untuk model StudentDetail
class StudentDetailViewSet(viewsets.ModelViewSet):
    queryset = StudentDetail.objects.all()
    serializer_class = StudentDetailSerializer

# ViewSet untuk model TeacherSubject
class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer

# ViewSet untuk model UserGroupMembership
class UserGroupMembershipViewSet(viewsets.ModelViewSet):
    queryset = UserGroupMembership.objects.all()
    serializer_class = UserGroupMembershipSerializer

# ViewSet untuk model RolePermission
class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
