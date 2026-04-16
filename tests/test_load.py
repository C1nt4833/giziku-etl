import unittest
import os
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_google_sheets

class TestLoad(unittest.TestCase):
    """Test cases untuk load/save data ke berbagai format output.
    
    Mencakup testing file I/O, Google Sheets API integration,
    error handling, dan data validation.
    """

    def setUp(self):
        self.data = [
            {"Kategori": "A", "Energi (kkal)": 100, "Protein (g)": 10},
            {"Kategori": "B", "Energi (kkal)": 150, "Protein (g)": 15}
        ]
        self.path = "test_tmp.csv"

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_load_csv_success(self):
        """Test CSV save dengan data valid."""
        load_to_csv(self.data, self.path)
        self.assertTrue(os.path.exists(self.path))
        
        # Verifikasi isi file
        with open(self.path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1)

    def test_load_csv_empty_data(self):
        """Test CSV save dengan data kosong."""
        load_to_csv([], self.path)
        self.assertFalse(os.path.exists(self.path))

    def test_load_csv_exception_handling(self):
        """Test CSV error handling (cover line 33-34)."""
        with patch("builtins.open", side_effect=Exception("Permission denied")):
            load_to_csv(self.data, self.path)

    @patch('utils.load.gspread.authorize')
    def test_load_gsheet_credentials_not_found(self, mock_auth):
        """Test Google Sheets ketika credentials file tidak ada."""
        with patch('os.path.exists', return_value=False):
            load_to_google_sheets(self.data, "Sheet", "no_credentials.json")
        mock_auth.assert_not_called()

    @patch('utils.load.gspread.authorize')
    def test_load_gsheet_empty_data(self, mock_auth):
        """Test Google Sheets dengan data kosong."""
        with patch('os.path.exists', return_value=True):
            load_to_google_sheets([], "Sheet", "fake.json")
        mock_auth.assert_not_called()

    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.gspread.authorize')
    def test_load_gsheet_full_success(self, mock_auth, mock_creds):
        """Test Google Sheets full success path (cover lines 47-64)."""
        # Setup mocks
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        
        mock_creds.return_value = MagicMock()
        mock_auth.return_value = mock_client
        mock_client.open.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        
        with patch('os.path.exists', return_value=True):
            load_to_google_sheets(self.data, "Data AKG", "fake.json")
        
        # Verifikasi calls
        mock_auth.assert_called_once()
        mock_client.open.assert_called_with("Data AKG")
        mock_spreadsheet.get_worksheet.assert_called_with(0)
        mock_worksheet.clear.assert_called_once()
        self.assertTrue(mock_worksheet.update.called)

    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.gspread.authorize')
    def test_load_gsheet_worksheet_update(self, mock_auth, mock_creds):
        """Test bahwa data di-format dan di-update dengan benar ke worksheet."""
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        
        mock_creds.return_value = MagicMock()
        mock_auth.return_value = mock_client
        mock_client.open.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        
        with patch('os.path.exists', return_value=True):
            load_to_google_sheets(self.data, "Data AKG", "fake.json")
        
        # Cek update call - harus include headers + data rows
        update_calls = mock_worksheet.update.call_args_list
        self.assertEqual(len(update_calls), 1)

    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.gspread.authorize')
    def test_load_gsheet_api_error(self, mock_auth, mock_creds):
        """Test Google Sheets exception handling (cover lines 66-67)."""
        mock_creds.return_value = MagicMock()
        mock_auth.side_effect = Exception("API Error - unauthorized")
        
        with patch('os.path.exists', return_value=True):
            load_to_google_sheets(self.data, "Sheet", "fake.json")

    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.gspread.authorize')
    def test_load_gsheet_open_spreadsheet_error(self, mock_auth, mock_creds):
        """Test Google Sheets ketika gagal membuka spreadsheet."""
        mock_client = MagicMock()
        mock_creds.return_value = MagicMock()
        mock_auth.return_value = mock_client
        mock_client.open.side_effect = Exception("Spreadsheet not found")
        
        with patch('os.path.exists', return_value=True):
            load_to_google_sheets(self.data, "Non-existent Sheet", "fake.json")

    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.gspread.authorize')
    def test_load_gsheet_worksheet_error(self, mock_auth, mock_creds):
        """Test Google Sheets ketika gagal mendapat worksheet."""
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        
        mock_creds.return_value = MagicMock()
        mock_auth.return_value = mock_client
        mock_client.open.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.side_effect = Exception("Worksheet error")
        
        with patch('os.path.exists', return_value=True):
            load_to_google_sheets(self.data, "Data AKG", "fake.json")

if __name__ == '__main__':
    unittest.main()