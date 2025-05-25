from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Model untuk Tahun Akademik
class AcademicYear(models.Model):
    year_name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.year_name

# Model untuk Jabatan/Posisi
class Position(models.Model):
    POSITION_TYPES = (
        ('Akademik', 'Akademik'),
        ('Non-Akademik', 'Non-Akademik'),
        ('Manajerial', 'Manajerial'),
        ('Pendukung', 'Pendukung'),
    )
    
    position_name = models.CharField(max_length=255, unique=True)
    position_code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    position_type = models.CharField(max_length=20, choices=POSITION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.position_name

# Model untuk Jurusan
class Major(models.Model):
    major_name = models.CharField(max_length=255, unique=True)
    major_code = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.major_name

# Model untuk Mata Pelajaran
class Subject(models.Model):
    subject_name = models.CharField(max_length=255, unique=True)
    subject_code = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.subject_name

# Model untuk Peran Pengguna
class Role(models.Model):
    role_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.role_name

# Model untuk Izin/Permission
class Permission(models.Model):
    permission_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.permission_name

# Model untuk Kelompok Pengguna
class Group(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.group_name

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email harus diisi')
        if not username:
            raise ValueError('Username harus diisi')
            
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', 'active')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser harus memiliki is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser harus memiliki is_superuser=True')
        
        # Membuat atau mendapatkan role admin
        admin_role, created = Role.objects.get_or_create(
            role_name='Admin',
            defaults={'description': 'Administrator dengan akses penuh ke sistem'}
        )
        extra_fields['role'] = admin_role
            
        return self.create_user(username, email, password, **extra_fields)

# Model User Kustom
class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    )
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Tambahan untuk Django admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username

# Model untuk Detail Staff
class StaffDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nip = models.CharField(max_length=100, unique=True, blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - Staff"

# Model untuk Detail Guru
class TeacherDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nip = models.CharField(max_length=100, unique=True, blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True)
    is_principal = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - Guru"

# Model untuk Kelas
class Class(models.Model):
    class_name = models.CharField(max_length=255)
    grade_level = models.IntegerField()
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.RESTRICT)
    homeroom_teacher = models.ForeignKey(TeacherDetail, on_delete=models.SET_NULL, null=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.class_name} - {self.academic_year.year_name}"
    
    class Meta:
        verbose_name_plural = 'Classes'

# Model untuk Detail Siswa
class StudentDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nisn = models.CharField(max_length=100, unique=True, blank=True, null=True)
    class_field = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, db_column='class_id')
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True)
    entry_year = models.IntegerField(blank=True, null=True)
    parent_guardian_name = models.CharField(max_length=255, blank=True, null=True)
    parent_guardian_phone = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - Siswa"

# Model untuk Relasi Guru dan Mata Pelajaran
class TeacherSubject(models.Model):
    teacher = models.ForeignKey(TeacherDetail, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('teacher', 'subject', 'class_field', 'academic_year')
    
    def __str__(self):
        return f"{self.teacher.user.username} - {self.subject.subject_name} - {self.class_field.class_name}"

# Model untuk Relasi User dan Group
class UserGroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'group')
    
    def __str__(self):
        return f"{self.user.username} - {self.group.group_name}"

# Model untuk Relasi Role dan Permission
class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('role', 'permission')
    
    def __str__(self):
        return f"{self.role.role_name} - {self.permission.permission_name}"
