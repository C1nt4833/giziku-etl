import unittest
import requests
from unittest.mock import patch
from utils.extract import fetch_content, extract_nutrition_values, run_extraction_pipeline

class TestExtract(unittest.TestCase):
    """Test cases untuk extract data gizi dari web.
    
    Mencakup testing untuk HTTP requests, HTML parsing, error handling,
    dan full extraction pipeline.
    """

    def setUp(self):
        self.sample_html = "Energi: 400 kkal Protein: 15 g Lemak Total: 2 g Karbohidrat: 50 g Serat: 5 g Natrium: 10 mg Air: 600 ml"

    @patch('utils.extract.requests.get')
    def test_fetch_content_success(self, mock_get):
        """Test fetch_content dengan response sukses."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "test content"
        self.assertEqual(fetch_content("http://test.com"), "test content")

    @patch('utils.extract.requests.get')
    def test_fetch_content_connection_error(self, mock_get):
        """Test fetch_content dengan connection error."""
        mock_get.side_effect = requests.exceptions.RequestException("Koneksi gagal")
        self.assertIsNone(fetch_content("http://test.com"))

    @patch('utils.extract.requests.get')
    def test_fetch_content_timeout(self, mock_get):
        """Test fetch_content dengan timeout."""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")
        self.assertIsNone(fetch_content("http://test.com"))

    def test_extract_values_success(self):
        """Test extract_nutrition_values dengan HTML valid."""
        res = extract_nutrition_values(self.sample_html)
        self.assertEqual(res['energi'], 400.0)
        self.assertEqual(res['protein'], 15.0)
        self.assertEqual(res['lemak'], 2.0)

    def test_extract_values_empty_result(self):
        """Test extract_nutrition_values ketika regex tidak menemukan data."""
        res_empty = extract_nutrition_values("Halaman tanpa data gizi")
        self.assertEqual(res_empty['energi'], 0.0)
        self.assertEqual(res_empty['protein'], 0.0)
        self.assertEqual(res_empty['karbohidrat'], 0.0)

    def test_extract_values_none_input(self):
        """Test extract_nutrition_values dengan input None."""
        self.assertIsNone(extract_nutrition_values(None))

    def test_extract_values_empty_string(self):
        """Test extract_nutrition_values dengan input string kosong."""
        self.assertIsNone(extract_nutrition_values(""))

    def test_extract_values_invalid_format(self):
        """Test extract_nutrition_values dengan format yang invalid."""
        invalid_html = "Energi: abc kkal Protein: xyz g"
        res = extract_nutrition_values(invalid_html)
        self.assertEqual(res['energi'], 0.0)
        self.assertEqual(res['protein'], 0.0)

    def test_extract_values_comma_format(self):
        """Test extract_nutrition_values dengan format koma (locale Indonesia)."""
        html_comma = "Energi: 400,5 kkal Protein: 15,3 g"
        res = extract_nutrition_values(html_comma)
        self.assertEqual(res['energi'], 400.5)
        self.assertEqual(res['protein'], 15.3)

    def test_extract_values_malformed_data(self):
        """Test extract_nutrition_values dengan nilai malformed (cover ValueError exception lines 81-82)."""
        # HTML dengan multiple dots/commas yang akan cause ValueError
        # Pattern matches "400,500.10" -> replace -> "400.500.10" -> float error
        html_malformed = "Energi: 400,500.10 kkal"
        res = extract_nutrition_values(html_malformed)
        # Ketika ValueError terjadi, ValueError handler set nilai ke 0.0
        self.assertIsNotNone(res)
        self.assertEqual(res['energi'], 0.0)  # nilai set jadi 0.0 karena ValueError

    @patch('utils.extract.BeautifulSoup')
    def test_extract_values_beautifulsoup_error(self, mock_soup):
        """Test extract_nutrition_values dengan BeautifulSoup error (cover Exception lines 86-88)."""
        mock_soup.side_effect = Exception("BeautifulSoup parsing error")
        result = extract_nutrition_values(self.sample_html)
        self.assertIsNone(result)

    @patch('utils.extract.fetch_content')
    def test_run_pipeline_full_success(self, mock_fetch):
        """Test pipeline dengan semua URL sukses."""
        mock_fetch.return_value = self.sample_html
        target = {"Kategori": [("Label", "url")]}
        res = run_extraction_pipeline(target)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['kategori'], "Kategori")
        self.assertEqual(res[0]['label'], "Label")

    @patch('utils.extract.fetch_content')
    def test_run_pipeline_partial_fail(self, mock_fetch):
        """Test pipeline dengan beberapa URL gagal (cover line 114-116 continue)."""
        mock_fetch.side_effect = [None, self.sample_html]
        target_partial = {"Kategori": [("Gagal", "url1"), ("Sukses", "url2")]}
        res_partial = run_extraction_pipeline(target_partial)
        self.assertEqual(len(res_partial), 1)

    @patch('utils.extract.fetch_content')
    def test_run_pipeline_extraction_fail(self, mock_fetch):
        """Test pipeline ketika extraction gagal parse HTML."""
        mock_fetch.return_value = "Invalid HTML"
        target = {"Kategori": [("Label", "url")]}
        res = run_extraction_pipeline(target)
        self.assertEqual(len(res), 1)

    def test_run_pipeline_empty_map(self):
        """Test pipeline dengan category_map kosong."""
        self.assertEqual(run_extraction_pipeline({}), [])

    @patch('utils.extract.fetch_content')
    def test_run_pipeline_exception_handling(self, mock_fetch):
        """Test pipeline exception handling (cover line 119)."""
        mock_fetch.side_effect = Exception("Network error")
        target = {"Kategori": [("Label", "url")]}
        res = run_extraction_pipeline(target)
        self.assertEqual(len(res), 0)

    @patch('utils.extract.fetch_content')
    def test_run_pipeline_all_fail(self, mock_fetch):
        """Test pipeline ketika semua URL gagal."""
        mock_fetch.return_value = None
        target = {"Kategori": [("Url1", "url1"), ("Url2", "url2")]}
        res = run_extraction_pipeline(target)
        self.assertEqual(len(res), 0)

if __name__ == '__main__':
    unittest.main()