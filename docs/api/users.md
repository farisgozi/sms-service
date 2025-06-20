# API Pengguna

Endpoint untuk manajemen data pengguna dalam sistem.

## Endpoint

### Daftar Pengguna

```http
GET /api/users/
```

Mendapatkan daftar semua pengguna dalam sistem.

#### Headers

```
Authorization: Token <token>
```

#### Query Parameters

| Parameter | Tipe    | Deskripsi |
|-----------|---------|------------|
| page      | integer | Nomor halaman |
| limit     | integer | Jumlah data per halaman |
| search    | string  | Kata kunci pencarian |

#### Response

```json
{
    "status": "success",
    "message": "Daftar pengguna berhasil diambil",
    "data": {
        "count": "integer",
        "next": "string|null",
        "previous": "string|null",
        "results": [
            {
                "id": "integer",
                "username": "string",
                "email": "string",
                "first_name": "string",
                "last_name": "string",
                "address": "string",
                "phone_number": "string",
                "is_active": "boolean",
                "date_joined": "datetime"
            }
        ]
    }
}
```

### Detail Pengguna

```http
GET /api/users/{id}/
```

Mendapatkan detail informasi pengguna berdasarkan ID.

#### Headers

```
Authorization: Token <token>
```

#### Response

```json
{
    "status": "success",
    "message": "Detail pengguna berhasil diambil",
    "data": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "address": "string",
        "phone_number": "string",
        "is_active": "boolean",
        "date_joined": "datetime",
        "groups": [
            {
                "id": "integer",
                "name": "string"
            }
        ],
        "roles": [
            {
                "id": "integer",
                "name": "string"
            }
        ]
    }
}
```

### Membuat Pengguna

```http
POST /api/users/
```

Membuat pengguna baru dalam sistem.

#### Headers

```
Authorization: Token <token>
Content-Type: application/json
```

#### Request Body

```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string",
    "address": "string",
    "phone_number": "string",
    "is_active": "boolean",
    "groups": ["integer"],
    "roles": ["integer"]
}
```

#### Response

```json
{
    "status": "success",
    "message": "Pengguna berhasil dibuat",
    "data": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "address": "string",
        "phone_number": "string",
        "is_active": "boolean",
        "date_joined": "datetime"
    }
}
```

### Memperbarui Pengguna

```http
PUT /api/users/{id}/
```

Memperbarui seluruh data pengguna.

#### Headers

```
Authorization: Token <token>
Content-Type: application/json
```

#### Request Body

```json
{
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "address": "string",
    "phone_number": "string",
    "is_active": "boolean",
    "groups": ["integer"],
    "roles": ["integer"]
}
```

### Memperbarui Sebagian Data Pengguna

```http
PATCH /api/users/{id}/
```

Memperbarui sebagian data pengguna.

#### Headers

```
Authorization: Token <token>
Content-Type: application/json
```

#### Request Body

```json
{
    "field_yang_diubah": "nilai_baru"
}
```

### Menghapus Pengguna

```http
DELETE /api/users/{id}/
```

Menghapus data pengguna dari sistem.

#### Headers

```
Authorization: Token <token>
```

#### Response

```json
{
    "status": "success",
    "message": "Pengguna berhasil dihapus",
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
    "message": "Pengguna tidak ditemukan",
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