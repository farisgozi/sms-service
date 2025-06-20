# API Siswa dan Kelas

Endpoint untuk manajemen data siswa dan kelas dalam sistem.

## Detail Siswa

### Daftar Detail Siswa

```http
GET /api/student-details/
```

Mendapatkan daftar detail siswa.

#### Headers

```
Authorization: Token <token>
```

#### Response

```json
{
    "status": "success",
    "message": "Daftar detail siswa berhasil diambil",
    "data": [
        {
            "id": "integer",
            "user": {
                "id": "integer",
                "username": "string",
                "email": "string",
                "full_name": "string"
            },
            "nis": "string",
            "nisn": "string",
            "major": {
                "id": "integer",
                "name": "string"
            },
            "entry_year": "integer",
            "status": "string"
        }
    ]
}
```

### Detail Siswa Spesifik

```http
GET /api/student-details/{id}/
```

### Membuat Detail Siswa

```http
POST /api/student-details/
```

#### Request Body

```json
{
    "user_id": "integer",
    "nis": "string",
    "nisn": "string",
    "major_id": "integer",
    "entry_year": "integer",
    "status": "string"
}
```

### Memperbarui Detail Siswa

```http
PUT /api/student-details/{id}/
PATCH /api/student-details/{id}/
```

### Menghapus Detail Siswa

```http
DELETE /api/student-details/{id}/
```

## Kelas

### Daftar Kelas

```http
GET /api/classes/
```

Mendapatkan daftar kelas.

#### Response

```json
{
    "status": "success",
    "message": "Daftar kelas berhasil diambil",
    "data": [
        {
            "id": "integer",
            "name": "string",
            "grade": "integer",
            "major": {
                "id": "integer",
                "name": "string"
            },
            "academic_year": {
                "id": "integer",
                "year_name": "string"
            },
            "homeroom_teacher": {
                "id": "integer",
                "user": {
                    "full_name": "string"
                }
            },
            "student_count": "integer"
        }
    ]
}
```

### Detail Kelas

```http
GET /api/classes/{id}/
```

### Membuat Kelas

```http
POST /api/classes/
```

#### Request Body

```json
{
    "name": "string",
    "grade": "integer",
    "major_id": "integer",
    "academic_year_id": "integer",
    "homeroom_teacher_id": "integer"
}
```

### Memperbarui Kelas

```http
PUT /api/classes/{id}/
PATCH /api/classes/{id}/
```

### Menghapus Kelas

```http
DELETE /api/classes/{id}/
```

## Keanggotaan Kelas

### Daftar Siswa dalam Kelas

```http
GET /api/classes/{id}/students/
```

Mendapatkan daftar siswa yang terdaftar dalam kelas tertentu.

#### Response

```json
{
    "status": "success",
    "message": "Daftar siswa dalam kelas berhasil diambil",
    "data": [
        {
            "id": "integer",
            "user": {
                "id": "integer",
                "username": "string",
                "full_name": "string"
            },
            "nis": "string",
            "nisn": "string"
        }
    ]
}
```

### Menambah Siswa ke Kelas

```http
POST /api/classes/{id}/students/
```

#### Request Body

```json
{
    "student_ids": ["integer"]
}
```

### Menghapus Siswa dari Kelas

```http
DELETE /api/classes/{id}/students/{student_id}/
```

## Error Response

### Unauthorized

```json
{
    "status": "error",
    "message": "Token tidak valid atau telah kadaluarsa",
    "data": null
}
```

### Not Found

```json
{
    "status": "error",
    "message": "Data tidak ditemukan",
    "data": null
}
```

### Validation Error

```json
{
    "status": "error",
    "message": "Validasi gagal",
    "data": {
        "field": [
            "Pesan error validasi"
        ]
    }
}
```