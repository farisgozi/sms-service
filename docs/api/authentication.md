# API Autentikasi

Endpoint untuk manajemen autentikasi pengguna dalam sistem.

## Endpoint

### Register

```http
POST /api/users/register/
```

Mendaftarkan pengguna baru ke dalam sistem.

#### Request Body

```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string",
    "address": "string",
    "phone_number": "string"
}
```

#### Response

```json
{
    "status": "success",
    "message": "Registrasi berhasil",
    "data": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "address": "string",
        "phone_number": "string"
    }
}
```

### Login

```http
POST /api/users/login/
```

Melakukan autentikasi pengguna dan mendapatkan token akses.

#### Request Body

```json
{
    "email": "string",
    "password": "string"
}
```

#### Response

```json
{
    "status": "success",
    "message": "Login berhasil",
    "data": {
        "token": "string",
        "user": {
            "id": "integer",
            "username": "string",
            "email": "string"
        }
    }
}
```

### Cek Autentikasi

```http
GET /api/auth/
```

Memeriksa status autentikasi pengguna saat ini.

#### Headers

```
Authorization: Token <token>
```

#### Response

```json
{
    "status": "success",
    "message": "Token valid",
    "data": {
        "user": {
            "id": "integer",
            "username": "string",
            "email": "string"
        }
    }
}
```

## Error Response

### Invalid Credentials

```json
{
    "status": "error",
    "message": "Email atau password salah",
    "data": null
}
```

### Invalid Token

```json
{
    "status": "error",
    "message": "Token tidak valid atau telah kadaluarsa",
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