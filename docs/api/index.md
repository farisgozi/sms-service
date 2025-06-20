# Dokumentasi API Sistem Manajemen Sekolah

Selamat datang di dokumentasi API Sistem Manajemen Sekolah (SMS). Dokumentasi ini berisi informasi lengkap tentang endpoint API yang tersedia dalam sistem.

## Kategori API

1. [Autentikasi](./authentication.md)
2. [Pengguna](./users.md)
3. [Peran dan Izin](./roles-permissions.md)
4. [Grup](./groups.md)
5. [Akademik](./academic.md)
6. [Staf dan Guru](./staff-teachers.md)
7. [Siswa](./students.md)
8. [Kelas](./classes.md)
9. [Kehadiran](./attendance.md)

## Format Response

Semua response API menggunakan format JSON dengan struktur berikut:

```json
{
    "status": "success",
    "message": "Pesan sukses atau error",
    "data": {}
}
```

## Autentikasi

Sebagian besar endpoint API memerlukan autentikasi. Untuk mengakses endpoint yang memerlukan autentikasi, sertakan token dalam header request:

```
Authorization: Token <your-token-here>
```

## Status Kode

- 200: Sukses
- 201: Berhasil membuat data baru
- 204: Berhasil menghapus data
- 400: Bad Request - request tidak valid
- 401: Unauthorized - token tidak valid atau expired
- 403: Forbidden - tidak memiliki izin
- 404: Not Found - data tidak ditemukan
- 500: Internal Server Error