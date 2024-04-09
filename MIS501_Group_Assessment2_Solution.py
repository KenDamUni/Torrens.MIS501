import re
# Define application constants
CURRENT_YEAR = 2021
MOBILE_NUMBER_PATTERN = r'^0\d{9}$'
PASSWORD_PATTERN = r'^[a-zA-Z].*[@&#].*\d$'
DATE_FORMAT = r'^\d{2}/\d{2}/\d{4}$'
MAX_VALUE_OF_LOGIN_ATTEMPTS = 3

################### Task 2A ###################


def validate_mobile_number(number):
    '''
    Phone number must start with '0' and have 10 digits.
    '''
    if number in user_mobile_numbers:
        print("Mobile number already exists. Please choose another one.")
        return False
    return re.match(MOBILE_NUMBER_PATTERN, number)


def validate_password(password):
    '''
    Password must start with a letter and end with a digit. 
    It must contain either '@' or '&' or '#'.
    '''
    return re.match(PASSWORD_PATTERN, password)


def validate_dob(dob):
    '''
    Date of birth must be in the format dd/mm/yyyy.
    '''
    is_valid = True
    if re.match(DATE_FORMAT, dob):
        day, month, year = map(int, dob.split('/'))
        # Validate day, month, and year.
        # Day must be between 1 and 31, month between 1 and 12,
        # Year between 1900 and 2021 and age must be at least 21 years.
        if (day < 1 or day > 31) and (month < 1 or month > 12) and (year < 1900 or (year - CURRENT_YEAR) < 21):
            is_valid = False
        # February has 29 days in a leap year
        elif (month == 2 and day > 29):
            is_valid = False
        # February has 28 days in a non-leap year
        elif (month == 2 and day == 29 and year % 4 != 0):
            is_valid = False
        # April, June, September, and November have 30 days
        elif (month in [4, 6, 9, 11] and day > 30):
            is_valid = False
        else:
            is_valid = True
    else:
        is_valid = False
    return is_valid


def sign_up():
    '''
    Register a new user.
    '''
    # Define steps for user registration
    step = 1  # Initial step
    while True:
        if step == 1:  # Step 1: Enter full name
            full_name = input("Please enter your name: ")
            if len(full_name) < 3:
                print("Name must be at least 3 characters long.")
            else:
                step += 1  # Move to next step
        if step == 2:  # Step 2: Enter mobile number
            user_mobile_number = input("Please enter your mobile number: ")
            # Validate mobile number
            if not validate_mobile_number(user_mobile_number):
                print(f"You have enter the invalid mobile number"
                      f"\nPlease start again:")
                # Continue to the same step if mobile number is invalid
            else:
                step += 1  # Move to next step
        if step == 3:  # Step 3: Enter password
            password = input("Please enter your password: ")
            if not validate_password(password):
                print(f"You have enter the invalid password."
                      f"\nPlease enter a valid password.")
            else:
                confirm_password = input("Please confirm your Password: ")
                if password != confirm_password:
                    print("Passwords do not match. Please start again.")
                else:
                    step += 1
        if step == 4:  # Step 4: Enter date of birth
            dob = input(
                "Please enter your Date of Birth (DD/MM/YYYY) (No Space): ")
            if not validate_dob(dob):
                print(f"You have enter the Date of Birth in invalid format."
                      f"\nPlease enter a valid date of birth.")
            else:  # Register user if all information is valid
                user_full_names.append(full_name.strip())
                user_passwords.append(password)
                user_mobile_numbers.append(user_mobile_number.strip())
                user_dobs.append(dob.strip())
                print("You have successfully Signed up.")
                break

################### Task 2B ###################


def verify_user(username, password):
    '''
    Verify user by username (Mobile Number) and password.
    '''
    index = user_mobile_numbers.index(username)
    if password == user_passwords[index]:
        return True
    return False


def get_user_details(username):
    '''
    Get user details by username (Mobile Number).
    '''
    if username in user_mobile_numbers:
        index = user_mobile_numbers.index(username)
        # Return user information in a tuple
        user_info = (user_full_names[index], username)
    else:
        user_info = None

    return user_info


