import requests
import json
import os
import time
import random
import concurrent.futures
import threading

# ==============================================================================
# KONFIGURASI BENCHMARK
# Ubah parameter ini untuk mensimulasikan beban yang berbeda
# ==============================================================================
# URL base API Anda (Ganti dengan URL hosting Anda untuk pengujian realistis)
BASE_URL = "http://api-sms.hexanest.id/api"

# Kredensial untuk login
USER_EMAIL = "hexanest@gmail.com"
USER_PASSWORD = "hexanestdotaidi"

# Parameter Load Testing
NUM_USERS = 150  # Jumlah pengguna simultan (concurrent users)
DURATION_SECONDS = 30  # Durasi benchmark dalam detik
REQUEST_MIX = {
    "get_subjects": 0.10,
    "get_majors": 0.10,
    "register_user": 0.05, # Kurangi frekuensi register karena lebih berat
    # Attendance Module Mix
    "get_attendance_platforms": 0.20,
    "create_attendance_platform": 0.10,
    "get_school_holidays_or_events": 0.15,
    # "create_school_holiday_or_event": 0.05, # Membutuhkan academic_year_id
    "get_absence_requests": 0.15,
    # "create_absence_request": 0.05, # Membutuhkan user_id & platform_id
    "get_attendances": 0.10,
    # "create_attendance_record": 0.05, # Membutuhkan user_id & platform_id
}

# Tambahkan fungsi create yang memerlukan ID ke API_ACTIONS jika ingin diuji dalam load test
# Pastikan variabel global seperti DEFAULT_ACADEMIC_YEAR_ID, DEFAULT_ATTENDANCE_PLATFORM_ID, DEFAULT_USER_ID_FOR_ATTENDANCE
# sudah diinisialisasi dengan benar sebelum benchmark dimulai (misalnya di setup_initial_data_for_attendance)

# Contoh jika ingin memasukkan create_school_holiday_or_event ke dalam benchmark:
# API_ACTIONS["create_school_holiday_or_event"] = create_school_holiday_or_event
# REQUEST_MIX["create_school_holiday_or_event"] = 0.05 # Sesuaikan bobotnya
# Pastikan worker_task meneruskan academic_year_id=DEFAULT_ACADEMIC_YEAR_ID saat memanggilnya.

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

COLORS = {
    'HEADER': '\033[95m', 'BLUE': '\033[94m', 'GREEN': '	\u001b[32m',
    'WARNING': '\033[93m', 'FAIL': '\033[91m', 'ENDC': '\033[0m', 'BOLD': '\033[1m'
}

def print_colored(text, color):
    """Mencetak teks dengan warna."""
    print(f"{COLORS.get(color, '')}{text}{COLORS['ENDC']}")

def login_user():
    """Login pengguna dan mengembalikan token otentikasi."""
    print_colored("\n[AUTH] Melakukan Login Pengguna...", 'HEADER')
    url = f"{BASE_URL}/users/login/"
    data = {"email": USER_EMAIL, "password": USER_PASSWORD}
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            return response.json().get('token')
        print_colored(f"Login Gagal! Status: {response.status_code}", "FAIL")
        return None
    except requests.exceptions.RequestException as e:
        print_colored(f"Koneksi ke {url} gagal: {e}", "FAIL")
        return None

def get_auth_headers(token):
    """Membuat header otentikasi."""
    return {'Authorization': f'Token {token}'}

# ==============================================================================
# FUNGSI API UNTUK BENCHMARK (USERS)
# ==============================================================================

# Fungsi yang akan diuji di bawah beban
def get_subjects(session, headers, **kwargs):
    return session.get(f"{BASE_URL}/subjects/", headers=headers, timeout=10)

def get_majors(session, headers, **kwargs):
    return session.get(f"{BASE_URL}/majors/", headers=headers, timeout=10)

