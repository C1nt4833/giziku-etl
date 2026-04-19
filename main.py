from utils.extract import run_extraction_pipeline, target_urls
from utils.transform import transform_akg_data
from utils.load import load_to_csv, load_to_google_sheets
import os

# ============================================================================
# GiziKu ETL PIPELINE - Main Orchestrator
# ============================================================================
# Pipeline: EXTRACT -> TRANSFORM -> LOAD
# 
# UNTUK TEAM:
# - Entry point utama. Jalankan: python main.py
# - Jika error, lihat tahap mana yang gagal (EXTRACT/TRANSFORM/LOAD)
# - Setiap tahap punya error handling -> tidak ada silent failures
# ============================================================================

def main():
    print("GiziKu ETL Pipeline: AKG Indonesia")

    # STEP 1: EXTRACT - Scraping data dari sumber
    # Mengambil data mentah dari Andrafarm berdasarkan target_urls di extract.py
    # Jika fail di step ini, check: URL valid? Internet connection? Server down?
    print("[1/3] Memulai proses Ekstraksi data...")
    raw_data = run_extraction_pipeline(target_urls)
    
    if not raw_data:
        print("Gagal mendapatkan data dari sumber. Proses dihentikan.")
        return

    # STEP 2: TRANSFORM - Bersihkan & process data
    # Melakukan perhitungan total gizi (Dasar + Tambahan untuk Hamil/Menyusui)
    # Jika fail di step ini, check: data format valid? Base reference ada?
    print(f"\n[2/3] Memproses Transformasi untuk {len(raw_data)} item...")
    try:
        clean_data = transform_akg_data(raw_data)
        print("Transformasi selesai (Logika Ibu Hamil/Menyusui diterapkan).")
    except Exception as e:
        print(f"Terjadi kesalahan pada tahap Transform: {e}")
        return

    # STEP 3: LOAD - Simpan ke 2 tempat (CSV backup + Google Sheets share)
    # Jika fail di step ini, check: credentials.json exist? Spreadsheet name correct?
    print("\n[3/3] Memulai proses Loading data...")
    
    # Simpan ke CSV sebagai cadangan LOCAL backup
    load_to_csv(clean_data, file_path="akg_indonesia_final.csv")
    
    # Unggah ke Google Sheets untuk TEAM COLLABORATION
    # Jika credentials.json tidak ada, skip (sudah di .gitignore)
    if os.path.exists("credentials.json"):
        load_to_google_sheets(
            data=clean_data, 
            spreadsheet_name="Data AKG", 
            json_key_path="credentials.json"
        )
    else:
        print("Skip Google Sheets: File 'credentials.json' tidak ditemukan.")

    print("SELURUH PROSES ETL SELESAI!")
    

if __name__ == "__main__":
    main()
