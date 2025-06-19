# Panduan Pengujian API Sistem Manajemen Sekolah

Dokumen ini berisi panduan untuk menguji semua API yang tersedia pada Sistem Manajemen Sekolah (SMS).

## Daftar Endpoint API

Berikut adalah daftar endpoint API yang tersedia pada sistem:

### Autentikasi
- `POST /api/users/register/` - Registrasi pengguna baru
- `POST /api/users/login/` - Login pengguna
- `GET /api/auth/` - Endpoint autentikasi Django REST Framework

### Pengguna (Users)
- `GET /api/users/` - Mendapatkan daftar pengguna
- `POST /api/users/` - Membuat pengguna baru
- `GET /api/users/{id}/` - Mendapatkan detail pengguna
- `PUT /api/users/{id}/` - Memperbarui pengguna
- `PATCH /api/users/{id}/` - Memperbarui sebagian data pengguna
- `DELETE /api/users/{id}/` - Menghapus pengguna

### Peran (Roles)
- `GET /api/roles/` - Mendapatkan daftar peran
- `POST /api/roles/` - Membuat peran baru
- `GET /api/roles/{id}/` - Mendapatkan detail peran
- `PUT /api/roles/{id}/` - Memperbarui peran
- `PATCH /api/roles/{id}/` - Memperbarui sebagian data peran
- `DELETE /api/roles/{id}/` - Menghapus peran

### Izin (Permissions)
- `GET /api/permissions/` - Mendapatkan daftar izin
- `POST /api/permissions/` - Membuat izin baru
- `GET /api/permissions/{id}/` - Mendapatkan detail izin
- `PUT /api/permissions/{id}/` - Memperbarui izin
- `PATCH /api/permissions/{id}/` - Memperbarui sebagian data izin
- `DELETE /api/permissions/{id}/` - Menghapus izin

### Grup (Groups)
- `GET /api/groups/` - Mendapatkan daftar grup
- `POST /api/groups/` - Membuat grup baru
- `GET /api/groups/{id}/` - Mendapatkan detail grup
- `PUT /api/groups/{id}/` - Memperbarui grup
- `PATCH /api/groups/{id}/` - Memperbarui sebagian data grup
- `DELETE /api/groups/{id}/` - Menghapus grup

### Tahun Akademik (Academic Years)
- `GET /api/academic-years/` - Mendapatkan daftar tahun akademik
- `POST /api/academic-years/` - Membuat tahun akademik baru
- `GET /api/academic-years/{id}/` - Mendapatkan detail tahun akademik
- `PUT /api/academic-years/{id}/` - Memperbarui tahun akademik
- `PATCH /api/academic-years/{id}/` - Memperbarui sebagian data tahun akademik
- `DELETE /api/academic-years/{id}/` - Menghapus tahun akademik

### Posisi (Positions)
- `GET /api/positions/` - Mendapatkan daftar posisi
- `POST /api/positions/` - Membuat posisi baru
- `GET /api/positions/{id}/` - Mendapatkan detail posisi
- `PUT /api/positions/{id}/` - Memperbarui posisi
- `PATCH /api/positions/{id}/` - Memperbarui sebagian data posisi
- `DELETE /api/positions/{id}/` - Menghapus posisi

### Jurusan (Majors)
- `GET /api/majors/` - Mendapatkan daftar jurusan
- `POST /api/majors/` - Membuat jurusan baru
- `GET /api/majors/{id}/` - Mendapatkan detail jurusan
- `PUT /api/majors/{id}/` - Memperbarui jurusan
- `PATCH /api/majors/{id}/` - Memperbarui sebagian data jurusan
- `DELETE /api/majors/{id}/` - Menghapus jurusan

### Mata Pelajaran (Subjects)
- `GET /api/subjects/` - Mendapatkan daftar mata pelajaran
- `POST /api/subjects/` - Membuat mata pelajaran baru
- `GET /api/subjects/{id}/` - Mendapatkan detail mata pelajaran
- `PUT /api/subjects/{id}/` - Memperbarui mata pelajaran
- `PATCH /api/subjects/{id}/` - Memperbarui sebagian data mata pelajaran
- `DELETE /api/subjects/{id}/` - Menghapus mata pelajaran