def register_user(session, headers, created_user_ids, lock):
    """Mendaftarkan pengguna baru dengan data unik."""
    # Hasilkan data unik untuk setiap pendaftaran
    timestamp = time.time_ns()
    unique_username = f"BenchmarkUser_{timestamp}"
    unique_email = f"benchmark_user_{timestamp}@test.com"
    
    data = {
        "username": unique_username,
        "email": unique_email,
        "password": "password123",
        "password_confirm": "password123",
        "role": 1, # Asumsi role 1 (Siswa) ada
    }
    response = session.post(f"{BASE_URL}/users/register/", json=data, timeout=10)
    
    # Jika berhasil, simpan ID pengguna untuk dibersihkan nanti
    if response.status_code == 201:
        user_id = response.json().get('id')
        if user_id:
            with lock:
                created_user_ids.append(user_id)
    return response

# Fungsi untuk teardown (membersihkan data)
def delete_user(session, headers, user_id):
    """Menghapus pengguna berdasarkan ID."""
    url = f"{BASE_URL}/users/{user_id}/"
    return session.delete(url, headers=headers)

# ==============================================================================
# FUNGSI API UNTUK MODUL ATTENDANCE
# ==============================================================================

# --- AttendancePlatform --- 
def get_attendance_platforms(session, headers, **kwargs):
    return session.get(f"{BASE_URL}/attendance/platforms/", headers=headers, timeout=10)

def create_attendance_platform(session, headers, **kwargs):
    timestamp = time.time_ns()
    data = {
        "status_code": f"CODE_{timestamp}",
        "status_name": f"Status Name {timestamp}",
        "is_agent_approval": random.choice([True, False])
    }
    return session.post(f"{BASE_URL}/attendance/platforms/", json=data, headers=headers, timeout=10)

def get_attendance_platform_detail(session, headers, platform_id, **kwargs):
    return session.get(f"{BASE_URL}/attendance/platforms/{platform_id}/", headers=headers, timeout=10)

def update_attendance_platform(session, headers, platform_id, **kwargs):
    data = {
        "status_name": f"Updated Status Name {time.time_ns()}"
    }
    return session.put(f"{BASE_URL}/attendance/platforms/{platform_id}/", json=data, headers=headers, timeout=10)

def delete_attendance_platform(session, headers, platform_id, **kwargs):
    return session.delete(f"{BASE_URL}/attendance/platforms/{platform_id}/", headers=headers, timeout=10)

# --- SchoolHolidaysOrEvents --- 
def get_school_holidays_or_events(session, headers, **kwargs):
    return session.get(f"{BASE_URL}/attendance/holidays-events/", headers=headers, timeout=10)

def create_school_holiday_or_event(session, headers, academic_year_id, **kwargs):
    timestamp = time.time_ns()
    start_date = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    end_date = start_date # Untuk sederhana, buat acara satu hari
    data = {
        "event_name": f"Event {timestamp}",
        "description": "Deskripsi acara benchmark",
        "event_date_start": start_date,
        "event_date_end": end_date,
        "is_school_off": random.choice([True, False]),
        "target_audience_type": random.choice(['Students_Only', 'Teachers_Only', 'All_Users']),
        "academic_year": academic_year_id # Asumsi academic_year_id valid
    }
    return session.post(f"{BASE_URL}/attendance/holidays-events/", json=data, headers=headers, timeout=10)

# --- AbsenceRequests --- 
def get_absence_requests(session, headers, **kwargs):
    return session.get(f"{BASE_URL}/attendance/absence-requests/", headers=headers, timeout=10)

def create_absence_request(session, headers, user_id, platform_id, **kwargs):
    start_date = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    end_date = start_date
    data = {
        "requester_user": user_id, # Asumsi user_id valid
        "absence_type_status": platform_id, # Asumsi platform_id valid
        "start_date": start_date,
        "end_date": end_date,
        "reason": f"Alasan izin benchmark {time.time_ns()}",
        "approval_status": "Pending"
    }
    return session.post(f"{BASE_URL}/attendance/absence-requests/", json=data, headers=headers, timeout=10)

# --- Attendances --- 
def get_attendances(session, headers, **kwargs):
    return session.get(f"{BASE_URL}/attendance/records/", headers=headers, timeout=10)

