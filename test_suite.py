######################################################################
# Author: Zaki Ayoubi
# Purpose: This program is designed to demonstrate testing of the of functionalities of my TVM calculator
# Specifically, it tests, Present value of money, future value of money, interest rate, number of periods
# & payment
####################################################################################
import unittest
from unittest.mock import patch, Mock
from tkinter import messagebox
from main import TVM_calculator

class Test_TVM_Calculator(unittest.TestCase):

    def setUp(self):
        self.calculator = TVM_calculator()

    def test_cal_present_value(self):
        # Test valid inputs
        self.calculator.fv_entry = Mock(get=Mock(return_value="1000"))
        self.calculator.r_entry = Mock(get=Mock(return_value="10"))
        self.calculator.pmt_entry = Mock(get=Mock(return_value="100"))
        self.calculator.n_entry = Mock(get=Mock(return_value="5"))
        self.assertEqual(self.calculator.cal_present_value(), 1000)

        # Test negative input
        self.calculator.fv_entry = Mock(get=Mock(return_value="-1000"))
        self.calculator.r_entry = Mock(get=Mock(return_value="10"))
        self.calculator.pmt_entry = Mock(get=Mock(return_value="100"))
        self.calculator.n_entry = Mock(get=Mock(return_value="5"))
        with patch.object(messagebox, 'showerror') as mock_showerror:
            self.calculator.cal_present_value()
            mock_showerror.assert_called_once()

    def test_cal_future_value(self):
        # Test valid inputs
        self.calculator.pv_entry = Mock(get=Mock(return_value="1000"))
        self.calculator.r_entry = Mock(get=Mock(return_value="10"))
        self.calculator.pmt_entry = Mock(get=Mock(return_value="100"))
        self.calculator.n_entry = Mock(get=Mock(return_value="5"))
        self.assertAlmostEqual(self.calculator.cal_future_value(), 2221.02, places=2)

    def test_cal_interest_rate(self):
        # Test valid inputs
        self.calculator.pv_entry = Mock(get=Mock(return_value=500))
        self.calculator.pmt_entry = Mock(get=Mock(return_value=50))
        self.calculator.n_entry = Mock(get=Mock(return_value=5))
        self.calculator.fv_entry = Mock(get=Mock(return_value=1000))
        self.assertAlmostEqual(self.calculator.cal_interest_rate(), 0.0729, places=2)

    def test_cal_payment(self):
        # Test valid inputs
        self.calculator.pv_entry = Mock(get=Mock(return_value=1000))
        self.calculator.r_entry = Mock(get=Mock(return_value=5))
        self.calculator.n_entry = Mock(get=Mock(return_value=5))
        self.calculator.fv_entry = Mock(get=Mock(return_value=100))
        self.assertAlmostEqual(self.calculator.cal_payment(), -212.88, places=2)

    def test_cal_period(self):
        # Test valid inputs
        self.calculator.pv_entry = Mock(get=Mock(return_value=500))
        self.calculator.r_entry = Mock(get=Mock(return_value=5))
        self.calculator.pmt_entry = Mock(get=Mock(return_value=0))
        self.calculator.fv_entry = Mock(get=Mock(return_value=1000))
        self.assertAlmostEqual(self.calculator.cal_period(), 14.21, places=2)

if __name__ == '__main__':
    unittest.main()
