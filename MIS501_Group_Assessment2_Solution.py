import re
# Define application constants
CURRENT_YEAR = 2021
MOBILE_NUMBER_PATTERN = r'^0\d{9}$'
PASSWORD_PATTERN = r'^[a-zA-Z][@&#]\d+$'
DATE_FORMAT = r'^\d{2}/\d{2}/\d{4}$'

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
    return re.match(r'^[a-zA-Z].*[@&#].*\d$', password)


def validate_dob(dob):
    '''
    Date of birth must be in the format dd/mm/yyyy.
    '''
    is_valid = True
    if re.match(DATE_FORMAT, dob):
        day, month, year = map(int, dob.split('/'))
        if (day < 1 or day > 31) and (month < 1 or month > 12) and (year < 1900 or
                                                                    (year - CURRENT_YEAR) < 21):
            is_valid = False
        elif (month == 2 and day > 29):
            is_valid = False
        elif (month == 2 and day == 29 and year % 4 != 0):
            is_valid = False
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
    step = 1
    while True:
        if step == 1:
            full_name = input("Enter a full name: ")
            if len(full_name) < 3:
                print("Name must be at least 3 characters long.")
            else:
                step += 1
        if step == 2:
            user_mobile_number = input("Enter a mobile number: ")
            if not validate_mobile_number(user_mobile_number):
                print("Invalid mobile number. Please enter a valid number.")
            else:
                step += 1
        if step == 3:
            password = input("Enter a password: ")
            if not validate_password(password):
                print("Invalid password. Please enter a valid password.")
            else:
                step += 1
        if step == 4:
            dob = input("Enter your date of birth (dd/mm/yyyy): ")
            if not validate_dob(dob):
                print("Invalid date of birth. Please enter a valid date of birth.")
            else:
                user_full_names.append(full_name)
                user_passwords.append(password)
                user_mobile_numbers.append(user_mobile_number)
                user_dobs.append(dob)
                print("User registered successfully.")
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
        user_info = (user_full_names[index], username, user_passwords[index], user_dobs[index])
    else:
        user_info = None

    return user_info

def reset_password(username):
    '''
    Reset password for a user.
    '''
    while True:
        new_password = input("Enter new password: ")
        if validate_password(new_password):
            index = user_mobile_numbers.index(username)
            user_passwords[index] = new_password
            print("Password reset successfully.")
        else:
            print("Invalid password. Please enter a valid password.")

def process_signed_in_user(username):
    '''
    Process signed in user.
    '''
    # Define user actions
    RESETTING_PASSWORD = '1'
    SIGN_OUT = '2'
    user_info = get_user_details(username)
    if user_info:
        full_name, username, password, dob = user_info
        print(f"Welcome {full_name}!")
        user_choice = input(f"Please enter {RESETTING_PASSWORD} for resetting password. 
                            Please enter {SIGN_OUT} for signing out.")
        if user_choice == RESETTING_PASSWORD:
            reset_password(username)
    else:
        print("User not found.")

def sign_in():
    username = input("Please enter your Username (Mobile Number): ")
    password = input("Please enter your password: ")
    is_valid_user = False
    if username in user_mobile_numbers:
        while True:
            is_valid_user = verify_user(username, password)
            if is_valid_user:
                print("You have successfully Signed in!")
                break
            else:
                print("Invalid password.")
    else:
        print("You have not signed up with this Contact Number. Please sign up first.")


################### Task 2C ###################
        
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
        return False
    else:
        print("Invalid choice. Please choose a valid option.")

    return True


# Main Program
user_full_names = []
user_passwords = []
user_mobile_numbers = []
user_dobs = []

while True:
    if not process():
        break
    
