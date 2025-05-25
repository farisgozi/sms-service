import requests
import json
import sys
import os
import base64

# URL base API
BASE_URL = "http://127.0.0.1:8000/api"

# Warna untuk output
COLORS = {
    'HEADER': '\033[95m',
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m'
}

# Fungsi untuk mencetak dengan warna
def print_colored(text, color):
    if os.name == 'nt':  # Windows tidak mendukung ANSI color codes di cmd default
        print(text)
    else:
        print(f"{COLORS[color]}{text}{COLORS['ENDC']}")

# Fungsi untuk mencetak response dengan format yang bagus
def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        formatted_json = json.dumps(response.json(), indent=2, ensure_ascii=False)
        print(formatted_json)
    except:
        print(response.text)
    print("\n" + "-"*50 + "\n")

# Fungsi untuk registrasi pengguna
def register_user():
    print_colored("REGISTRASI PENGGUNA BARU", 'HEADER')
    url = f"{BASE_URL}/users/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "role": 1,  # Asumsi ID role = 1 untuk siswa
        "address": "Jl. Test No. 123",
        "phone_number": "081234567890"
    }
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data)
    print_response(response)
    return response

# Fungsi untuk login pengguna
def login_user():
    print_colored("LOGIN PENGGUNA", 'HEADER')
    url = f"{BASE_URL}/users/login/"
    data = {
        "email": "ojigoji5@gmail.com",
        "password": "nianajoyyi1503"
    }
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data)
    print_response(response)
    if response.status_code == 200:
        return response.json().get('token')
    return None

# Fungsi untuk mendapatkan headers dengan token
def get_auth_headers(token):
    if token:
        return {'Authorization': f'Token {token}'}
    return {}

# Fungsi untuk membuat Basic Auth header
def get_auth_header(username, password):
    auth_str = f"{username}:{password}"
    auth_bytes = auth_str.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    return auth_b64