def sign_in():
    '''
    Sign in a user.
    '''
    username = input("Please enter your Username (Mobile Number): ")
    password = input("Please enter your password: ")
    is_valid_user = False
    if username in user_mobile_numbers:
        counting_of_login_attempts = 1  # Initialize counting of login attempts
        while counting_of_login_attempts < MAX_VALUE_OF_LOGIN_ATTEMPTS:
            is_valid_user = verify_user(username, password)
            if is_valid_user:
                (full_name, mobile_number) = get_user_details(username)
                print(
                    f"Welcome {full_name}!.\nYou have successfully Signed in!")
                break
            else:
                print("You have entered the wrong Password.\nPlease try again.")
                counting_of_login_attempts += 1
                password = input("Please enter your password: ")

        if not is_valid_user:
            print("You have used the maximum number of attempts of Login")
            # Request for password change after exceeding the maximum number of login attempts
            request_change_password()
        else:
            # Process next step after signing in
            process_signed_in_user(username)
    else:
        print("You have not signed up with this Contact Number. Please sign up first.")


################### Task 2C ###################
def process_signed_in_user(username):
    '''
    Process user actions after signing in.
    '''
    # Define user actions
    RESETTING_PASSWORD = '1'
    SIGN_OUT = '2'
    # Get user details by username in the form of a tuple
    user_info = get_user_details(username)
    if user_info:
        full_name, username = user_info  # Unpack user information from the tuple
        print(f"Welcome {full_name}!")
        while True:
            user_choice = input(f"Please enter {RESETTING_PASSWORD} for Resetting password."
                                f"\nPlease enter {SIGN_OUT} for Sign out.")
            if user_choice.strip() == RESETTING_PASSWORD:
                reset_password(username)
            elif user_choice.strip() == SIGN_OUT:
                print("You have successfully signed out.")
                break
    else:
        print("User not found.")


def request_change_password():
    '''
    Request for password change.
    '''
    print("Please reset the password by entering the following details:")
    username_for_confirming = input(
        "Please enter your Username (Mobile Number) to confirm: ").strip()

    if username_for_confirming in user_mobile_numbers:
        index = user_mobile_numbers.index(username_for_confirming)
        dob_for_confirming = input(
            "Please enter your Date of Birth in DD/MM/YYYY format to confirm: ")
        if dob_for_confirming.strip() == user_dobs[index]:
            reset_password(username_for_confirming)
    else:
        print("User not found")


def reset_password(username):
    '''
    Reset password for a user.
    '''
    while True:
        new_password = input("Enter new password: ")
        if validate_password(new_password):
            # Update password if it is valid
            index = user_mobile_numbers.index(username)
            # Get the index of the username (Mobile Number)
            old_password = user_passwords[index]
            # Check if the new password is the same as the old password
            if old_password == new_password:
                print("You cannot use the password used earlier.")
            else:
                confirm_password = input("Please re-enter password: ")
                if new_password != confirm_password:
                    print("Passwords do not match. Please try again.")
                else:
                    # Update the password
                    user_passwords[index] = new_password
                    print("Password reset successfully.")
                    break
        else:
            print("Invalid password. Please enter a valid password.")


# Define an entry function to process user choice
def process():
    '''
    Process user choice.
    '''
    # Define constants for choice
    SIGN_UP = '1'
    SIGN_IN = '2'
    QUIT = '3'
    print(f"\n{SIGN_UP}- Sign up\n{SIGN_IN}- Sign In\n{QUIT}- Quit application")
    choice = input("Enter your choice: ")
    if choice == SIGN_UP:
        sign_up()
    elif choice == SIGN_IN:
        sign_in()
    elif choice == QUIT:
        # Exit the application
        return False
    else:
        print("Invalid choice. Please choose a valid option.")

    return True  # Continue processing user choice


# Main Program
user_full_names = []
user_passwords = []
user_mobile_numbers = []
user_dobs = []

while True:
    # Process user choice until the user quits the application
    if not process():
        break
