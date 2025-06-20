# API Staf dan Guru

Endpoint untuk manajemen data staf dan guru dalam sistem.

## Detail Staf

### Daftar Detail Staf

```http
GET /api/staff-details/
```

Mendapatkan daftar detail staf.

#### Headers

```
Authorization: Token <token>
```

#### Response

```json
{
    "status": "success",
    "message": "Daftar detail staf berhasil diambil",
    "data": [
        {
            "id": "integer",
            "user": {
                "id": "integer",
                "username": "string",
                "email": "string",
                "full_name": "string"
            },
            "nip": "string",
            "position": {
                "id": "integer",
                "name": "string"
            },
            "join_date": "date",
            "status": "string"
        }
    ]
}
```

### Detail Staf Spesifik

```http
GET /api/staff-details/{id}/
```

### Membuat Detail Staf

```http
POST /api/staff-details/
```

#### Request Body

```json
{
    "user_id": "integer",
    "nip": "string",
    "position_id": "integer",
    "join_date": "date",
    "status": "string"
}
```

### Memperbarui Detail Staf

```http
PUT /api/staff-details/{id}/
PATCH /api/staff-details/{id}/
```

### Menghapus Detail Staf

```http
DELETE /api/staff-details/{id}/
```

## Detail Guru

### Daftar Detail Guru

```http
GET /api/teacher-details/
```

Mendapatkan daftar detail guru.

#### Response

```json
{
    "status": "success",
    "message": "Daftar detail guru berhasil diambil",
    "data": [
        {
            "id": "integer",
            "user": {
                "id": "integer",
                "username": "string",
                "email": "string",
                "full_name": "string"
            },
            "nip": "string",
            "specialization": "string",
            "join_date": "date",
            "status": "string"
        }
    ]
}
```

### Detail Guru Spesifik

```http
GET /api/teacher-details/{id}/
```

### Membuat Detail Guru

```http
POST /api/teacher-details/
```

#### Request Body

```json
{
    "user_id": "integer",
    "nip": "string",
    "specialization": "string",
    "join_date": "date",
    "status": "string"
}
```

### Memperbarui Detail Guru

```http
PUT /api/teacher-details/{id}/
PATCH /api/teacher-details/{id}/
```

### Menghapus Detail Guru

```http
DELETE /api/teacher-details/{id}/
```

## Guru Mata Pelajaran

### Daftar Guru Mata Pelajaran

```http
GET /api/teacher-subjects/
```

Mendapatkan daftar relasi guru dengan mata pelajaran yang diajar.

#### Response

```json
{
    "status": "success",
    "message": "Daftar guru mata pelajaran berhasil diambil",
    "data": [
        {
            "id": "integer",
            "teacher": {
                "id": "integer",
                "user": {
                    "full_name": "string"
                }
            },
            "subject": {
                "id": "integer",
                "name": "string",
                "code": "string"
            },
            "academic_year": {
                "id": "integer",
                "year_name": "string"
            }
        }
    ]
}
```

### Detail Guru Mata Pelajaran

```http
GET /api/teacher-subjects/{id}/
```

### Menambah Guru Mata Pelajaran

```http
POST /api/teacher-subjects/
```

#### Request Body

```json
{
    "teacher_id": "integer",
    "subject_id": "integer",
    "academic_year_id": "integer"
}
```

### Memperbarui Guru Mata Pelajaran

```http
PUT /api/teacher-subjects/{id}/
PATCH /api/teacher-subjects/{id}/
```

### Menghapus Guru Mata Pelajaran

```http
DELETE /api/teacher-subjects/{id}/
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