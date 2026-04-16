import unittest
from utils.transform import transform_akg_data

class TestTransform(unittest.TestCase):
    """Test cases untuk transform data gizi sesuai standar AKG.
    
    Mencakup testing normalisasi kolom, logika penjumlahan untuk kategori khusus
    (hamil/menyusui), dan removal kolom yang tidak relevan dengan AKG.
    """

    def setUp(self):
        """Menyiapkan data mentah (raw) simulasi hasil scraping."""
        self.raw_mock_data = [
            {
                "label": "19-29 tahun",
                "kategori": "Perempuan",
                "energi": 2250.0,
                "protein": 60.0,
                "natrium": 1500.0,
                "air": 2350.0
            },
            {
                "label": "19-29 tahun",
                "kategori": "Laki-Laki",
                "energi": 2650.0,
                "protein": 65.0,
                "natrium": 1500.0,
                "air": 2500.0
            },
            {
                "label": "01-13 minggu",
                "kategori": "Hamil",
                "energi": 180.0,   # Nilai tambahan (+) dari web
                "protein": 1.0,    # Nilai tambahan (+) dari web
                "natrium": 0.0,
                "air": 300.0
            }
        ]

    def test_transform_normal_category(self):
        """Memastikan kategori normal (Laki-Laki) tidak berubah angkanya."""
        print("\nTesting Transform Kategori Normal...")
        result = transform_akg_data(self.raw_mock_data)
        
        # Cari data laki-laki di hasil transform
        male_data = next(item for item in result if item['Kategori'] == "Laki-Laki")
        
        self.assertEqual(male_data['Energi (kkal)'], 2650.0)
        self.assertEqual(male_data['Protein (g)'], 65.0)

    def test_transform_pregnancy_logic(self):
        """Memastikan logika penjumlahan (Dasar + Tambahan) untuk Hamil bekerja."""
        print("Testing Logika Penjumlahan Ibu Hamil (Dasar + Tambahan)...")
        result = transform_akg_data(self.raw_mock_data)
        
        # Cari data hamil di hasil transform
        preg_data = next(item for item in result if item['Kategori'] == "Hamil")
        
        # Ekspektasi: Dasar Perempuan (2250) + Tambahan Hamil (180) = 2430
        self.assertEqual(preg_data['Energi (kkal)'], 2430.0)
        # Ekspektasi: Dasar Perempuan (60) + Tambahan Hamil (1) = 61
        self.assertEqual(preg_data['Protein (g)'], 61.0)

    def test_column_removal(self):
        """Memastikan kolom Gula, Kolesterol, dan Waktu_Makan sudah dihapus."""
        print("Testing Penghapusan Kolom Non-AKG...")
        result = transform_akg_data(self.raw_mock_data)
        
        for item in result:
            self.assertNotIn("Gula (g)", item)
            self.assertNotIn("Kolesterol (mg)", item)
            self.assertNotIn("Waktu_Makan", item)
            # memastikan kolom baru yang kita buat ada
            self.assertIn("Label_Umur_Kondisi", item)

if __name__ == '__main__':
    unittest.main()