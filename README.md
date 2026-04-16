# GiziKu - ETL Pipeline AKG Indonesia

Automated extraction, transformation, dan loading data Angka Kecukupan Gizi (AKG) Indonesia dari sumber online ke Google Sheets untuk keperluan analisis dan kolaborasi tim.

## 📋 Tentang Project

Project ini mengimplementasikan ETL (Extract, Transform, Load) pipeline untuk:
- **Extract**: Scraping data AKG dari website Andrafarm
- **Transform**: Membersihkan, normalizing, dan melakukan kalkulasi khusus untuk kategori ibu hamil/menyusui
- **Load**: Menyimpan hasil ke file CSV lokal dan Google Sheets untuk tim collaboration

## 📁 Struktur Project

```
GiziKu-ETL/
├── main.py                    # Entry point pipeline
├── utils/
│   ├── extract.py            # Web scraping & data fetching
│   ├── transform.py          # Data cleaning & transformation
│   ├── load.py               # CSV & Google Sheets output
│   └── __init__.py
├── tests/
│   ├── test_extract.py       # Unit tests untuk extract module
│   ├── test_load.py          # Unit tests untuk load module
│   ├── test_transform.py     # Unit tests untuk transform module
│   └── __init__.py
├── akg_indonesia_final.csv   # Output file (CSV)
├── akg_raw.csv               # Raw data backup
├── requirements.txt          # Python dependencies
├── .gitignore               # Git exclusion rules
└── README.md                # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip atau virtual environment manager

### Installation

1. Clone repository:
```bash
git clone https://github.com/username/giziku-etl.git
cd giziku-etl
```

2. Setup virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Setup Google Sheets (Optional)

Untuk automatic upload ke Google Sheets:

1. Buat Google Cloud Project dan enable Google Sheets API
2. Download service account credentials sebagai `credentials.json`
3. Letakkan file di root directory project
4. Bagikan Google Sheets dengan email dari service account

### Menjalankan Pipeline

```bash
python main.py
```

**Output:**
- File CSV disimpan ke `akg_indonesia_final.csv`
- Data (jika credentials tersedia) upload ke Google Sheets

## 🧪 Testing

Jalankan unit tests:

```bash
# Run semua tests
python -m unittest discover tests

# Run dengan coverage report
coverage run -m unittest discover tests
coverage report -m
```

## 📊 Pipeline Stages

### 1. Extract (utils/extract.py)
- Fetch HTML dari Andrafarm untuk setiap kategori umur/gender
- Parse data gizi menggunakan regex dan BeautifulSoup
- Error handling untuk network issues & parsing failures
- Output: List of dictionaries dengan nutrient values

### 2. Transform (utils/transform.py)
- Normalize column names sesuai standard AKG
- Handle kategori khusus:
  - **Ibu Hamil**: Kalkulasi = Dasar (Perempuan) + Tambahan (Hamil)
  - **Ibu Menyusui**: Kalkulasi = Dasar (Perempuan) + Tambahan (Menyusui)
- Remove non-AKG columns (Gula, Kolesterol, Waktu_Makan)
- Output: Normalized dan calculated nutrient data

### 3. Load (utils/load.py)
- Simpan ke CSV dengan UTF-8 encoding
- Upload ke Google Sheets via API (jika credentials ada)
- Automatic worksheet clearing & update
- Error handling untuk file I/O & API rate limits

## 📝 Data Structure

### Input (Extract output):
```python
{
    "label": "19-29 tahun",
    "kategori": "Laki-Laki",
    "energi": 2650.0,
    "protein": 65.0,
    "lemak": 78.0,
    ...
}
```

### Output (Transform output):
```python
{
    "Label_Umur_Kondisi": "Laki-Laki 19-29 tahun",
    "Kategori": "Laki-Laki",
    "Energi (kkal)": 2650.0,
    "Protein (g)": 65.0,
    "Lemak Total (g)": 78.0,
    ...
}
```

## ⚠️ Important Notes

### Data Source
- Source URL: https://m.andrafarm.com/_andra.php?_i=daftar-akg
- URL dapat berubah tanpa notifikasi - perlu monitoring berkala
- Jika error kategori tidak ditemukan = struktur web kemungkinan berubah

### Maintenance
- Test coverage target: >85%
- Update target_urls jika website struktur berubah
- Monitor API rate limits untuk Google Sheets

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection timeout | Check internet connection, verify URL masih valid |
| "Kategori tidak ditemukan" | Website Andrafarm struktur berubah, update regex/selectors |
| Google Sheets upload gagal | Cek credentials.json exist & memiliki akses ke spreadsheet |
| CSV save error | Cek folder permissions, pastikan disk space cukup |
| Test failure | Run `pip install -r requirements.txt` ulang untuk update dependencies |

## 📄 License

Project ini menggunakan lisensi MIT. Lihat [LICENSE](LICENSE) untuk detail.

## 📞 Support & Contact

Untuk issues, questions, atau suggestions:
- Buat GitHub Issue untuk bug reports
- Diskusi di team chat untuk general questions
- Code review request untuk PR changes

## 🔄 Changelog

### v1.0.0 (Current)
- Initial release
- Extract, Transform, Load pipeline complete
- Google Sheets integration
- Unit tests dengan coverage

---

**Last Updated**: April 2026  
**Maintained By**: Tim Capstone Proyek GiziKu