# Fungsi untuk mendapatkan daftar pengguna
def get_users(token=None):
    print_colored("MENDAPATKAN DAFTAR PENGGUNA", 'HEADER')
    url = f"{BASE_URL}/users/"
    headers = get_auth_headers(token)
    print(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update pengguna
def update_user(user_id, token=None):
    print_colored("UPDATE DATA PENGGUNA", 'HEADER')
    url = f"{BASE_URL}/users/{user_id}/"
    data = {
        "address": "Jl. Update No. 456",
        "phone_number": "087654321098"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat tahun akademik
def create_academic_year(token=None):
    print_colored("MEMBUAT TAHUN AKADEMIK BARU", 'HEADER')
    url = f"{BASE_URL}/academic-years/"
    data = {
        "year_name": "2023/2024",
        "start_date": "2023-07-01",
        "end_date": "2024-06-30",
        "is_active": True
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk mendapatkan daftar tahun akademik
def get_academic_years(token=None):
    print_colored("MENDAPATKAN DAFTAR TAHUN AKADEMIK", 'HEADER')
    url = f"{BASE_URL}/academic-years/"
    headers = get_auth_headers(token)
    print(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update tahun akademik
def update_academic_year(year_id, token=None):
    print_colored("UPDATE TAHUN AKADEMIK", 'HEADER')
    url = f"{BASE_URL}/academic-years/{year_id}/"
    data = {
        "is_active": False
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat jurusan
def create_major(token=None):
    print_colored("MEMBUAT JURUSAN BARU", 'HEADER')
    url = f"{BASE_URL}/majors/"
    data = {
        "major_name": "Teknik Informatika",
        "major_code": "TI"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk mendapatkan daftar jurusan
def get_majors(token=None):
    print_colored("MENDAPATKAN DAFTAR JURUSAN", 'HEADER')
    url = f"{BASE_URL}/majors/"
    headers = get_auth_headers(token)
    print(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update jurusan
def update_major(major_id, token=None):
    print_colored("UPDATE JURUSAN", 'HEADER')
    url = f"{BASE_URL}/majors/{major_id}/"
    data = {
        "major_name": "Teknik Informatika dan Komputer"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat mata pelajaran
def create_subject(token=None):
    print_colored("MEMBUAT MATA PELAJARAN BARU", 'HEADER')
    url = f"{BASE_URL}/subjects/"
    data = {
        "subject_name": "Matematika",
        "subject_code": "MTK"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk mendapatkan daftar mata pelajaran
def get_subjects(token=None):
    print_colored("MENDAPATKAN DAFTAR MATA PELAJARAN", 'HEADER')
    url = f"{BASE_URL}/subjects/"
    headers = get_auth_headers(token)
    print(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update mata pelajaran
def update_subject(subject_id, token=None):
    print_colored("UPDATE MATA PELAJARAN", 'HEADER')
    url = f"{BASE_URL}/subjects/{subject_id}/"
    data = {
        "subject_name": "Matematika Dasar"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat role
def create_role(token=None):
    print_colored("MEMBUAT ROLE BARU", 'HEADER')
    url = f"{BASE_URL}/roles/"
    data = {
        "role_name": "Guru",
        "description": "Role untuk Guru"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk mendapatkan daftar role
def get_roles(token=None):
    print_colored("MENDAPATKAN DAFTAR ROLE", 'HEADER')
    url = f"{BASE_URL}/roles/"
    headers = get_auth_headers(token)
    print(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update role
def update_role(role_id, token=None):
    print_colored("UPDATE ROLE", 'HEADER')
    url = f"{BASE_URL}/roles/{role_id}/"
    data = {
        "description": "Role untuk siswa aktif"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat permission
def create_permission(token=None):
    print_colored("MEMBUAT PERMISSION BARU", 'HEADER')
    url = f"{BASE_URL}/permissions/"
    data = {
        "permission_name": "view_profile",
        "description": "Izin untuk melihat profil"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update permission
def update_permission(permission_id, token=None):
    print_colored("UPDATE PERMISSION", 'HEADER')
    url = f"{BASE_URL}/permissions/{permission_id}/"
    data = {
        "description": "Izin untuk melihat dan mengedit profil"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat group
def create_group(token=None):
    print_colored("MEMBUAT GROUP BARU", 'HEADER')
    url = f"{BASE_URL}/groups/"
    data = {
        "group_name": "Kelas X",
        "description": "Grup untuk siswa kelas X"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update group
def update_group(group_id, token=None):
    print_colored("UPDATE GROUP", 'HEADER')
    url = f"{BASE_URL}/groups/{group_id}/"
    data = {
        "description": "Grup untuk siswa kelas X Semester 1"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat posisi
def create_position(token=None):
    print_colored("MEMBUAT POSISI BARU", 'HEADER')
    url = f"{BASE_URL}/positions/"
    data = {
        "position_name": "Guru Matematika",
        "position_code": "GM",
        "description": "Posisi untuk guru matematika",
        "position_type": "Akademik"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update posisi
def update_position(position_id, token=None):
    print_colored("UPDATE POSISI", 'HEADER')
    url = f"{BASE_URL}/positions/{position_id}/"
    data = {
        "description": "Posisi untuk guru matematika senior"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat kelas
def create_class(token=None):
    print_colored("MEMBUAT KELAS BARU", 'HEADER')
    url = f"{BASE_URL}/classes/"
    data = {
        "class_name": "X-TI-1",
        "grade_level": 10,
        "academic_year": 1,  # Asumsi ID tahun akademik = 1
        "major": 1  # Asumsi ID jurusan = 1
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update kelas
def update_class(class_id, token=None):
    print_colored("UPDATE KELAS", 'HEADER')
    url = f"{BASE_URL}/classes/{class_id}/"
    data = {
        "class_name": "X-TI-1A"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat detail guru
def create_teacher_detail(token=None):
    print_colored("MEMBUAT DETAIL GURU BARU", 'HEADER')
    url = f"{BASE_URL}/teacher-details/"
    data = {
        "user_id": 1,  # Asumsi ID user = 1
        "nip": "198501012010011001",
        "position": 1,  # Asumsi ID posisi = 1
        "major": 1,  # Asumsi ID jurusan = 1
        "is_principal": False
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update detail guru
def update_teacher_detail(teacher_id, token=None):
    print_colored("UPDATE DETAIL GURU", 'HEADER')
    url = f"{BASE_URL}/teacher-details/{teacher_id}/"
    data = {
        "is_principal": True
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat detail siswa
def create_student_detail(token=None):
    print_colored("MEMBUAT DETAIL SISWA BARU", 'HEADER')
    url = f"{BASE_URL}/student-details/"
    data = {
        "user_id": 2,  # Asumsi ID user = 2
        "nisn": "0012345678",
        "class_field": 1,  # Asumsi ID kelas = 1
        "major": 1,  # Asumsi ID jurusan = 1
        "entry_year": 2023,
        "parent_guardian_name": "Orang Tua Siswa",
        "parent_guardian_phone": "081234567890"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update detail siswa
def update_student_detail(student_id, token=None):
    print_colored("UPDATE DETAIL SISWA", 'HEADER')
    url = f"{BASE_URL}/student-details/{student_id}/"
    data = {
        "parent_guardian_phone": "087654321098"
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk membuat relasi guru dan mata pelajaran
def create_teacher_subject(token=None):
    print_colored("MEMBUAT RELASI GURU DAN MATA PELAJARAN BARU", 'HEADER')
    url = f"{BASE_URL}/teacher-subjects/"
    data = {
        "teacher": 1,  # Asumsi ID detail guru = 1
        "subject": 1,  # Asumsi ID mata pelajaran = 1
        "class_field": 1,  # Asumsi ID kelas = 1
        "academic_year": 1  # Asumsi ID tahun akademik = 1
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"POST {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk update relasi guru dan mata pelajaran
def update_teacher_subject(teacher_subject_id, token=None):
    print_colored("UPDATE RELASI GURU DAN MATA PELAJARAN", 'HEADER')
    url = f"{BASE_URL}/teacher-subjects/{teacher_subject_id}/"
    data = {
        "class_field": 2  # Asumsi ID kelas baru = 2
    }
    headers = get_auth_headers(token)
    headers["Content-Type"] = "application/json"
    print(f"PATCH {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    response = requests.patch(url, json=data, headers=headers)
    print_response(response)
    return response

# Fungsi untuk menampilkan menu
def show_menu():
    print_colored("\nMENU PENGUJIAN API SISTEM MANAJEMEN SEKOLAH", 'BOLD')
    print("1. Registrasi Pengguna")
    print("2. Login Pengguna")
    print("3. Mendapatkan Daftar Pengguna")
    print("4. Update Data Pengguna")
    print("5. Membuat Tahun Akademik Baru")
    print("6. Update Tahun Akademik")
    print("7. Membuat Jurusan Baru")
    print("8. Update Jurusan")
    print("9. Membuat Mata Pelajaran Baru")
    print("10. Update Mata Pelajaran")
    print("11. Membuat Role Baru")
    print("12. Update Role")
    print("13. Membuat Permission Baru")
    print("14. Update Permission")
    print("15. Membuat Group Baru")
    print("16. Update Group")
    print("17. Membuat Posisi Baru")
    print("18. Update Posisi")
    print("19. Membuat Kelas Baru")
    print("20. Update Kelas")
    print("21. Membuat Detail Guru Baru")
    print("22. Update Detail Guru")
    print("23. Membuat Detail Siswa Baru")
    print("24. Update Detail Siswa")
    print("25. Membuat Relasi Guru dan Mata Pelajaran")
    print("26. Update Relasi Guru dan Mata Pelajaran")
    print("27. Mendapatkan Daftar Tahun Akademik")
    print("28. Mendapatkan Daftar Jurusan")
    print("29. Mendapatkan Daftar Mata Pelajaran")
    print("30. Mendapatkan Daftar Role")
    print("31. Menjalankan Semua Pengujian")
    print("0. Keluar")
    choice = input("\nPilih menu (0-31): ")
    return choice

# Fungsi utama
def main():
    while True:
        choice = show_menu()
        
        # Login terlebih dahulu untuk mendapatkan token
        if choice != '0' and choice != '1' and choice != '2':
            token = login_user()
            if not token:
                print_colored("Gagal login! Tidak bisa melanjutkan test.", 'FAIL')
                continue
            print_colored("\nBerhasil login! Melanjutkan dengan test API...", 'GREEN')
        
        if choice == '0':
            break
        elif choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            get_users(token)
        elif choice == '4':
            user_id = input("Masukkan ID pengguna yang akan diupdate: ")
            update_user(user_id, token)
        elif choice == '5':
            create_academic_year(token)
        elif choice == '6':
            year_id = input("Masukkan ID tahun akademik yang akan diupdate: ")
            update_academic_year(year_id, token)
        elif choice == '7':
            create_major(token)
        elif choice == '8':
            major_id = input("Masukkan ID jurusan yang akan diupdate: ")
            update_major(major_id, token)
        elif choice == '9':
            create_subject(token)
        elif choice == '10':
            subject_id = input("Masukkan ID mata pelajaran yang akan diupdate: ")
            update_subject(subject_id, token)
        elif choice == '11':
            create_role(token)
        elif choice == '12':
            role_id = input("Masukkan ID role yang akan diupdate: ")
            update_role(role_id, token)
        elif choice == '13':
            create_permission(token)
        elif choice == '14':
            permission_id = input("Masukkan ID permission yang akan diupdate: ")
            update_permission(permission_id, token)
        elif choice == '15':
            create_group(token)
        elif choice == '16':
            group_id = input("Masukkan ID group yang akan diupdate: ")
            update_group(group_id, token)
        elif choice == '17':
            create_position(token)
        elif choice == '18':
            position_id = input("Masukkan ID posisi yang akan diupdate: ")
            update_position(position_id, token)
        elif choice == '19':
            create_class(token)
        elif choice == '20':
            class_id = input("Masukkan ID kelas yang akan diupdate: ")
            update_class(class_id, token)
        elif choice == '21':
            create_teacher_detail(token)
        elif choice == '22':
            teacher_id = input("Masukkan ID detail guru yang akan diupdate: ")
            update_teacher_detail(teacher_id, token)
        elif choice == '23':
            create_student_detail(token)
        elif choice == '24':
            student_id = input("Masukkan ID detail siswa yang akan diupdate: ")
            update_student_detail(student_id, token)
        elif choice == '25':
            create_teacher_subject(token)
        elif choice == '26':
            teacher_subject_id = input("Masukkan ID relasi guru dan mata pelajaran yang akan diupdate: ")
            update_teacher_subject(teacher_subject_id, token)
        elif choice == '27':
            get_academic_years(token)
        elif choice == '28':
            get_majors(token)
        elif choice == '29':
            get_subjects(token)
        elif choice == '30':
            get_roles(token)
        elif choice == '31':
            # Jalankan semua fungsi test
            get_users(token)
            create_role(token)
            update_role(1, token)
            get_roles(token)
            create_academic_year(token)
            update_academic_year(1, token)
            get_academic_years(token)
            create_major(token)
            update_major(1, token)
            get_majors(token)
            create_subject(token)
            update_subject(1, token)
            get_subjects(token)

if __name__ == "__main__":
    main()