from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import (
    User, Role, Permission, Group, AcademicYear, Position, Major, Subject,
    StaffDetail, TeacherDetail, StudentDetail, Class, TeacherSubject,
    UserGroupMembership, RolePermission
)
import json

class AuthenticationTests(APITestCase):
    """Pengujian untuk endpoint autentikasi"""
    
    def setUp(self):
        # Membuat user untuk pengujian
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'address': 'Test Address',
            'phone_number': '081234567890',
            'status': 'active'
        }
        self.client = APIClient()
    
    def test_user_registration(self):
        """Pengujian registrasi pengguna"""
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
    
    def test_user_login(self):
        """Pengujian login pengguna"""
        # Membuat user terlebih dahulu
        User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        url = reverse('user-login')
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Login successful')

class UserViewSetTests(APITestCase):
    """Pengujian untuk UserViewSet"""
    
    def setUp(self):
        # Membuat user untuk pengujian
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'address': 'Test Address',
            'phone_number': '081234567890',
            'status': 'active'
        }
    
    def test_create_user(self):
        """Pengujian membuat user baru"""
        url = reverse('user-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # admin + new user
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)
    
    def test_get_user_list(self):
        """Pengujian mendapatkan daftar user"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # hanya admin user
    
    def test_get_user_detail(self):
        """Pengujian mendapatkan detail user"""
        url = reverse('user-detail', args=[self.admin_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'admin')
    
    def test_update_user(self):
        """Pengujian memperbarui user"""
        url = reverse('user-detail', args=[self.admin_user.id])
        update_data = {
            'username': 'adminupdated',
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'Updated',
            'address': 'Updated Address',
            'phone_number': '089876543210',
        }
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.username, 'adminupdated')
        self.assertEqual(self.admin_user.last_name, 'Updated')
    
    def test_delete_user(self):
        """Pengujian menghapus user"""
        # Membuat user baru untuk dihapus
        user = User.objects.create_user(
            username='userdelete',
            email='delete@example.com',
            password='deletepassword123'
        )
        
        url = reverse('user-detail', args=[user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(username='userdelete').count(), 0)

class RoleViewSetTests(APITestCase):
    """Pengujian untuk RoleViewSet"""
    
    def setUp(self):
        # Membuat user admin untuk autentikasi
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        
        # Data role untuk pengujian
        self.role_data = {
            'role_name': 'Teacher',
            'description': 'Role for teachers'
        }
    
    def test_create_role(self):
        """Pengujian membuat role baru"""
        url = reverse('role-list')
        response = self.client.post(url, self.role_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 1)
        self.assertEqual(Role.objects.get().role_name, 'Teacher')
    
    def test_get_role_list(self):
        """Pengujian mendapatkan daftar role"""
        # Membuat beberapa role
        Role.objects.create(role_name='Teacher', description='Role for teachers')
        Role.objects.create(role_name='Student', description='Role for students')
        
        url = reverse('role-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_role_detail(self):
        """Pengujian mendapatkan detail role"""
        role = Role.objects.create(role_name='Teacher', description='Role for teachers')
        
        url = reverse('role-detail', args=[role.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role_name'], 'Teacher')
    
    def test_update_role(self):
        """Pengujian memperbarui role"""
        role = Role.objects.create(role_name='Teacher', description='Role for teachers')
        
        url = reverse('role-detail', args=[role.id])
        update_data = {
            'role_name': 'Senior Teacher',
            'description': 'Role for senior teachers'
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        role.refresh_from_db()
        self.assertEqual(role.role_name, 'Senior Teacher')
        self.assertEqual(role.description, 'Role for senior teachers')
    
    def test_delete_role(self):
        """Pengujian menghapus role"""
        role = Role.objects.create(role_name='Teacher', description='Role for teachers')
        
        url = reverse('role-detail', args=[role.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Role.objects.count(), 0)

class AcademicYearViewSetTests(APITestCase):
    """Pengujian untuk AcademicYearViewSet"""
    
    def setUp(self):
        # Membuat user admin untuk autentikasi
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        
        # Data tahun akademik untuk pengujian
        self.academic_year_data = {
            'year_name': '2023/2024',
            'start_date': '2023-07-01',
            'end_date': '2024-06-30',
            'is_active': True
        }
    
    def test_create_academic_year(self):
        """Pengujian membuat tahun akademik baru"""
        url = reverse('academicyear-list')
        response = self.client.post(url, self.academic_year_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AcademicYear.objects.count(), 1)
        self.assertEqual(AcademicYear.objects.get().year_name, '2023/2024')
    
    def test_get_academic_year_list(self):
        """Pengujian mendapatkan daftar tahun akademik"""
        # Membuat beberapa tahun akademik
        AcademicYear.objects.create(
            year_name='2023/2024',
            start_date='2023-07-01',
            end_date='2024-06-30',
            is_active=True
        )
        AcademicYear.objects.create(
            year_name='2024/2025',
            start_date='2024-07-01',
            end_date='2025-06-30',
            is_active=False
        )
        
        url = reverse('academicyear-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class MajorViewSetTests(APITestCase):
    """Pengujian untuk MajorViewSet"""
    
    def setUp(self):
        # Membuat user admin untuk autentikasi
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        
        # Data jurusan untuk pengujian
        self.major_data = {
            'major_name': 'Teknik Informatika',
            'major_code': 'TI'
        }
    
    def test_create_major(self):
        """Pengujian membuat jurusan baru"""
        url = reverse('major-list')
        response = self.client.post(url, self.major_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Major.objects.count(), 1)
        self.assertEqual(Major.objects.get().major_name, 'Teknik Informatika')
    
    def test_get_major_list(self):
        """Pengujian mendapatkan daftar jurusan"""
        # Membuat beberapa jurusan
        Major.objects.create(major_name='Teknik Informatika', major_code='TI')
        Major.objects.create(major_name='Sistem Informasi', major_code='SI')
        
        url = reverse('major-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)