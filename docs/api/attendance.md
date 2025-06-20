# API Kehadiran

Endpoint untuk manajemen kehadiran siswa, termasuk platform kehadiran, hari libur/acara sekolah, dan permintaan ketidakhadiran.

## Platform Kehadiran

### Daftar Platform

```http
GET /api/users/attendance-platforms/
```

Mendapatkan daftar platform kehadiran yang tersedia.

#### Headers

```
Authorization: Token <token>
```

#### Response

```json
{
    "status": "success",
    "message": "Daftar platform kehadiran berhasil diambil",
    "data": [
        {
            "id": "integer",
            "name": "string",
            "description": "string",
            "is_active": "boolean"
        }
    ]
}
```

### Detail Platform

```http
GET /api/users/attendance-platforms/{id}/
```

### Membuat Platform

```http
POST /api/users/attendance-platforms/
```

#### Request Body

```json
{
    "name": "string",
    "description": "string",
    "is_active": "boolean"
}
```

### Memperbarui Platform

```http
PUT /api/users/attendance-platforms/{id}/
PATCH /api/users/attendance-platforms/{id}/
```

### Menghapus Platform

```http
DELETE /api/users/attendance-platforms/{id}/
```

## Hari Libur/Acara Sekolah

### Daftar Hari Libur/Acara

```http
GET /api/users/school-holidays/
```

Mendapatkan daftar hari libur dan acara sekolah.

#### Response

```json
{
    "status": "success",
    "message": "Daftar hari libur/acara berhasil diambil",
    "data": [
        {
            "id": "integer",
            "title": "string",
            "description": "string",
            "start_date": "date",
            "end_date": "date",
            "type": "string"
        }
    ]
}
```

### Detail Hari Libur/Acara

```http
GET /api/users/school-holidays/{id}/
```

### Membuat Hari Libur/Acara

```http
POST /api/users/school-holidays/
```

#### Request Body

```json
{
    "title": "string",
    "description": "string",
    "start_date": "date",
    "end_date": "date",
    "type": "string"
}
```

### Memperbarui Hari Libur/Acara

```http
PUT /api/users/school-holidays/{id}/
PATCH /api/users/school-holidays/{id}/
```

### Menghapus Hari Libur/Acara

```http
DELETE /api/users/school-holidays/{id}/
```

## Permintaan Ketidakhadiran

### Daftar Permintaan

```http
GET /api/users/absence-requests/
```

Mendapatkan daftar permintaan ketidakhadiran.

#### Response

```json
{
    "status": "success",
    "message": "Daftar permintaan ketidakhadiran berhasil diambil",
    "data": [
        {
            "id": "integer",
            "student": {
                "id": "integer",
                "user": {
                    "full_name": "string"
                }
            },
            "type": "string",
            "reason": "string",
            "start_date": "date",
            "end_date": "date",
            "status": "string",
            "attachments": [
                {
                    "id": "integer",
                    "file_url": "string",
                    "file_type": "string"
                }
            ]
        }
    ]
}
```

### Detail Permintaan

```http
GET /api/users/absence-requests/{id}/
```

### Membuat Permintaan

```http
POST /api/users/absence-requests/
```

#### Request Body

```json
{
    "student_id": "integer",
    "type": "string",
    "reason": "string",
    "start_date": "date",
    "end_date": "date"
}
```

### Memperbarui Permintaan

```http
PUT /api/users/absence-requests/{id}/
PATCH /api/users/absence-requests/{id}/
```

### Menghapus Permintaan

```http
DELETE /api/users/absence-requests/{id}/
```

### Mengunggah Lampiran

```http
POST /api/users/absence-requests/{id}/attachments/
```

#### Request Body (multipart/form-data)

```
file: File
```

### Menghapus Lampiran

```http
DELETE /api/users/absence-requests/{id}/attachments/{attachment_id}/
```

## Kehadiran

### Daftar Kehadiran

```http
GET /api/users/attendances/
```

Mendapatkan daftar kehadiran.

#### Query Parameters

| Parameter    | Tipe    | Deskripsi |
|--------------|---------|------------|
| date         | date    | Tanggal kehadiran |
| student_id   | integer | ID siswa |
| class_id     | integer | ID kelas |

#### Response

```json
{
    "status": "success",
    "message": "Daftar kehadiran berhasil diambil",
    "data": [
        {
            "id": "integer",
            "student": {
                "id": "integer",
                "user": {
                    "full_name": "string"
                }
            },
            "date": "date",
            "status": "string",
            "platform": {
                "id": "integer",
                "name": "string"
            },
            "notes": "string"
        }
    ]
}
```

### Detail Kehadiran

```http
GET /api/users/attendances/{id}/
```

### Mencatat Kehadiran

```http
POST /api/users/attendances/
```

#### Request Body

```json
{
    "student_id": "integer",
    "date": "date",
    "status": "string",
    "platform_id": "integer",
    "notes": "string"
}
```

### Memperbarui Kehadiran

```http
PUT /api/users/attendances/{id}/
PATCH /api/users/attendances/{id}/
```

### Menghapus Kehadiran

```http
DELETE /api/users/attendances/{id}/
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