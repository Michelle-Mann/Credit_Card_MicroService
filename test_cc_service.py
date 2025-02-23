import unittest
from cc_service import format_cc, validate_card_type, valid_card_length
from cc_service import validate_luhn, validate_expiration


class TestMyModule(unittest.TestCase):
    def test_format(self):
        """Tests format function of cc_service with all correct."""
        cc = "123456789123"
        self.assertEqual(format_cc(cc), "123456789123")

    def test_format2(self):
        """Tests format function of cc_service with spaces in cc."""
        cc = "1234 5678 9123 1111"
        self.assertEqual(format_cc(cc), "1234567891231111")

    def test_format3(self):
        """Tests format function of cc_service with dashes in cc."""
        cc = "1234-5678-9123-1111"
        self.assertEqual(format_cc(cc), "1234567891231111")

    def test_format4(self):
        """Tests format function of cc_service with all zeroes in cc."""
        cc = "0000"
        self.assertEqual(format_cc(cc), "0000")

    def test_format5(self):
        """Tests format function of cc_service with all spaces in cc."""
        cc = "        "
        self.assertEqual(format_cc(cc), -1)

    def test_type1(self):
        """Tests valid Visa Card #"""
        cc = "4111111111111111"
        self.assertEqual(validate_card_type(cc), "Visa")

    def test_type2(self):
        """Tests valid MC card # in range 51-55"""
        cc = "5500000000000004"
        self.assertEqual(validate_card_type(cc), "MC")

    def test_type3(self):
        cc = "340000000000009"
        """Tests valid AmEx card #"""
        self.assertEqual(validate_card_type(cc), "AmEx")

    def test_type4(self):
        """Tests valid MC card # in range 2221-2720"""
        cc = "2720999999999999"
        self.assertEqual(validate_card_type(cc), "MC")

    def test_type5(self):
        """Tests valid Visa card # with incorrect # of digits"""
        cc = "4111111111111"
        self.assertEqual(validate_card_type(cc), "Visa")

    def test_type6(self):
        """Tests valid incorrect card type with valid # of digits"""
        cc = "1234567890123456"
        self.assertEqual(validate_card_type(cc), -1)

    def test_visa_correct_length(self):
        """Tests a Visa card with the correct length (16 digits)."""
        cc = "4111111111111111"  # 16 digits
        self.assertEqual(valid_card_length(cc, "Visa"), "Visa")

    def test_visa_incorrect_length(self):
        """Tests a Visa card with an incorrect length (too short)."""
        cc = "4111111111111"  # 13 digits (too short)
        self.assertEqual(valid_card_length(cc, "Visa"), -1)

    def test_mc_correct_length(self):
        """Tests a MasterCard with the correct length (16 digits)."""
        cc = "5500000000000004"  # 16 digits
        self.assertEqual(valid_card_length(cc, "MC"), "MC")

    def test_mc_incorrect_length(self):
        """Tests a MasterCard with an incorrect length (too long)."""
        cc = "5500000000000004444"  # 19 digits (too long)
        self.assertEqual(valid_card_length(cc, "MC"), -1)

    def test_amex_correct_length(self):
        """Tests an American Express card with the correct length
        (15 digits)."""
        cc = "340000000000009"  # 15 digits
        self.assertEqual(valid_card_length(cc, "AmEx"), "AmEx")

    def test_amex_incorrect_length(self):
        """Tests an American Express card with an incorrect length
        (too short)."""
        cc = "34000000000"  # 11 digits (too short)
        self.assertEqual(valid_card_length(cc, "AmEx"), -1)

    def test_unknown_card_type(self):
        """Tests an unknown card type to ensure it returns -1."""
        cc = "1234567890123456"  # 16 digits
        self.assertEqual(valid_card_length(cc, "Unknown"), -1)

    def test_empty_card_number(self):
        """Tests an empty card number input."""
        cc = ""
        self.assertEqual(valid_card_length(cc, "Visa"), -1)

    def test_luhn1(self):
        """Tests an cc # with correct checksum."""
        cc = "79927398713"  # 5 should be correct
        self.assertTrue(validate_luhn(cc))

    def test_luhn2(self):
        """Tests an cc # with correct checksum."""
        cc = "1234567814"  # 4 should be correct
        self.assertTrue(validate_luhn(cc))

    def test_luhn3(self):
        """Tests an cc # with correct checksum."""
        cc = "9876543217"  # 7 should be correct
        self.assertTrue(validate_luhn(cc))

    def test_expiry1(self):
        """Tests an expiration date with valid two-digit month date."""
        date = "05/25"  # this is valid.
        self.assertTrue(validate_expiration(date))

    def test_expiry2(self):
        """Tests an expiration date with valid single-digit month date."""
        date = "7/27"  # this is valid.
        self.assertTrue(validate_expiration(date))

    def test_expiry3(self):
        """Tests an expiration date with invalid date."""
        date = "11/24"  # Expired
        self.assertFalse(validate_expiration(date))

    def test_expiry4(self):
        """Tests an incorrectly entered date with valid date."""
        date = "2/2027"  # Incorrectly typed
        self.assertEqual(validate_expiration(date), -1)


if __name__ == '__main__':
    unittest.main()
