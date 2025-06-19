-- =================================================================
-- SQL SCRIPT FOR ATTENDANCE MODULE
-- =================================================================
-- Script ini mendefinisikan tabel-tabel yang dibutuhkan untuk
-- fungsionalitas absensi, permintaan izin, dan hari libur sekolah.
-- Ini dirancang untuk terintegrasi dengan modul User yang ada.
--
-- Rekomendasi: Jalankan script ini setelah struktur User sudah ada.
-- Untuk menghindari masalah urutan pembuatan tabel dengan Foreign Key,
-- Anda bisa menggunakan 'SET FOREIGN_KEY_CHECKS = 0;' di awal dan
-- 'SET FOREIGN_KEY_CHECKS = 1;' di akhir.
-- =================================================================

-- -----------------------------------------------------
-- Table: Attendance_Platform
-- Tabel master untuk status absensi (misal: Hadir, Sakit, Izin)
-- dan juga tipe permintaan izin.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Attendance_Platform (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status_code VARCHAR(50) NOT NULL UNIQUE,
    status_name VARCHAR(100) NOT NULL,
    is_agent_approval BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Apakah status ini memerlukan persetujuan?',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table: School_Holidays_Or_Events
-- Tabel untuk menyimpan hari libur atau acara sekolah.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS School_Holidays_Or_Events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    description TEXT,
    event_date_start DATE NOT NULL,
    event_date_end DATE NOT NULL,
    is_school_off BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Apakah pada hari ini sekolah libur?',
    target_audience_type ENUM('Students_Only', 'Teachers_Only', 'All_Users') NOT NULL,
    academic_year_id INT NOT NULL,
    FOREIGN KEY (academic_year_id) REFERENCES Academic_Years(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table: Absence_Requests
-- Tabel untuk mencatat permintaan izin atau sakit dari pengguna.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Absence_Requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requester_user_id INT NOT NULL COMMENT 'User yang mengajukan izin (Siswa/Guru/Staff)',
    absence_type_status_id INT NOT NULL COMMENT 'Jenis izin, FK ke Attendance_Platform (misal: Sakit, Izin, Cuti)',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    approval_status ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending',
    approved_by_user_id INT NULL COMMENT 'User yang menyetujui (atasan/admin)',
    approval_timestamp TIMESTAMP NULL,
    approval_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (requester_user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (approved_by_user_id) REFERENCES Users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (absence_type_status_id) REFERENCES Attendance_Platform(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table: Absence_Requests_Attachments
-- Tabel untuk menyimpan lampiran dari permintaan izin.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Absence_Requests_Attachments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    absence_request_id INT NOT NULL,
    file_url VARCHAR(255) NOT NULL,
    file_name_original VARCHAR(255),
    file_mime_type VARCHAR(100),
    file_size_bytes INT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (absence_request_id) REFERENCES Absence_Requests(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table: Attendances
-- Tabel utama untuk mencatat setiap kehadiran pengguna.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Attendances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_user_id INT NOT NULL COMMENT 'User yang melakukan absensi (Guru/Staff)',
    attendance_date DATE NOT NULL,
    attendance_status_id INT NOT NULL COMMENT 'Status kehadiran, FK ke Attendance_Platform',
    clock_in_time TIME NULL,
    clock_out_time TIME NULL,
    clock_in_latitude DECIMAL(10, 8) NULL,
    clock_in_longitude DECIMAL(11, 8) NULL,
    clock_in_photo_url VARCHAR(255) NULL,
    clock_out_latitude DECIMAL(10, 8) NULL,
    clock_out_longitude DECIMAL(11, 8) NULL,
    clock_out_photo_url VARCHAR(255) NULL,
    notes TEXT,
    attachment_url VARCHAR(255) NULL,
    event_id INT NULL COMMENT 'Jika hari ini adalah event/libur, FK ke School_Holidays_Or_Events',
    recorded_by_user_id INT NULL COMMENT 'User yang mencatat absensi ini jika dilakukan manual oleh admin',
    absence_request_id INT NULL COMMENT 'Jika absensi ini terkait dengan permintaan izin, FK ke Absence_Requests',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (employee_user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (attendance_status_id) REFERENCES Attendance_Platform(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (recorded_by_user_id) REFERENCES Users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES School_Holidays_Or_Events(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (absence_request_id) REFERENCES Absence_Requests(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;