### Detail Staf (Staff Details)
- `GET /api/staff-details/` - Mendapatkan daftar detail staf
- `POST /api/staff-details/` - Membuat detail staf baru
- `GET /api/staff-details/{id}/` - Mendapatkan detail staf
- `PUT /api/staff-details/{id}/` - Memperbarui detail staf
- `PATCH /api/staff-details/{id}/` - Memperbarui sebagian data detail staf
- `DELETE /api/staff-details/{id}/` - Menghapus detail staf

### Detail Guru (Teacher Details)
- `GET /api/teacher-details/` - Mendapatkan daftar detail guru
- `POST /api/teacher-details/` - Membuat detail guru baru
- `GET /api/teacher-details/{id}/` - Mendapatkan detail guru
- `PUT /api/teacher-details/{id}/` - Memperbarui detail guru
- `PATCH /api/teacher-details/{id}/` - Memperbarui sebagian data detail guru
- `DELETE /api/teacher-details/{id}/` - Menghapus detail guru

### Detail Siswa (Student Details)
- `GET /api/student-details/` - Mendapatkan daftar detail siswa
- `POST /api/student-details/` - Membuat detail siswa baru
- `GET /api/student-details/{id}/` - Mendapatkan detail siswa
- `PUT /api/student-details/{id}/` - Memperbarui detail siswa
- `PATCH /api/student-details/{id}/` - Memperbarui sebagian data detail siswa
- `DELETE /api/student-details/{id}/` - Menghapus detail siswa

### Kelas (Classes)
- `GET /api/classes/` - Mendapatkan daftar kelas
- `POST /api/classes/` - Membuat kelas baru
- `GET /api/classes/{id}/` - Mendapatkan detail kelas
- `PUT /api/classes/{id}/` - Memperbarui kelas
- `PATCH /api/classes/{id}/` - Memperbarui sebagian data kelas
- `DELETE /api/classes/{id}/` - Menghapus kelas

### Guru Mata Pelajaran (Teacher Subjects)
- `GET /api/teacher-subjects/` - Mendapatkan daftar guru mata pelajaran
- `POST /api/teacher-subjects/` - Membuat guru mata pelajaran baru
- `GET /api/teacher-subjects/{id}/` - Mendapatkan detail guru mata pelajaran
- `PUT /api/teacher-subjects/{id}/` - Memperbarui guru mata pelajaran
- `PATCH /api/teacher-subjects/{id}/` - Memperbarui sebagian data guru mata pelajaran
- `DELETE /api/teacher-subjects/{id}/` - Menghapus guru mata pelajaran

### Keanggotaan Grup Pengguna (User Group Memberships)
- `GET /api/user-group-memberships/` - Mendapatkan daftar keanggotaan grup
- `POST /api/user-group-memberships/` - Membuat keanggotaan grup baru
- `GET /api/user-group-memberships/{id}/` - Mendapatkan detail keanggotaan grup
- `PUT /api/user-group-memberships/{id}/` - Memperbarui keanggotaan grup
- `PATCH /api/user-group-memberships/{id}/` - Memperbarui sebagian data keanggotaan grup
- `DELETE /api/user-group-memberships/{id}/` - Menghapus keanggotaan grup

### Modul Kehadiran (Attendance)

- **Attendance Platform (Status Kehadiran)**
  - `GET /api/attendance/platforms/` - Mendapatkan daftar status kehadiran
  - `POST /api/attendance/platforms/` - Membuat status kehadiran baru
  - `GET /api/attendance/platforms/{id}/` - Mendapatkan detail status kehadiran
  - `PUT /api/attendance/platforms/{id}/` - Memperbarui status kehadiran
  - `PATCH /api/attendance/platforms/{id}/` - Memperbarui sebagian data status kehadiran
  - `DELETE /api/attendance/platforms/{id}/` - Menghapus status kehadiran

- **School Holidays or Events (Hari Libur/Acara Sekolah)**
  - `GET /api/attendance/holidays-events/` - Mendapatkan daftar hari libur/acara sekolah
  - `POST /api/attendance/holidays-events/` - Membuat hari libur/acara sekolah baru
  - `GET /api/attendance/holidays-events/{id}/` - Mendapatkan detail hari libur/acara sekolah
  - `PUT /api/attendance/holidays-events/{id}/` - Memperbarui hari libur/acara sekolah
  - `PATCH /api/attendance/holidays-events/{id}/` - Memperbarui sebagian data hari libur/acara sekolah
  - `DELETE /api/attendance/holidays-events/{id}/` - Menghapus hari libur/acara sekolah

