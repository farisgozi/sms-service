-- Pastikan untuk membuat database terlebih dahulu jika belum ada
-- CREATE DATABASE IF NOT EXISTS nama_database_anda;
-- USE nama_database_anda;

-- Matikan cek Foreign Key untuk sementara, ini berguna jika ada masalah sirkular dependensi
-- SET FOREIGN_KEY_CHECKS = 0;

-- -----------------------------------------------------
-- Table: Academic_Years
-- Tahun Akademik (misal: 2023/2024)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Academic_Years (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year_name VARCHAR(100) NOT NULL UNIQUE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Positions
-- Jabatan atau posisi dalam institusi
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Positions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    position_name VARCHAR(255) NOT NULL UNIQUE,
    position_code VARCHAR(50),
    description TEXT,
    position_type ENUM('Akademik', 'Non-Akademik', 'Manajerial', 'Pendukung') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Majors
-- Jurusan atau konsentrasi
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Majors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    major_name VARCHAR(255) NOT NULL UNIQUE,
    major_code VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Subjects
-- Mata Pelajaran
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(255) NOT NULL UNIQUE,
    subject_code VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Roles
-- Peran pengguna (misal: Admin, Guru, Siswa, Staff)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Permissions
-- Izin atau hak akses spesifik
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    permission_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Groups
-- Kelompok pengguna (misal: Komite Sekolah, OSIS)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Users
-- Tabel utama pengguna dengan informasi dasar
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- Simpan hash password, bukan plain text
    email VARCHAR(255) NOT NULL UNIQUE,
    address TEXT,
    phone_number VARCHAR(50),
    profile_picture VARCHAR(255), -- Path atau URL ke gambar profil
    role_id INT NOT NULL,
    status ENUM('active', 'inactive', 'suspended') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Staff_Details
-- Detail khusus untuk staff non-pengajar
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Staff_Details (
    user_id INT PRIMARY KEY,
    nip VARCHAR(100) UNIQUE, -- Nomor Induk Pegawai
    position_id INT,
    department VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (position_id) REFERENCES Positions(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Teacher_Details
-- Detail khusus untuk guru/pengajar
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Teacher_Details (
    user_id INT PRIMARY KEY,
    nip VARCHAR(100) UNIQUE, -- Nomor Induk Pegawai
    position_id INT,
    major_id INT, -- Jurusan yang diajar
    is_principal BOOLEAN NOT NULL DEFAULT FALSE, -- Apakah guru ini kepala sekolah?
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (position_id) REFERENCES Positions(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (major_id) REFERENCES Majors(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Classes
-- Kelas atau rombongan belajar
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    grade_level INT NOT NULL,
    academic_year_id INT NOT NULL,
    homeroom_teacher_user_id INT, -- User ID guru wali kelas (FK ke Teacher_Details)
    major_id INT,
    FOREIGN KEY (academic_year_id) REFERENCES Academic_Years(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (homeroom_teacher_user_id) REFERENCES Teacher_Details(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (major_id) REFERENCES Majors(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Student_Details
-- Detail khusus untuk siswa
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Student_Details (
    user_id INT PRIMARY KEY,
    nisn VARCHAR(100) UNIQUE, -- Nomor Induk Siswa Nasional
    class_id INT,
    major_id INT,
    entry_year YEAR, -- Tahun masuk
    parent_guardian_name VARCHAR(255),
    parent_guardian_phone VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Classes(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (major_id) REFERENCES Majors(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Teacher_Subjects
-- Tabel relasi Many-to-Many antara Guru dan Mata Pelajaran di Kelas tertentu pada Tahun Akademik tertentu
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Teacher_Subjects (
    teacher_user_id INT NOT NULL,
    subject_id INT NOT NULL,
    class_id INT NOT NULL,
    academic_year_id INT NOT NULL,
    PRIMARY KEY (teacher_user_id, subject_id, class_id, academic_year_id),
    FOREIGN KEY (teacher_user_id) REFERENCES Teacher_Details(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subjects(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Classes(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (academic_year_id) REFERENCES Academic_Years(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: User_Group_Membership
-- Tabel relasi Many-to-Many antara User dan Group
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS User_Group_Membership (
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (group_id) REFERENCES Groups(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table: Role_Permissions
-- Tabel relasi Many-to-Many antara Role dan Permission
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Role_Permissions (
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES Permissions(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Aktifkan kembali cek Foreign Key
-- SET FOREIGN_KEY_CHECKS = 1;