def create_attendance_record(session, headers, user_id, platform_id, **kwargs):
    attendance_date = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    clock_in_time = f"{random.randint(7,9):02d}:{random.randint(0,59):02d}:00"
    data = {
        "employee_user": user_id, # Asumsi user_id valid
        "attendance_date": attendance_date,
        "attendance_status": platform_id, # Asumsi platform_id valid
        "clock_in_time": clock_in_time
    }
    return session.post(f"{BASE_URL}/attendance/records/", json=data, headers=headers, timeout=10)


# ==============================================================================
# LOGIKA BENCHMARK KONKUREN
# ==============================================================================

API_ACTIONS = {
    "get_subjects": get_subjects,
    "get_majors": get_majors,
    "register_user": register_user,
    # Attendance Module Actions
    "get_attendance_platforms": get_attendance_platforms,
    "create_attendance_platform": create_attendance_platform,
    # "get_attendance_platform_detail": get_attendance_platform_detail, # Perlu ID, lebih cocok untuk test fungsional
    # "update_attendance_platform": update_attendance_platform, # Perlu ID
    # "delete_attendance_platform": delete_attendance_platform, # Perlu ID
    "get_school_holidays_or_events": get_school_holidays_or_events,
    # "create_school_holiday_or_event": create_school_holiday_or_event, # Perlu academic_year_id
    "get_absence_requests": get_absence_requests,
    # "create_absence_request": create_absence_request, # Perlu user_id dan platform_id
    "get_attendances": get_attendances,
    # "create_attendance_record": create_attendance_record, # Perlu user_id dan platform_id
}

# Variabel global untuk menyimpan ID yang dibuat agar bisa di-pass ke fungsi create
# Ini adalah penyederhanaan untuk benchmark, idealnya ID ini didapat dari GET request sebelumnya
# atau dari data fixture yang sudah ada di database.
# Untuk benchmark ini, kita akan coba buat beberapa platform dan academic year di awal jika belum ada.

# ID default jika tidak ditemukan atau gagal dibuat (HARUS ADA DI DATABASE ANDA)
DEFAULT_ACADEMIC_YEAR_ID = 1 
DEFAULT_ATTENDANCE_PLATFORM_ID = 1 
DEFAULT_USER_ID_FOR_ATTENDANCE = 1 # ID user yang akan digunakan untuk membuat data absensi

def setup_initial_data_for_attendance(token):
    """Mencoba membuat data awal yang dibutuhkan oleh modul attendance jika belum ada."""
    global DEFAULT_ACADEMIC_YEAR_ID, DEFAULT_ATTENDANCE_PLATFORM_ID
    headers = get_auth_headers(token)
    with requests.Session() as session:
        # Cek atau buat Academic Year
        try:
            response_ay = session.get(f"{BASE_URL}/academic-years/", headers=headers, timeout=5)
            if response_ay.status_code == 200 and response_ay.json():
                DEFAULT_ACADEMIC_YEAR_ID = response_ay.json()[0]['id']
                print_colored(f"[SETUP] Menggunakan Academic Year ID: {DEFAULT_ACADEMIC_YEAR_ID}", "BLUE")
            else:
                # Coba buat jika tidak ada (sesuaikan data jika perlu)
                ay_data = {"year_name": "AY Benchmark", "start_date": "2024-01-01", "end_date": "2024-12-31", "is_active": True}
                response_create_ay = session.post(f"{BASE_URL}/academic-years/", json=ay_data, headers=headers, timeout=5)
                if response_create_ay.status_code == 201:
                    DEFAULT_ACADEMIC_YEAR_ID = response_create_ay.json()['id']
                    print_colored(f"[SETUP] Membuat Academic Year ID: {DEFAULT_ACADEMIC_YEAR_ID}", "GREEN")
        except Exception as e:
            print_colored(f"[SETUP] Gagal setup Academic Year: {e}", "WARNING")

        # Cek atau buat Attendance Platform
        try:
            response_ap = session.get(f"{BASE_URL}/attendance/platforms/", headers=headers, timeout=5)
            if response_ap.status_code == 200 and response_ap.json():
                DEFAULT_ATTENDANCE_PLATFORM_ID = response_ap.json()[0]['id']
                print_colored(f"[SETUP] Menggunakan Attendance Platform ID: {DEFAULT_ATTENDANCE_PLATFORM_ID}", "BLUE")
            else:
                ap_data = {"status_code": "PRESENT_BM", "status_name": "Hadir (Benchmark)"}
                response_create_ap = session.post(f"{BASE_URL}/attendance/platforms/", json=ap_data, headers=headers, timeout=5)
                if response_create_ap.status_code == 201:
                    DEFAULT_ATTENDANCE_PLATFORM_ID = response_create_ap.json()['id']
                    print_colored(f"[SETUP] Membuat Attendance Platform ID: {DEFAULT_ATTENDANCE_PLATFORM_ID}", "GREEN")
        except Exception as e:
            print_colored(f"[SETUP] Gagal setup Attendance Platform: {e}", "WARNING")


