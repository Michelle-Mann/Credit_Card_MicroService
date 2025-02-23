import unittest
import random
from cc_service import format_cc, validate_card_type, valid_card_length
from cc_service import validate_luhn


class TestCase(unittest.TestCase):
    def test_random_cc_nums(self):

        # # # Helper function #1 -- invalid headers...
        def generate_invalid_header():
            """Generates a random card header that is NOT Visa, MasterCard,
            or AmEx."""
            while True:
                # Randomly choose header length: 1, 2, 3, or 4 digits
                header_length = random.choice([1, 2, 3, 4])
                header = str(random.randint(10**(header_length-1),
                                            (10**header_length)-1))

                # Ensure it's NOT Visa, MasterCard, or AmEx
                if not (header.startswith("4") or       # Visa (4)
                        51 <= int(header[:2]) <= 55 or  # MasterCard (51-55)
                        2221 <= int(header) <= 2720 or  # MasterCard: 2221-2720
                        header.startswith("34") or      # AmEx (34)
                        header.startswith("37")):       # AmEx (37)
                    return header  # Return valid "invalid" header

        # # # Helper function #2 -- generate digits.
        def generate_random_digits(length):
            """Generates a string of random digits with the given length."""
            return "".join(str(random.randint(0, 9)) for _ in range(length))

        # Random test Generation starts here!
        tests_to_generate = 1000  # Number of randomized test cases

        for i in range(tests_to_generate):
            edge_cases = [12, 13, 14, 17, 18, 19]  # Edge case lengths

            # Randomly determine the card length
            odds_len = random.randint(0, 2)
            if odds_len == 1:
                length = random.choice(edge_cases)  # Edge case lengths
            elif odds_len == 2:
                length = random.randint(10, 25)  # Extreme lengths
            else:
                length = random.choice([15, 16])  # Normal valid length

            odds_header = random.randint(0, 4)

            header_types = ["Visa", "MC", "MC", "AmEx", "AmEx", "Other"]

            prefixes = [[4, 4], [51, 55], [2221, 2720], [34, 34], [37, 37]]

            if header_types[odds_header] == "Other":
                header = generate_invalid_header()
            else:
                start, end = prefixes[odds_header]
                header = random.randint(start, end)

            header = str(header)

            if header_types[odds_header] != "Other":
                expected_type = header_types[odds_header]
            else:
                expected_type = -1

            # Determine remaining digits needed to meet length
            remaining_length = length - len(header) - 1  # -1 for Luhn

            # Ensure remaining numbers are valid digits
            card_no = header + generate_random_digits(remaining_length)

            # **New: Coin flip for Luhn validity**
            make_luhn_valid = random.choice([True, False])

            # Compute correct Luhn check digit
            digits = [int(d) for d in str(card_no)]
            for i in range(len(digits) - 1, -1, -2):
                digits[i] *= 2
                if digits[i] > 9:
                    digits[i] -= 9

            total = sum(digits)
            check_digit = (10 - (total % 10)) % 10

            if make_luhn_valid:
                card_no += str(check_digit)
            else:
                wrong_check_digit = (check_digit + 1) % 10
                card_no += str(wrong_check_digit)

            # 33% chance of adding spaces or dashes
            odds_sep = random.randint(0, 2)
            if odds_sep == 1:
                card_no = " ".join([card_no[i:i + 4] for i in
                                    range(0, len(card_no), 4)])
            elif odds_sep == 2:
                card_no = "-".join([card_no[i:i+4] for i in
                                    range(0, len(card_no), 4)])

            # Run each validation function in a subtest
            with self.subTest(card_no=card_no):
                card_no = format_cc(card_no)

                # For card type:
                self.assertEqual(validate_card_type(card_no), expected_type,
                                 f"valid_card_type failed for {card_no}")

                # Set expected lengths.
                if expected_type == "Visa" or expected_type == "MC":
                    expected_length = 16
                elif expected_type == "AmEx":
                    expected_length = 15
                else:
                    expected_length = -1

                # If the type itself isn't faulty, test the length and Luhn.
                if expected_length > 0:
                    self.assertEqual(valid_card_length(card_no, expected_type),
                                     len(card_no) == expected_length,
                                     f"valid_card_length failed for {card_no}")

                    self.assertEqual(validate_luhn(card_no), make_luhn_valid,
                                     f"validate_luhn failed for {card_no}")
                else:
                    self.assertFalse(valid_card_length(card_no, expected_type),
                                     f"valid_card_length failed for {card_no}")


if __name__ == '__main__':
    unittest.main()
