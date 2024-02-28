import unittest
import pandas as pd

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        # Path to your Excel file
        self.data_file = '../../data/data.xlsx'
        # Try reading the Excel file to ensure it exists and is accessible
        try:
            self.xls = pd.ExcelFile(self.data_file)
        except FileNotFoundError:
            self.fail(f"Excel file not found at {self.data_file}")

    def test_read_excel_file(self):
        """Ensure the Excel file is readable."""
        self.assertIsInstance(self.xls, pd.ExcelFile, "Failed to read the Excel file.")

    def test_sheet_names(self):
        """Check if the Excel file contains the expected sheets (cities)."""
        expected_sheets = ['City1', 'City2']  # Update with your actual expected city sheet names
        sheet_names = self.xls.sheet_names
        self.assertListEqual(sheet_names, expected_sheets, "Sheet names do not match the expected city names.")

    def test_data_structure(self):
        """Verify that each sheet has the expected columns: Date, Hour, MT, PV, Wind."""
        for sheet_name in self.xls.sheet_names:
            df = pd.read_excel(self.data_file, sheet_name=sheet_name)
            expected_columns = ['Date', 'Hour', 'MT', 'PV', 'Wind']  # Update this list based on your actual columns
            for column in expected_columns:
                self.assertIn(column, df.columns, f"Missing expected column '{column}' in sheet '{sheet_name}'.")

if __name__ == '__main__':
    unittest.main()
