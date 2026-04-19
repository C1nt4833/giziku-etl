import unittest
from utils.transform import transform_akg_data

class TestTransform(unittest.TestCase):

    def setUp(self):
        """Menyiapkan data mentah (mock) hasil extraction."""
        self.raw_data = [
            {
                "kategori": "Perempuan",
                "label": "19-29 tahun",
                "energi": 2250.0,
                "protein": 60.0,
                "lemak": 65.0,
                "lemak_omega6": 12.0,
                "lemak_omega3": 1.1,
                "karbohidrat": 360.0,
                "serat": 32.0,
                "natrium": 1500.0,
                "air": 2350.0
            },
            {
                "kategori": "Hamil",
                "label": "01-13 minggu",
                "energi": 180.0,   # Nilai tambahan saja
                "protein": 1.0,    # Nilai tambahan saja
                "lemak": 2.3,      # Nilai tambahan saja
                "lemak_omega6": 2.0,
                "lemak_omega3": 0.3,
                "karbohidrat": 25.0,
                "serat": 3.0,
                "natrium": 6.0,    # Asumsi tambahan dari web
                "air": 300.0
            }
        ]

    def test_baseline_calculation(self):
        """Pastikan data Hamil dijumlahkan dengan Baseline Perempuan 19-29 tahun."""
        transformed = transform_akg_data(self.raw_data)
        
        # Cari data hamil hasil transformasi
        hamil_data = next(item for item in transformed if item['Kategori'] == "Hamil")
        
        # Verifikasi penjumlahan Energi: 2250 (base) + 180 (add) = 2430
        self.assertEqual(hamil_data['Energi (kkal)'], 2430.0)
        
        # Verifikasi penjumlahan Protein: 60 (base) + 1 (add) = 61
        self.assertEqual(hamil_data['Protein (g)'], 61.0)
        
        # Verifikasi Lemak: 65 + 2.3 = 67.3
        self.assertAlmostEqual(hamil_data['Lemak (g)'], 67.3)

    def test_normal_category_no_addition(self):
        """Pastikan kategori normal (Perempuan) tidak ikut terjumlahkan dua kali."""
        transformed = transform_akg_data(self.raw_data)
        perempuan_data = next(item for item in transformed if item['Kategori'] == "Perempuan")
        
        # Nilai harus tetap sama dengan input awal
        self.assertEqual(perempuan_data['Energi (kkal)'], 2250.0)

    def test_missing_baseline(self):
        """Tes perilaku sistem jika data baseline Perempuan 19-29 tidak ditemukan."""
        # Data tanpa baseline perempuan
        bad_data = [self.raw_data[1]] 
        transformed = transform_akg_data(bad_data)
        
        hamil_data = transformed[0]
        # Jika base tidak ada, seharusnya hanya mengembalikan nilai aslinya (180) 
        # atau menghandle gracefully agar tidak crash.
        self.assertEqual(hamil_data['Energi (kkal)'], 180.0)

if __name__ == '__main__':
    unittest.main()
