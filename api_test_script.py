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
    "get_subjects": 0.5,  # 50% kemungkinan menjalankan GET /subjects/
    "get_majors": 0.3,    # 30% kemungkinan menjalankan GET /majors/
    "register_user": 0.2  # 20% kemungkinan mendaftarkan pengguna baru
}

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
# FUNGSI API UNTUK BENCHMARK
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
    # Endpoint ini mengasumsikan Anda memiliki hak untuk menghapus pengguna
    # Mungkin perlu disesuaikan dengan API Anda, misal: /users/{id}/delete/
    url = f"{BASE_URL}/users/{user_id}/"
    return session.delete(url, headers=headers)

# ==============================================================================
# LOGIKA BENCHMARK KONKUREN
# ==============================================================================

API_ACTIONS = {
    "get_subjects": get_subjects,
    "get_majors": get_majors,
    "register_user": register_user,
}

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
                response = api_function(
                    session=session, 
                    headers=headers_with_auth, 
                    created_user_ids=created_user_ids, 
                    lock=lock
                )
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
        # Jika login gagal, beberapa aksi mungkin tidak bisa dilakukan
        # Namun, kita bisa lanjutkan untuk menguji endpoint publik seperti register
        print_colored("Login gagal, melanjutkan tanpa token otorisasi untuk beberapa endpoint.", "WARNING")

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
