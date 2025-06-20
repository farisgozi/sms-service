# API Peran dan Izin

Endpoint untuk manajemen peran (roles) dan izin (permissions) dalam sistem.

## Peran (Roles)

### Daftar Peran

```http
GET /api/roles/
```

Mendapatkan daftar semua peran dalam sistem.

#### Headers

```
Authorization: Token <token>
```

#### Response

```json
{
    "status": "success",
    "message": "Daftar peran berhasil diambil",
    "data": [
        {
            "id": "integer",
            "name": "string",
            "description": "string",
            "permissions": [
                {
                    "id": "integer",
                    "name": "string",
                    "codename": "string"
                }
            ]
        }
    ]
}
```

### Detail Peran

```http
GET /api/roles/{id}/
```

Mendapatkan detail informasi peran berdasarkan ID.

#### Response

```json
{
    "status": "success",
    "message": "Detail peran berhasil diambil",
    "data": {
        "id": "integer",
        "name": "string",
        "description": "string",
        "permissions": [
            {
                "id": "integer",
                "name": "string",
                "codename": "string"
            }
        ],
        "created_at": "datetime",
        "updated_at": "datetime"
    }
}
```

### Membuat Peran

```http
POST /api/roles/
```

Membuat peran baru dalam sistem.

#### Request Body

```json
{
    "name": "string",
    "description": "string",
    "permissions": ["integer"]
}
```

### Memperbarui Peran

```http
PUT /api/roles/{id}/
PATCH /api/roles/{id}/
```

Memperbarui data peran yang ada.

#### Request Body

```json
{
    "name": "string",
    "description": "string",
    "permissions": ["integer"]
}
```

### Menghapus Peran

```http
DELETE /api/roles/{id}/
```

## Izin (Permissions)

### Daftar Izin

```http
GET /api/permissions/
```

Mendapatkan daftar semua izin dalam sistem.

#### Response

```json
{
    "status": "success",
    "message": "Daftar izin berhasil diambil",
    "data": [
        {
            "id": "integer",
            "name": "string",
            "codename": "string",
            "description": "string"
        }
    ]
}
```

### Detail Izin

```http
GET /api/permissions/{id}/
```

Mendapatkan detail informasi izin berdasarkan ID.

#### Response

```json
{
    "status": "success",
    "message": "Detail izin berhasil diambil",
    "data": {
        "id": "integer",
        "name": "string",
        "codename": "string",
        "description": "string",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
}
```

### Membuat Izin

```http
POST /api/permissions/
```

Membuat izin baru dalam sistem.

#### Request Body

```json
{
    "name": "string",
    "codename": "string",
    "description": "string"
}
```

### Memperbarui Izin

```http
PUT /api/permissions/{id}/
PATCH /api/permissions/{id}/
```

Memperbarui data izin yang ada.

#### Request Body

```json
{
    "name": "string",
    "codename": "string",
    "description": "string"
}
```

### Menghapus Izin

```http
DELETE /api/permissions/{id}/
```

## Izin Peran (Role Permissions)

### Daftar Izin Peran

```http
GET /api/role-permissions/
```

Mendapatkan daftar relasi antara peran dan izin.

#### Response

```json
{
    "status": "success",
    "message": "Daftar izin peran berhasil diambil",
    "data": [
        {
            "id": "integer",
            "role": {
                "id": "integer",
                "name": "string"
            },
            "permission": {
                "id": "integer",
                "name": "string",
                "codename": "string"
            }
        }
    ]
}
```

### Menambah Izin ke Peran

```http
POST /api/role-permissions/
```

Menambahkan izin ke peran tertentu.

#### Request Body

```json
{
    "role_id": "integer",
    "permission_id": "integer"
}
```

### Menghapus Izin dari Peran

```http
DELETE /api/role-permissions/{id}/
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