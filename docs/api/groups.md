# API Grup

Endpoint untuk manajemen grup pengguna dalam sistem.

## Endpoint

### Daftar Grup

```http
GET /api/groups/
```

Mendapatkan daftar semua grup dalam sistem.

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
    "message": "Daftar grup berhasil diambil",
    "data": {
        "count": "integer",
        "next": "string|null",
        "previous": "string|null",
        "results": [
            {
                "id": "integer",
                "name": "string",
                "description": "string",
                "member_count": "integer"
            }
        ]
    }
}
```

### Detail Grup

```http
GET /api/groups/{id}/
```

Mendapatkan detail informasi grup berdasarkan ID.

#### Response

```json
{
    "status": "success",
    "message": "Detail grup berhasil diambil",
    "data": {
        "id": "integer",
        "name": "string",
        "description": "string",
        "members": [
            {
                "id": "integer",
                "username": "string",
                "email": "string",
                "full_name": "string"
            }
        ],
        "created_at": "datetime",
        "updated_at": "datetime"
    }
}
```

### Membuat Grup

```http
POST /api/groups/
```

Membuat grup baru dalam sistem.

#### Request Body

```json
{
    "name": "string",
    "description": "string"
}
```

### Memperbarui Grup

```http
PUT /api/groups/{id}/
PATCH /api/groups/{id}/
```

Memperbarui data grup yang ada.

#### Request Body

```json
{
    "name": "string",
    "description": "string"
}
```

### Menghapus Grup

```http
DELETE /api/groups/{id}/
```

## Keanggotaan Grup

### Daftar Keanggotaan

```http
GET /api/user-group-memberships/
```

Mendapatkan daftar keanggotaan grup.

#### Response

```json
{
    "status": "success",
    "message": "Daftar keanggotaan grup berhasil diambil",
    "data": [
        {
            "id": "integer",
            "user": {
                "id": "integer",
                "username": "string",
                "email": "string"
            },
            "group": {
                "id": "integer",
                "name": "string"
            },
            "joined_at": "datetime"
        }
    ]
}
```

### Menambah Anggota ke Grup

```http
POST /api/user-group-memberships/
```

Menambahkan pengguna ke dalam grup.

#### Request Body

```json
{
    "user_id": "integer",
    "group_id": "integer"
}
```

### Menghapus Anggota dari Grup

```http
DELETE /api/user-group-memberships/{id}/
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
    "message": "Grup tidak ditemukan",
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

### Duplicate Entry

```json
{
    "status": "error",
    "message": "Pengguna sudah menjadi anggota grup ini",
    "data": null
}
```