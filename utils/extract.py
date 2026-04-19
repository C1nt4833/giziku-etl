import requests
from bs4 import BeautifulSoup
import re
import time

# EKSTRAKSI DATA AKG (Angka Kecukupan Gizi) dari Andrafarm
# SOURCE: https://m.andrafarm.com/_andra.php?_i=daftar-akg
# CATATAN: URL ini dapat berubah - perlu monitoring berkala dari tim
# MAINTENANCE: Jika error "Kategori tidak ditemukan", berarti struktur web mungkin berubah

target_urls = {
    "Bayi/Anak": [
        ("0-5 bulan", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=4"),
        ("6-11 bulan", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=5"),
        ("1-3 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=6"),
        ("4-6 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=7"),
        ("7-9 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=8"),
    ],
    "Laki-Laki": [
        ("10-12 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=11"),
        ("13-15 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=12"),
        ("16-18 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=13"),
        ("19-29 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=14"),
        ("30-49 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=15"),
        ("50-64 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=16"),
        ("65-80 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=17"),
        ("80+ tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=18")
    ],
    "Perempuan": [
        ("10-12 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=21"),
        ("13-15 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=22"),
        ("16-18 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=23"),
        ("19-29 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=24"),
        ("30-49 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=25"),
        ("50-64 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=26"),
        ("65-80 tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=27"),
        ("80+ tahun", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=28")
    ],
    "Hamil": [
        ("01-13 minggu", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=31"),
        ("14-27 minggu", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=32"),
        ("28-41 minggu", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=33")
    ],
    "Menyusui": [
        ("6 bulan pertama", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=36"),
        ("6 bulan kedua", "https://m.andrafarm.com/_andra.php?_i=daftar-akg&id=37")
    ]
}

def fetch_content(url):
    """
    Mengambil HTML content dari URL dengan error handling.
    
    Args:
        url (str): URL target untuk di-scrape
    
    Returns:
        str: HTML content jika sukses, None jika gagal (timeout/connection error)
    
    PENTING: Timeout 10 detik - cukup untuk koneksi normal. 
    Jika sering timeout, pertimbangkan naik jadi 15-20 detik.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        return response.text
    except Exception as e:
        print(f"Error saat mengambil data: {e}")
        return None 
def extract_nutrition_values(html_content):
    if not html_content: return None
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Mencari semua baris atau elemen list yang mengandung data
        items = soup.find_all(['li', 'tr', 'td']) 
        full_text = " ".join([i.get_text(separator=" ") for i in items])
        
        # Gunakan Regex yang mengunci Nama Nutrisi hingga ke Angkanya
        # Kita gunakan [:\s]+ untuk melewati titik dua dan spasi
        patterns = {
            "energi": r"Energi\s*\(Energy\)\s*[:\s]+\+?([\d,.]+)",
            "protein": r"Protein\s*[:\s]+\+?([\d,.]+)",
            "karbohidrat": r"Karbohidrat\s*\(total\).*?[:\s]+\+?([\d,.]+)",
            "lemak": r"Lemak\s*Total\s*[:\s]+\+?([\d,.]+)",
            "lemak_omega6": r"Lemak\s*Omega\s*6\s*[:\s]+\+?([\d,.]+)",
            "lemak_omega3": r"Lemak\s*Omega\s*3\s*[:\s]+\+?([\d,.]+)",
            "serat": r"Serat,.*?[:\s]+\+?([\d,.]+)",
            "air": r"Air\s*\(Water\)\s*[:\s]+\+?([\d,.]+)",
            "natrium": r"Natrium\s*\(Na\).*?[:\s]+\+?([\d,.]+)"
        }

        results = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                # Mengubah koma desimal Indonesia menjadi titik
                val = match.group(1).replace(',', '.')
                results[key] = float(val)
            else:
                results[key] = 0.0
        return results
    except Exception as e:
        # Ini akan menangkap TypeError dari BeautifulSoup dan mengembalikan None
        print(f"Gagal parsing: {e}")
        return None
    
def run_extraction_pipeline(category_map):
    """
    Main orchestration function untuk scraping semua kategori AKG.
    
    PENTING:
    - time.sleep(0.5): Delay untuk respect server & avoid rate limiting
    - Jika ada error pada URL tertentu, LANJUT (tidak stop semua)
    - Logging verbose untuk debugging bila ada issue
    - Return empty list jika semua gagal (jangan raise error)
    
    Args:
        category_map (dict): Struktur {kategori: [(label, url), ...]}
    
    Returns:
        list: Data nutrition yang berhasil di-extract, atau [] jika gagal semua
    """
    all_data = []
    
    if not category_map:
        print("Error: Map kategori kosong.")
        return all_data

    for category, links in category_map.items():
        print(f"--- Memproses Kategori: {category} ---")
        for label, url in links:
            try:
                print(f"Mengekstrak: {label}...")
                html = fetch_content(url)
                if not html:
                    # URL gagal (timeout/error), skip ke URL berikutnya
                    continue 
                
                nutrition = extract_nutrition_values(html)
                if nutrition:
                    nutrition['kategori'] = category
                    nutrition['label'] = label
                    all_data.append(nutrition)
                
                # RATE LIMITING: Delay 0.5s antara requests untuk respect server
                time.sleep(0.5) 
            except Exception as e:
                # Graceful handling - log error tapi lanjut proses
                print(f"Terjadi kesalahan saat memproses {label}: {e}")
                continue
                
    if not all_data:
        print("Ekstraksi gagal total: Tidak ada data yang berhasil diambil.")
    else:
        print(f"Selesai: {len(all_data)} item berhasil diekstrak.")
        
    return all_data
