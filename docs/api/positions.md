# API Posisi

Endpoint untuk manajemen data posisi dalam sistem.

## Daftar Posisi

```http
GET /api/positions/
```

Mendapatkan daftar semua posisi dalam sistem.

### Headers

```
Authorization: Token <token>
```

### Response

```json
{
    "status": "success",
    "message": "Daftar posisi berhasil diambil",
    "data": [
        {
            "id": "integer",
            "name": "string",
            "code": "string",
            "description": "string",
            "is_active": "boolean"
        }
    ]
}
```

## Detail Posisi

```http
GET /api/positions/{id}/
```

Mendapatkan detail informasi posisi berdasarkan ID.

### Response

```json
{
    "status": "success",
    "message": "Detail posisi berhasil diambil",
    "data": {
        "id": "integer",
        "name": "string",
        "code": "string",
        "description": "string",
        "is_active": "boolean",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
}
```

## Membuat Posisi

```http
POST /api/positions/
```

Membuat posisi baru dalam sistem.

### Request Body

```json
{
    "name": "string",
    "code": "string",
    "description": "string",
    "is_active": "boolean"
}
```

### Response Success

```json
{
    "status": "success",
    "message": "Posisi berhasil dibuat",
    "data": {
        "id": "integer",
        "name": "string",
        "code": "string",
        "description": "string",
        "is_active": "boolean"
    }
}
```

## Memperbarui Posisi

```http
PUT /api/positions/{id}/
PATCH /api/positions/{id}/
```

Memperbarui data posisi yang ada.

### Request Body

```json
{
    "name": "string",
    "code": "string",
    "description": "string",
    "is_active": "boolean"
}
```

### Response Success

```json
{
    "status": "success",
    "message": "Posisi berhasil diperbarui",
    "data": {
        "id": "integer",
        "name": "string",
        "code": "string",
        "description": "string",
        "is_active": "boolean"
    }
}
```

## Menghapus Posisi

```http
DELETE /api/positions/{id}/
```

Menghapus posisi dari sistem.

### Response Success

```json
{
    "status": "success",
    "message": "Posisi berhasil dihapus",
    "data": null
}
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
    "message": "Posisi tidak ditemukan",
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

### Conflict

```json
{
    "status": "error",
    "message": "Kode posisi sudah digunakan",
    "data": null
}
```