- **Absence Requests (Permintaan Izin)**
  - `GET /api/attendance/absence-requests/` - Mendapatkan daftar permintaan izin
  - `POST /api/attendance/absence-requests/` - Membuat permintaan izin baru
  - `GET /api/attendance/absence-requests/{id}/` - Mendapatkan detail permintaan izin
  - `PUT /api/attendance/absence-requests/{id}/` - Memperbarui permintaan izin
  - `PATCH /api/attendance/absence-requests/{id}/` - Memperbarui sebagian data permintaan izin
  - `DELETE /api/attendance/absence-requests/{id}/` - Menghapus permintaan izin

- **Absence Requests Attachments (Lampiran Permintaan Izin)**
  - `GET /api/attendance/absence-attachments/` - Mendapatkan daftar lampiran permintaan izin
  - `POST /api/attendance/absence-attachments/` - Membuat lampiran permintaan izin baru
  - `GET /api/attendance/absence-attachments/{id}/` - Mendapatkan detail lampiran permintaan izin
  - `PUT /api/attendance/absence-attachments/{id}/` - Memperbarui lampiran permintaan izin
  - `PATCH /api/attendance/absence-attachments/{id}/` - Memperbarui sebagian data lampiran permintaan izin
  - `DELETE /api/attendance/absence-attachments/{id}/` - Menghapus lampiran permintaan izin

- **Attendances (Data Kehadiran)**
  - `GET /api/attendance/records/` - Mendapatkan daftar data kehadiran
  - `POST /api/attendance/records/` - Membuat data kehadiran baru
  - `GET /api/attendance/records/{id}/` - Mendapatkan detail data kehadiran
  - `PUT /api/attendance/records/{id}/` - Memperbarui data kehadiran
  - `PATCH /api/attendance/records/{id}/` - Memperbarui sebagian data data kehadiran
  - `DELETE /api/attendance/records/{id}/` - Menghapus data kehadiran

### Izin Peran (Role Permissions)
- `GET /api/role-permissions/` - Mendapatkan daftar izin peran
- `POST /api/role-permissions/` - Membuat izin peran baru
- `GET /api/role-permissions/{id}/` - Mendapatkan detail izin peran
- `PUT /api/role-permissions/{id}/` - Memperbarui izin peran
- `PATCH /api/role-permissions/{id}/` - Memperbarui sebagian data izin peran
- `DELETE /api/role-permissions/{id}/` - Menghapus izin peran

## Cara Menguji API

Berikut adalah beberapa cara untuk menguji API yang tersedia:

### 1. Menggunakan Django REST Framework Web Interface

Django REST Framework menyediakan antarmuka web yang dapat digunakan untuk menguji API secara langsung melalui browser.

1. Jalankan server Django dengan perintah:
   ```
   python manage.py runserver
   ```

2. Buka browser dan akses URL endpoint API, misalnya:
   ```
   http://127.0.0.1:8000/api/users/
   ```

3. Anda akan melihat antarmuka web Django REST Framework yang dapat digunakan untuk menguji API.

### 2. Menggunakan Postman

Postman adalah aplikasi yang sangat berguna untuk menguji API.