def worker_task(token, created_user_ids, lock):
    """Fungsi yang dijalankan oleh setiap pengguna virtual (pekerja)."""
    stats = {"success": 0, "failed": 0, "total_time": 0}
    start_time = time.time()
    
    with requests.Session() as session:
        # Untuk GET requests, kita tidak perlu token. Untuk delete, kita perlu.
        # Untuk register, API Anda mungkin tidak memerlukan token. Sesuaikan jika perlu.
        headers_with_auth = get_auth_headers(token)
        
        actions = list(REQUEST_MIX.keys())
        weights = list(REQUEST_MIX.values())

        while time.time() - start_time < DURATION_SECONDS:
            try:
                chosen_action_name = random.choices(actions, weights, k=1)[0]
                api_function = API_ACTIONS[chosen_action_name]
                
                req_start_time = time.time()
                # Teruskan argumen yang relevan ke fungsi API
                # Beberapa fungsi create memerlukan ID tambahan
                action_kwargs = {
                    "session": session,
                    "headers": headers_with_auth,
                    "created_user_ids": created_user_ids, # Untuk register_user
                    "lock": lock # Untuk register_user
                }
                if chosen_action_name == "create_school_holiday_or_event":
                    action_kwargs["academic_year_id"] = DEFAULT_ACADEMIC_YEAR_ID
                elif chosen_action_name == "create_absence_request":
                    action_kwargs["user_id"] = DEFAULT_USER_ID_FOR_ATTENDANCE
                    action_kwargs["platform_id"] = DEFAULT_ATTENDANCE_PLATFORM_ID
                elif chosen_action_name == "create_attendance_record":
                    action_kwargs["user_id"] = DEFAULT_USER_ID_FOR_ATTENDANCE
                    action_kwargs["platform_id"] = DEFAULT_ATTENDANCE_PLATFORM_ID
                
                response = api_function(**action_kwargs)

                req_end_time = time.time()

                stats["total_time"] += (req_end_time - req_start_time)
                
                if 200 <= response.status_code < 300:
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
            except requests.exceptions.RequestException:
                stats["failed"] += 1
    
    return stats

