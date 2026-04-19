import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
from utils.load import load_to_csv, load_to_google_sheets

class TestLoad(unittest.TestCase):

    def setUp(self):
        """Menyiapkan data dummy untuk testing."""
        self.sample_data = [
            {
                "Kategori": "Laki-Laki",
                "Label": "19-29 tahun",
                "Energi": 2650.0,
                "Protein": 65.0
            }
        ]
        self.empty_data = []

    # --- 1. TEST load_to_csv ---

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.DictWriter")
    def test_load_to_csv_success(self, mock_writer, mock_file):
        """Test berhasil menyimpan CSV."""
        load_to_csv(self.sample_data, "test.csv")
        
        # Memastikan file dibuka
        mock_file.assert_called_with("test.csv", mode='w', newline='', encoding='utf-8')
        # Memastikan writer dipanggil
        mock_writer.return_value.writeheader.assert_called_once()
        mock_writer.return_value.writerows.assert_called_once_with(self.sample_data)

    def test_load_to_csv_empty(self):
        """Test jika data kosong (memicu return early)."""
        with patch('builtins.print') as mock_print:
            load_to_csv(self.empty_data)
            mock_print.assert_any_call("Data kosong, tidak ada yang disimpan ke CSV.")

    @patch("builtins.open", side_effect=Exception("Permission Denied"))
    def test_load_to_csv_exception(self, mock_file):
        """Test memicu blok 'except' pada CSV."""
        with patch('builtins.print') as mock_print:
            load_to_csv(self.sample_data)
            mock_print.assert_any_call("error CSV: Permission Denied")


    # --- 2. TEST load_to_google_sheets ---

    @patch("utils.load.os.path.exists")
    @patch("utils.load.Credentials.from_service_account_file")
    @patch("utils.load.gspread.authorize")
    def test_load_to_sheets_success(self, mock_auth, mock_creds, mock_os):
        """Test berhasil upload ke Google Sheets."""
        # Mock file credentials ada
        mock_os.return_value = True
        
        # Mock gspread objects
        mock_client = MagicMock()
        mock_sh = MagicMock()
        mock_ws = MagicMock()
        
        mock_auth.return_value = mock_client
        mock_client.open.return_value = mock_sh
        mock_sh.get_worksheet.return_value = mock_ws
        
        load_to_google_sheets(self.sample_data)
        
        # Pastikan worksheet dibersihkan dan diupdate
        mock_ws.clear.assert_called_once()
        mock_ws.update.assert_called_once()

    def test_load_to_sheets_empty_data(self):
        """Test upload jika data kosong."""
        with patch('builtins.print') as mock_print:
            load_to_google_sheets(self.empty_data)
            mock_print.assert_any_call("Data kosong, gagal unggah ke Google Sheets.")

    @patch("utils.load.os.path.exists")
    def test_load_to_sheets_no_creds(self, mock_os):
        """Test jika file credentials.json tidak ditemukan."""
        mock_os.return_value = False
        with patch('builtins.print') as mock_print:
            load_to_google_sheets(self.sample_data, json_key_path="missing.json")
            mock_print.assert_any_call("Error: File 'missing.json' tidak ditemukan!")

    @patch("utils.load.os.path.exists")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_load_to_sheets_exception(self, mock_creds, mock_os):
        """Test memicu blok 'except' pada Google Sheets (e.g., API Error)."""
        mock_os.return_value = True
        mock_creds.side_effect = Exception("API Quota Exceeded")
        
        with patch('builtins.print') as mock_print:
            load_to_google_sheets(self.sample_data)
            mock_print.assert_any_call("Error Google Sheets: API Quota Exceeded")

if __name__ == '__main__':
    unittest.main()