1. Unduh dan instal Postman dari [situs resmi Postman](https://www.postman.com/downloads/).

2. Buat request baru dengan metode HTTP yang sesuai (GET, POST, PUT, PATCH, DELETE).

3. Masukkan URL endpoint API, misalnya:
   ```
   http://127.0.0.1:8000/api/users/
   ```

4. Untuk request yang memerlukan autentikasi, tambahkan header Authorization:
   ```
   Authorization: Basic <base64-encoded-credentials>
   ```
   atau gunakan tab "Authorization" dan pilih tipe autentikasi yang sesuai.

5. Untuk request POST, PUT, atau PATCH, tambahkan data dalam format JSON di tab "Body" dan pilih "raw" dan "JSON".

6. Klik tombol "Send" untuk mengirim request.

#### Contoh Request di Postman:

**Registrasi Pengguna Baru:**
```
POST http://127.0.0.1:8000/api/users/register/

Body (JSON):
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123",
    "first_name": "New",
    "last_name": "User",
    "address": "Jl. Contoh No. 123",
    "phone_number": "081234567890"
}
```

**Login Pengguna:**
```
POST http://127.0.0.1:8000/api/users/login/

Body (JSON):
{
    "email": "newuser@example.com",
    "password": "securepassword123"
}
```

**Membuat Tahun Akademik Baru:**
```
POST http://127.0.0.1:8000/api/academic-years/

Body (JSON):
{
    "year_name": "2023/2024",
    "start_date": "2023-07-01",
    "end_date": "2024-06-30",
    "is_active": true
}
```

### 3. Menggunakan curl

curl adalah alat command-line untuk mentransfer data dengan URL syntax.

**Mendapatkan Daftar Pengguna:**
```bash
curl -X GET http://127.0.0.1:8000/api/users/ -H "Authorization: Basic <base64-encoded-credentials>"
```

**Registrasi Pengguna Baru:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","email":"newuser@example.com","password":"securepassword123","first_name":"New","last_name":"User","address":"Jl. Contoh No. 123","phone_number":"081234567890"}'
```

**Login Pengguna:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"newuser@example.com","password":"securepassword123"}'
```

### 4. Menggunakan Python Requests

Python Requests adalah library HTTP untuk Python yang dapat digunakan untuk menguji API.

```python
import requests
import json

# URL base API
base_url = "http://127.0.0.1:8000/api"

# Registrasi pengguna baru
def register_user():
    url = f"{base_url}/users/register/"
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword123",
        "first_name": "New",
        "last_name": "User",
        "address": "Jl. Contoh No. 123",
        "phone_number": "081234567890"
    }
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

# Login pengguna
def login_user():
    url = f"{base_url}/users/login/"
    data = {
        "email": "newuser@example.com",
        "password": "securepassword123"
    }
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# Mendapatkan daftar pengguna (memerlukan autentikasi)
def get_users(auth_token=None):
    url = f"{base_url}/users/"
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Token {auth_token}"
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Response: {response.text}")

# Membuat tahun akademik baru (memerlukan autentikasi)
def create_academic_year(auth_token=None):
    url = f"{base_url}/academic-years/"
    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Token {auth_token}"
    data = {
        "year_name": "2023/2024",
        "start_date": "2023-07-01",
        "end_date": "2024-06-30",
        "is_active": True
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json() if response.status_code < 400 else response.text}")

# Contoh penggunaan
if __name__ == "__main__":
    # Registrasi pengguna baru
    register_user()
    
    # Login pengguna
    login_response = login_user()
    
    # Mendapatkan token autentikasi (jika menggunakan token authentication)
    # auth_token = login_response.get("token")
    
    # Mendapatkan daftar pengguna
    # get_users(auth_token)
    
    # Membuat tahun akademik baru
    # create_academic_year(auth_token)
```

### 5. Menggunakan Automated Testing

Untuk pengujian otomatis, Anda dapat menggunakan file `test_api.py` yang telah dibuat. File ini berisi pengujian untuk berbagai endpoint API menggunakan Django REST Framework's APITestCase.

Untuk menjalankan pengujian, gunakan perintah:

```bash
python manage.py test users.test_api
```

Ini akan menjalankan semua pengujian yang didefinisikan dalam file `test_api.py`.

## Tips Pengujian API

1. **Autentikasi**: Sebagian besar endpoint API memerlukan autentikasi. Pastikan Anda telah login atau menyertakan kredensial autentikasi yang valid dalam request.

2. **Format Data**: Pastikan data yang dikirim dalam format yang benar (biasanya JSON) dan memiliki semua field yang diperlukan.

3. **Status Code**: Perhatikan status code response untuk mengetahui apakah request berhasil atau gagal:
   - 2xx: Sukses (200 OK, 201 Created, 204 No Content)
   - 4xx: Kesalahan klien (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found)
   - 5xx: Kesalahan server

4. **Validasi Data**: Pastikan data yang dikirim memenuhi validasi yang ditentukan dalam serializer.

5. **Pengujian Negatif**: Selain menguji skenario sukses, juga uji skenario gagal untuk memastikan API menangani kesalahan dengan benar.

## Troubleshooting

1. **CSRF Token**: Jika mengalami masalah CSRF token saat menggunakan browser, pastikan Anda telah mendapatkan token CSRF dari server dan menyertakannya dalam header request.

2. **Autentikasi**: Jika mendapatkan error 401 Unauthorized, pastikan Anda telah menyertakan kredensial autentikasi yang benar.

3. **Format Data**: Jika mendapatkan error 400 Bad Request, periksa format dan isi data yang dikirim.

4. **Server Error**: Jika mendapatkan error 500 Internal Server Error, periksa log server untuk informasi lebih lanjut.

5. **CORS**: Jika mengalami masalah CORS saat mengakses API dari domain yang berbeda, pastikan CORS telah dikonfigurasi dengan benar di server.