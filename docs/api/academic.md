# API Akademik

Endpoint untuk manajemen data akademik seperti tahun akademik, jurusan, dan mata pelajaran.

## Tahun Akademik

### Daftar Tahun Akademik

```http
GET /api/academic-years/
```

Mendapatkan daftar tahun akademik.

#### Response

```json
{
    "status": "success",
    "message": "Daftar tahun akademik berhasil diambil",
    "data": [
        {
            "id": "integer",
            "year_name": "string",
            "start_date": "date",
            "end_date": "date",
            "is_active": "boolean"
        }
    ]
}
```

### Detail Tahun Akademik

```http
GET /api/academic-years/{id}/
```

### Membuat Tahun Akademik

```http
POST /api/academic-years/
```

#### Request Body

```json
{
    "year_name": "string",
    "start_date": "date",
    "end_date": "date",
    "is_active": "boolean"
}
```

### Memperbarui Tahun Akademik

```http
PUT /api/academic-years/{id}/
PATCH /api/academic-years/{id}/
```

### Menghapus Tahun Akademik

```http
DELETE /api/academic-years/{id}/
```

## Jurusan

### Daftar Jurusan

```http
GET /api/majors/
```

Mendapatkan daftar jurusan.

#### Response

```json
{
    "status": "success",
    "message": "Daftar jurusan berhasil diambil",
    "data": [
        {
            "id": "integer",
            "name": "string",
            "code": "string",
            "description": "string"
        }
    ]
}
```

### Detail Jurusan

```http
GET /api/majors/{id}/
```

### Membuat Jurusan

```http
POST /api/majors/
```

#### Request Body

```json
{
    "name": "string",
    "code": "string",
    "description": "string"
}
```

### Memperbarui Jurusan

```http
PUT /api/majors/{id}/
PATCH /api/majors/{id}/
```

### Menghapus Jurusan

```http
DELETE /api/majors/{id}/
```

## Mata Pelajaran

### Daftar Mata Pelajaran

```http
GET /api/subjects/
```

Mendapatkan daftar mata pelajaran.

#### Response

```json
{
    "status": "success",
    "message": "Daftar mata pelajaran berhasil diambil",
    "data": [
        {
            "id": "integer",
            "name": "string",
            "code": "string",
            "description": "string",
            "major": {
                "id": "integer",
                "name": "string"
            }
        }
    ]
}
```

### Detail Mata Pelajaran

```http
GET /api/subjects/{id}/
```

### Membuat Mata Pelajaran

```http
POST /api/subjects/
```

#### Request Body

```json
{
    "name": "string",
    "code": "string",
    "description": "string",
    "major_id": "integer"
}
```

### Memperbarui Mata Pelajaran

```http
PUT /api/subjects/{id}/
PATCH /api/subjects/{id}/
```

### Menghapus Mata Pelajaran

```http
DELETE /api/subjects/{id}/
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