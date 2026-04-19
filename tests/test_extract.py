import unittest
from unittest.mock import patch, MagicMock
from utils.extract import fetch_content, extract_nutrition_values, run_extraction_pipeline

class TestExtract(unittest.TestCase):

    def setUp(self):
        """Menyiapkan data dummy untuk testing."""
        self.mock_html = "<li>Energi (Energy) : 550 kkal</li><li>Protein : 9 g</li>"
        self.sample_category_map = {
            "Bayi": [("0-5 bulan", "https://fakeurl.com/1")]
        }

    # --- 1. TEST fetch_content ---
    @patch('utils.extract.requests.get')
    def test_fetch_content_success(self, mock_get):
        """Test jika request berhasil (HTTP 200)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>Success</html>"
        mock_get.return_value = mock_response
        
        result = fetch_content("https://fakeurl.com")
        self.assertEqual(result, "<html>Success</html>")

    @patch('utils.extract.requests.get')
    def test_fetch_content_failure(self, mock_get):
        """Test jika request gagal (Timeout/Error) untuk memicu blok 'except'."""
        mock_get.side_effect = Exception("Connection Timeout")
        result = fetch_content("https://fakeurl.com")
        self.assertIsNone(result)

    # --- 2. TEST extract_nutrition_values ---
    def test_extract_nutrition_success(self):
        """Test ekstraksi regex dengan data normal."""
        result = extract_nutrition_values(self.mock_html)
        self.assertEqual(result['energi'], 550.0)
        self.assertEqual(result['protein'], 9.0)

    def test_extract_nutrition_none_input(self):
        """Test proteksi jika input HTML None."""
        self.assertIsNone(extract_nutrition_values(None))

    def test_extract_nutrition_empty_html(self):
        """Test jika HTML ada tapi data gizi tidak ditemukan (memicu 'else')."""
        result = extract_nutrition_values("<html>No Data</html>")
        self.assertEqual(result['energi'], 0.0)
        self.assertEqual(result['protein'], 0.0)

    def test_extract_nutrition_exception(self):
        """Test memicu blok 'except' di extract_nutrition_values."""
        # Memberikan input integer (bukan string) akan memicu error pada BeautifulSoup
        self.assertIsNone(extract_nutrition_values(12345))

    # --- 3. TEST run_extraction_pipeline ---
    @patch('utils.extract.fetch_content')
    def test_pipeline_success(self, mock_fetch):
        """Test alur kerja pipeline dari awal sampai akhir."""
        mock_fetch.return_value = self.mock_html
        
        result = run_extraction_pipeline(self.sample_category_map)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['kategori'], "Bayi")
        self.assertEqual(result[0]['label'], "0-5 bulan")

    def test_pipeline_empty_map(self):
        """Test jika category_map kosong."""
        result = run_extraction_pipeline({})
        self.assertEqual(result, [])

    @patch('utils.extract.fetch_content')
    def test_pipeline_fetch_fails(self, mock_fetch):
        """Test pipeline jika fetch_content mengembalikan None (memicu 'continue')."""
        mock_fetch.return_value = None
        result = run_extraction_pipeline(self.sample_category_map)
        self.assertEqual(result, [])

    @patch('utils.extract.fetch_content')
    def test_pipeline_exception_in_loop(self, mock_fetch):
        """Test memicu blok 'except' di dalam loop pipeline."""
        mock_fetch.side_effect = Exception("Unexpected Error")
        result = run_extraction_pipeline(self.sample_category_map)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
