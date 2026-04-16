import csv
import gspread
from google.oauth2.service_account import Credentials
import os

# LOAD/PERSIST DATA AKG
# Dua opsi simpan:
# 1. CSV Lokal - untuk local backup (akg_raw.csv)
# 2. Google Sheets - untuk sharing & collaboration (Data AKG spreadsheet)

def load_to_csv(data, file_path="akg_raw.csv"):
    """
    Simpan data ke file CSV lokal sebagai BACKUP.
    
    - Encoding UTF-8: support karakter Indonesia (e.g., "Menyusui")
    - Headers diambil dari key pertama dict - PASTIKAN konsisten
    - Jika data kosong, file tidak dibuat (safety)
    - Gunakan DictWriter untuk maintain column order
    """
    try:
        if not data:
            print("Data kosong, tidak ada yang disimpan ke CSV.")
            return

        # Extract headers dari item pertama - CRITICAL untuk DictWriter
        headers = data[0].keys()

        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
            
        print(f"Data berhasil disimpan ke {file_path}")
    except Exception as e:
        print(f"error CSV: {e}")

def load_to_google_sheets(data, spreadsheet_name="Data AKG", json_key_path="credentials.json"):
    """
    Unggah data ke Google Sheets untuk sharing & real-time collaboration.
    
    CREDENTIALS SETUP:
    - File credentials.json HARUS ada di root folder
    - Dibuat dari Google Cloud Console -> Service Account (download JSON key)
    - JANGAN commit ke Git! Sudah ada di .gitignore
    - Kontak team lead jika hilang/expired
    
    SCOPES (Permission):
    - spreadsheets: Read/Write Google Sheets
    - drive: Access file di Google Drive
    
    SHEET STRUCTURE:
    - Ambil Worksheet pertama (index 0) - PASTIKAN sudah ada di Spreadsheet
    - Nama Spreadsheet harus sesuai di Google Drive
    - Jika spreadsheet hilang, error akan jelas di console
    
    ERROR CASES:
    - No credentials.json -> Return dengan print (tidak crash)
    - Spreadsheet tidak ketemu -> Buat manual di Google Drive
    - Data kosong -> Return early (safety)
    """
    try:
        if not data:
            print("Data kosong, gagal unggah ke Google Sheets.")
            return

        # OAuth2 Scopes - jangan ubah tanpa alasan
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # CRITICAL: File credentials harus ada
        if not os.path.exists(json_key_path):
            print(f"Error: File '{json_key_path}' tidak ditemukan!")
            return

        # Authorize dengan service account
        creds = Credentials.from_service_account_file(json_key_path, scopes=scope)
        client = gspread.authorize(creds)

        # Buka spreadsheet di Google Drive
        sh = client.open(spreadsheet_name)
        worksheet = sh.get_worksheet(0)  # Worksheet index 0 (pertama)

        # Format data: List of Dict -> List of Lists (untuk gspread)
        headers = list(data[0].keys())
        rows = [headers]  # Header row
        
        for item in data:
            rows.append([item.get(h, "") for h in headers])

        # Clear & update worksheet dengan data baru
        worksheet.clear()
        worksheet.update(rows, 'A1')
        
        print(f"Data berhasil diunggah ke Google Sheets: {spreadsheet_name}")

    except Exception as e:
        print(f"Error Google Sheets: {e}")