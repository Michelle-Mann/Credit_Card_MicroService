"""This is a python program credit-card microservice.
Written by: Michelle Mann

This is the server side of the socket and should receive a message in the form
"[some credit card #]".
"""

import time
import zmq  # For ZeroMQ
import re
import json
from datetime import datetime


# ------------ All functions related to cc checker ----------- #
def format_cc(cc_number: str):
    """Returns useable cc_number as a string, but without whitespace, dashes or
    alpha characters (if exist)"""

    # Removes all non-digits using regex notation, returns -1 if incorrect.
    clean_cc_number = re.sub(r"[^\d]", "", cc_number)
    return clean_cc_number if clean_cc_number else -1


def validate_card_type(cc_number: str):
    """Returns type of credit card (if valid). If not, returns error.

    MC, Visa, or AmEx cards have the following headers / lengths:
        Visa - 4 is first digit (16 digits)
        MC - 51-55 or 2221 - 2720 (16 digits)
        AmEx - 34 or 37 (15 digits)
    """
    patterns = {
        "Visa": r"^4",
        "MC": r"^(5[1-5]|2(?:2(?:[2-9]\d|3\d)|[3-6]\d{2}|7(?:[01]\d|20)))",
        "AmEx": r"^3[47]"
        }

    for card_type, pattern in patterns.items():
        if re.match(pattern, cc_number):
            return card_type

    return -1


def valid_card_length(cc_number: str, card_type: str):
    """Returns card type if card is still valid after length check, otherwise
    returns False"""

    # Store the length of the cc #
    cc_length = len(cc_number)

    # Visa and MC cards have 16 digits, Amex has 15
    valid_lengths = {"Visa": 16, "MC": 16, "AmEx": 15}
    return True if cc_length == valid_lengths.get(card_type, -1) else False


def validate_luhn(cc_number: str):
    """Does checsum digit check to test validity of credit card numbers.
     Returns True if valid card, returns False otherwise."""

    # Creation of a list of digits from the string cc_number.
    digits = [int(d) for d in str(cc_number)]

    # Stores the last digit of the string - this is the listed Luhn's #
    last_digit = digits.pop()

    # Loops through the rest of the list backwards, skipping every other #.
    for i in range(len(digits) - 1, -1, -2):

        # Multiples that digit by 2.
        digits[i] *= 2

        # If the resulting doubling is greater than 9, subtract 9
        if digits[i] > 9:
            digits[i] -= 9

    # We're now looking for the highest multiple of 10 that when subtracted by
    # our total, the result is <= 9.
    total = sum(digits)
    check_digit = (10 - (total % 10)) % 10

    # We return if this is equal to the last digit listed (or not)
    return check_digit == last_digit


def validate_expiration(exp_date: str):
    """Takes a user-input expiration date as a string and returns True for
    valid or False for invalid. Valid dates are input as MM/YY"""

    # Ensures MM is between 1 and 12 only -- captures either leading 0 notation
    # or single digit, and YY is two-digits separated by a "/"
    date_pattern = r"^(0?[1-9]|1[0-2])\/\d{2}$"

    if not re.fullmatch(date_pattern, exp_date):
        return -1

    # Parse month and year details from user-entered exp_date
    exp_date = exp_date.split('/')            # Gives us format of ['MM', 'YY']
    exp_month = int(exp_date[0])
    exp_year = int(exp_date[1])

    # Compare properly formatted date to today, if it's not in the future,
    # return False, otherwise, True.

    # Today's date.
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    # Determine century
    cutoff_year = current_year % 100 + 20       # a little in the future
    if exp_year < cutoff_year:
        exp_year += 2000
    else:
        exp_year += 1900

    return (exp_year > current_year) or \
        (exp_year == current_year and exp_month >= current_month)

# ------------ All functions related to cc checker ----------- #


def validate_card(card_number, exp_date):
    """Returns message responses cc_validation rules"""

    results = {"valid": True}  # Start with a positive assumption

    # Attempts to format card, adds error if failed.
    formatted_cc = format_cc(card_number)
    if formatted_cc == -1:
        results["valid"] = False
        results["error"] = "Invalid card format"
        return results

    # Attempts to determine card type, adds error if failed.
    card_type = validate_card_type(formatted_cc)
    if card_type == -1:
        results["valid"] = False
        results["error"] = "Unknown card header"
        return results
    else:
        results["card_type"] = card_type

    # Attemptes to validate card length based on card type, adds error if
    # failed.
    if not valid_card_length(formatted_cc, card_type):
        results["valid"] = False
        results["error"] = "Incorrect length"
        return results

    # Attempts to validate checksum value, adds error if failed.
    if not validate_luhn(formatted_cc):
        results["valid"] = False
        results["error"] = "Invalid checksum"
        return results

    # Attempts to validate expiration date, adds error if failed.
    valid_date = validate_expiration(exp_date)
    if valid_date == -1:
        results["valid"] = False
        results["error"] = "Invalid date format"
        return results

    if not valid_date:
        results["valid"] = False
        results["error"] = "Card Expired"
        return results

    # Returns valid card message.
    results["valid_exp"] = "Valid"
    return results


# ------------ All related to Sending / Receiving message ----------- #

def start_server():
    # Step #1: Set up the context on the server side.
    context = zmq.Context()

    # Step #2: Sets up this socket as a reply socket.
    socket = context.socket(zmq.REP)

    # Step #3: Sets the port # binding for the socket.
    socket.bind("tcp://*:5557")
    print("Server is running on port 5557...")

    # Step #4: Creation of our listener for loop - listens until it gets a
    # request.
    while True:
        try:

            # Step #5: Stores the message as a variable.
            message = socket.recv()

            # We will decode the message so that we don't get a 'b' before text
            # ZeroMQ defaults to UTF-8 encoding when nothing is specified.
            message_str = message.decode()
            print(f"Received request: {message_str}")

            if len(message) > 0:
                # Client asked server to quit
                if message.decode() == 'Q':
                    break

                # Safely parse JSON
                try:
                    message_dict = json.loads(message)
                except json.JSONDecodeError:
                    socket.send_json({"valid": False,
                                      "error": "Invalid JSON format"})
                    continue

                print(f"Processed request: {message_dict}")

                # Handles bad header calls.
                try:
                    card_number = message_dict["cc_number"]
                    exp_date = message_dict["exp_date"]
                except KeyError:
                    socket.send_json({"valid": False,
                                      "error": "Incorrect message headers \
                                           for service"})
                    continue
                card_number = message_dict.get("cc_number", "")
                exp_date = message_dict.get("exp_date", "")

                result = validate_card(card_number, exp_date)

                # Append results to message_dict
                message_dict.update(result)

                # Make the program sleep for X seconds.
                time.sleep(3)

                print(f"Sending response: {message_dict}")

                # Send message.
                socket.send_json(message_dict)

        # Handle server errors.
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

    # Make a clean exit.
    socket.close()
    context.term()


if __name__ == "__main__":
    start_server()
