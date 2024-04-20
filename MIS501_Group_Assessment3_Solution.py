import re
####### User Component #######


class User:

    def __init__(self):
        self.full_name = ""
        self.mobile_number = ""
        self.password = ""
        self.dob = ""
        self.address = ""

    def request_user_information(self):
        # Define application constants
        CURRENT_YEAR = 2021
        # full name must contain only alphabets and spaces.
        FULL_NAME_PATTERN = r'^[A-Za-z\s]+$'
        # Phone number must start with '0' and have 10 digits.
        MOBILE_NUMBER_PATTERN = r'^0\d{9}$'
        # Password must start with a letter and end with a digit. It must contain either '@' or '&' or '#'.
        PASSWORD_PATTERN = r'^[a-zA-Z].*[@&#].*\d$'
        # Date of birth must be in the format dd/mm/yyyy.
        DATE_FORMAT = r'^\d{2}/\d{2}/\d{4}$'
        # Address must contain only alphabets, digits, spaces, and commas.
        ADDRESS_PATTERN = r'^[A-Za-z0-9\s,]+$'

        full_name = input("Please enter your name: ")
        while not re.match(FULL_NAME_PATTERN, full_name):
            print("Invalid name. Please enter a valid name.")
            full_name = input("Please enter your name: ")

        mobile_number = input("Please enter your mobile number: ")
        while not re.match(MOBILE_NUMBER_PATTERN, mobile_number):
            print("Invalid mobile number. Please enter a valid mobile number.")
            mobile_number = input("Please enter your mobile number: ")

        password = input("Please enter your password: ")

        self.full_name = input("Enter your full name: ")
        self.mobile_number = input("Enter your mobile number: ")
        self.password = input("Enter your password: ")
        self.dob = input("Enter your date of birth: ")
        self.address = input("Enter your address: ")


####### Order Component #######


class Order:
    def __init__(self, user, order_type, food_items):
        pass


####### Menu ##################
class Menu:
    def __init__(self):
        pass


####### Restaurant Component #######
class Restaurant:

    def __init__(self):
        self.users = []
        self.orders = []
        self.menu = Menu()

    def open(self):

        SIGN_UP = "1"
        SIGN_IN = "2"
        QUIT = "3"

        while True:

            user_choice = (f"Please Enter {SIGN_UP}  for Sign up."
                           "\nPlease Enter {SIGN_IN} for Sign in."
                           "\nPlease Enter {QUIT} for Quit").strip()

            if user_choice == SIGN_UP:
                self.sign_up()
            elif user_choice == SIGN_IN:
                self.sign_in()
            elif user_choice == QUIT:
                break
            else:
                print("Invalid choice. Please enter a valid choice.")

    def sign_up(self):

        user = User()
        user.request_user_information()
        self.users.append(user)
        print("User has been successfully signed up.")

    def sign_in(self):
        pass


####### Main #######


def main():
    restaurant = Restaurant()
    restaurant.open()


if __name__ == "__main__":
    main()