def run_load_test():
    """Orkestrasi utama untuk menjalankan Load Test."""
    print_colored("="*60, 'HEADER')
    print_colored("MEMULAI REALISTIC LOAD TEST BENCHMARK (DENGAN REGISTER)", 'BOLD')
    print_colored(f"Parameter: {NUM_USERS} pengguna, {DURATION_SECONDS} detik", "BLUE")
    print_colored("="*60, 'HEADER')

    token = login_user()
    if not token:
        print_colored("Login gagal. Benchmark tidak dapat dilanjutkan tanpa token otentikasi yang valid.", "FAIL")
        return

    # Setup data awal untuk modul attendance
    print_colored("\n[SETUP] Menyiapkan data awal untuk modul Attendance...", 'HEADER')
    setup_initial_data_for_attendance(token)
    print_colored("[SETUP] Selesai menyiapkan data awal.", 'GREEN')

    # Shared list dan lock untuk mengumpulkan ID pengguna yang baru dibuat
    created_user_ids = []
    lock = threading.Lock()
    all_stats = []
    
    # --- Tahap Eksekusi Konkuren ---
    print_colored(f"\n[EXECUTE] Menjalankan benchmark dengan {NUM_USERS} pengguna...", 'HEADER')
    start_benchmark_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_USERS) as executor:
        futures = [executor.submit(worker_task, token, created_user_ids, lock) for _ in range(NUM_USERS)]
        
        for future in concurrent.futures.as_completed(futures):
            try:
                all_stats.append(future.result())
            except Exception as e:
                print_colored(f"Sebuah task gagal: {e}", "FAIL")

    end_benchmark_time = time.time()
    actual_duration = end_benchmark_time - start_benchmark_time
    print_colored("\n[EXECUTE] Benchmark selesai.", 'GREEN')

    # --- Tahap Pembersihan Data (Teardown) ---
    if created_user_ids:
        print_colored("\n[TEARDOWN] Membersihkan pengguna yang dibuat oleh benchmark...", 'HEADER')
        
        # Saring daftar ID, kecualikan pengguna yang dilindungi (ID 1 dan 2)
        protected_ids = {1, 2}
        ids_to_delete = [uid for uid in created_user_ids if uid not in protected_ids]
        
        if len(ids_to_delete) < len(created_user_ids):
             print_colored(f"--> ID yang dilindungi ditemukan dan akan dilewati saat penghapusan.", "WARNING")

        with requests.Session() as session:
            # Login lagi untuk memastikan token masih valid untuk operasi delete
            token_for_delete = login_user()
            if not token_for_delete:
                print_colored("Gagal mendapatkan token untuk pembersihan. Melewatkan penghapusan data.", "FAIL")
            else:
                headers = get_auth_headers(token_for_delete)
                deleted_count = 0
                print(f"Mencoba menghapus {len(ids_to_delete)} pengguna...")
                for user_id in ids_to_delete:
                    res = delete_user(session, headers, user_id)
                    if res.status_code == 204:
                        deleted_count += 1
                print(f"{deleted_count} dari {len(ids_to_delete)} pengguna berhasil dihapus.")
    else:
        print_colored("\n[TEARDOWN] Tidak ada pengguna baru yang dibuat untuk dibersihkan.", "WARNING")


    # --- Kalkulasi dan Tampilkan Hasil ---
    print_summary(all_stats, actual_duration)

def print_summary(all_stats, duration):
    """Mencetak ringkasan hasil benchmark yang lebih detail."""
    total_success = sum(s['success'] for s in all_stats)
    total_failed = sum(s['failed'] for s in all_stats)
    total_requests = total_success + total_failed
    total_response_time = sum(s['total_time'] for s in all_stats)

    avg_rps = total_requests / duration if duration > 0 else 0
    avg_time_per_request = total_response_time / total_requests if total_requests > 0 else 0
    
    print_colored("\n="*60, 'HEADER')
    print_colored("RINGKASAN HASIL LOAD TEST", 'BOLD')
    print_colored("="*60, 'HEADER')

    print(f"Durasi Aktual         : {duration:.2f} detik")
    print(f"Total Permintaan       : {total_requests}")
    print_colored(f"   - Berhasil          : {total_success}", "GREEN")
    print_colored(f"   - Gagal             : {total_failed}", "FAIL" if total_failed > 0 else "GREEN")
    
    print_colored("\n--- Metrik Performa ---", "HEADER")
    print_colored(f"Requests Per Second (RPS): {avg_rps:.2f}", "BLUE")
    print_colored(f"Waktu Respons Rata-rata  : {avg_time_per_request * 1000:.2f} ms", "BLUE")
    
    print_colored("\nBenchmark Selesai.", 'GREEN')
    print_colored("="*60, 'HEADER')


if __name__ == "__main__":
    run_load_test()
