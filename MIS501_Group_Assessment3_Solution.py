from datetime import datetime
import re
####### User Component #######


class User:

    def __init__(self):
        self.full_name = ""
        self.mobile_number = ""
        self.password = ""
        self.dob = ""
        self.address = ""
        self.orders = []

    def request_user_information(self):
        '''
        Request user information from the user and validate it.
        '''
        # Define application constants

        # full name must contain only alphabets and spaces.
        FULL_NAME_PATTERN = r'^[A-Za-z\s]+$'
        # Phone number must start with '0' and have 10 digits.
        MOBILE_NUMBER_PATTERN = r'^0\d{9}$'
        # Password must start with a letter and end with a digit. It must contain either '@' or '&' or '#'.
        PASSWORD_PATTERN = r'^[a-zA-Z].*[@&#].*\d$'

        # Address must contain only alphabets, digits, spaces, and commas.
        ADDRESS_PATTERN = r'^[A-Za-z0-9\s,]+$'

        full_name = input("Please enter your name: ")
        while not re.match(FULL_NAME_PATTERN, full_name):
            print("Invalid name. Please enter a valid name.")
            full_name = input("Please enter your name: ")

        address = input("Please enter your address or press Enter to skip: ")
        while not re.match(ADDRESS_PATTERN, address) and address != "":
            print("Invalid address. Please enter a valid address.")
            address = input("Please enter your address: ")

        mobile_number = input("Please enter your mobile number: ")
        while not re.match(MOBILE_NUMBER_PATTERN, mobile_number):
            print("Invalid mobile number. Please enter a valid mobile number.")
            mobile_number = input("Please enter your mobile number: ")

        password = input("Please enter your Password: ")
        while not re.match(PASSWORD_PATTERN, password):
            print("Invalid Password. Please enter a valid password.")
            password = input("Please enter your Password: ")

        confirm_password = input("Please re-enter your password: ")
        while password != confirm_password:
            print("Password does not match. Please re-enter your password.")
            confirm_password = input("Please re-enter your password: ")

        input_message = "Please enter your Date of Birth # DD/MM/YYYY (No Space): "
        dob = input(input_message)

        while not self._validate_dob(dob):
            print("Invalid Date of Birth. Please enter a valid Date of Birth.")
            dob = input(input_message)

        self.full_name = full_name
        self.mobile_number = mobile_number
        self.password = password
        self.dob = dob
        self.address = address

    def _validate_dob(self, dob):
        '''
        Validate the date of birth.
        '''
        # Date of birth must be in the format dd/mm/yyyy.
        DATE_FORMAT = r'^\d{2}/\d{2}/\d{4}$'
        if not re.match(DATE_FORMAT, dob):
            return False
        # Split the date of birth into day, month, and year
        day, month, year = map(int, dob.split("/"))
        # Validate the input date
        try:
            datetime(year, month, day)
        except ValueError:
            return False
        # Validate the year of birth to ensure the user is at least 21 years old
        if year < 1900 or year > datetime.now().year or datetime.now().year - year < 21:
            return False
        return True

####### Menu Component #######


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Menu:
    def __init__(self):
        self.food_items = [MenuItem("Noodle", 2), MenuItem("Sandwich", 4), MenuItem(
            "Dumpling", 6), MenuItem("Muffins", 8), MenuItem("Pasta", 10), MenuItem("Pizza", 20)]
        self.drink_items = [MenuItem("Coffee", 2), MenuItem(
            "Cold drink", 4), MenuItem("Shake", 6)]
        self.selected_items = []

    def process_food_menu(self):
        '''
        Show the food menu.
        '''
        CHECK_OUT = str(len(self.food_items) + 1)
        self._process_food_menu(f"Enter {CHECK_OUT} to Check out.\n")

    def process_food_drink_menu(self):
        '''
        Show the food and drink menu.
        '''
        LAST_MENU_INDEX = str(len(self.food_items) + 1)
        self._process_food_menu(f"Enter {LAST_MENU_INDEX} for Drinks Menu.\n")
        self._process_drink_menu()

    def _process_food_menu(self, last_food_menu):
        '''
        Process the food menu.
        '''
        food_menu = self._get_menu(self.food_items)
        while True:
            LAST_MENU_INDEX = str(len(self.food_items) + 1)
            food_menu += last_food_menu  # Add check out item to the menu
            food_choice = input(food_menu).strip()
            if food_choice.isdigit() and 0 < int(food_choice) <= len(self.food_items):
                choice_index = int(food_choice) - 1
                choice_item = self.food_items[choice_index]
                self.selected_items.append(choice_item)
                print(f"You have selected {choice_item.name} "
                      "for ${choice_item.price}")
            elif food_choice == LAST_MENU_INDEX:
                break
            else:
                print("Invalid choice. Please enter a valid choice.")
        return

    def _process_drink_menu(self):
        drink_menu = self._get_menu(self.drink_items)
        while True:
            CHECK_OUT = str(len(self.drink_items) + 1)
            check_out_item = f"Enter {CHECK_OUT} to Check out.\n"
            drink_menu += check_out_item
            drink_choice = input(drink_menu).strip()
            if drink_choice.isdigit() and 0 < int(drink_choice) <= len(self.drink_items):
                choice_index = int(drink_choice) - 1
                self.selected_items.append(
                    self.drink_items[choice_index])
                print(f"You have selected {self.drink_items[choice_index]}")
            elif drink_choice == CHECK_OUT:
                break
            else:
                print("Invalid choice. Please enter a valid choice.")

    def _get_menu(self, items):
        menu = ""
        for index, item in enumerate(items):
            menu += f"Enter {index + 1} for {item}\n"
        return menu
####### Order Component #######


class Order:
    def __init__(self, user):
        self.user = user
        self.menu = Menu()
        self.selected_items = []

    def process_order(self):
        pass

    def get_selected_items(self):
        self.process_order()
        return self.selected_items


class DineInOrder(Order):
    def __init__(self, user):
        super().__init__(user)

    def process_order(self):
        super().menu.process_food_drink_menu()


class OnlineOrder(Order):
    def __init__(self, user):
        super().__init__(user)

    def process_order(self):
        super().menu.process_food_menu()


class SelfPickupOrder(OnlineOrder):
    def __init__(self, user):
        super().__init__(user)
        self.pickup_time = ""

    def process_order(self):
        super().menu.process_food_menu()


class DeliveryOrder(OnlineOrder):
    def __init__(self, user):
        super().__init__(user)
        self.delivery_address = ""


class Ordering:
    def __init__(self, user):
        self.user = user
        self.order = Order()

    def start_ordering(self):
        # Define application constants
        DINE_IN = "1"
        ORDER_ONLINE = "2"
        BACK_TO_PREVIOUS = "3"
        while True:
            ordering_choice = input(f"Please Enter {DINE_IN} for Dine in."
                                    "\nPlease Enter {ORDER_ONLINE} for Order Online."
                                    "\nPlease Enter {BACK_TO_PREVIOUS} to go to Previous Menu.---> ").strip()
            if ordering_choice == DINE_IN:
                self.order = DineInOrder(self.user)
            elif ordering_choice == ORDER_ONLINE:
                self._ordering_online()
            elif ordering_choice == BACK_TO_PREVIOUS:
                break

        return self.order

    def _ordering_online(self):
        # Define application constants
        SELF_PICKUP = "1"
        HOME_DELIVERY = "2"
        BACK_TO_PREVIOUS = "3"
        while True:
            ordering_choice = input(f"Please Enter {SELF_PICKUP} for Self Pickup."
                                    "\nPlease Enter {HOME_DELIVERY} for Home Delivery."
                                    "\nPlease Enter {BACK_TO_PREVIOUS} to go to Previous Menu.---> ").strip()
            if ordering_choice == SELF_PICKUP:
                self.order = SelfPickupOrder(self.user)
            elif ordering_choice == HOME_DELIVERY:
                self.order = DeliveryOrder(self.user)
            elif ordering_choice == BACK_TO_PREVIOUS:
                break

####### Payment Component #######


class PaymentItem:
    def __init__(self, username, order_id, date, total_amount_paid, type_of_order, details):
        self.username = username
        self.order_id = order_id
        self.date = date
        self.total_amount_paid = total_amount_paid
        self.type_of_order = type_of_order
        self.details = details


class Payment:
    def __init__(self, user, ordered_items):
        self.user = user
        self.ordered_items = ordered_items

    def process_payment(self):
        return PaymentItem("sample", 1, "2021-10-10", 100, "Dine In", self.ordered_items)

####### Restaurant Component #######


class Restaurant:

    def __init__(self):
        self.users = []
        self.paid_orders = []

    def open(self):

        SIGN_UP = "1"
        SIGN_IN = "2"
        QUIT = "3"

        while True:
            # Display the main menu to the user ( Login page)
            user_choice = input(f"Please Enter {SIGN_UP}  for Sign up."
                                "\nPlease Enter {SIGN_IN} for Sign in."
                                "\nPlease Enter {QUIT} for Quit."
                                "\n ---> ").strip()

            if user_choice == SIGN_UP:
                self.sign_up()
            elif user_choice == SIGN_IN:
                self.sign_in()
            elif user_choice == QUIT:
                break
            else:
                print("Invalid choice. Please enter a valid choice.")

    def sign_up(self):
        '''
        Sign up the user.
        '''
        user = User()
        user.request_user_information()
        self.users.append(user)
        print("User has been successfully signed up.")

    def sign_in(self):
        '''
        Sign in the user.
        '''
        user_name = input("Please enter your Username (Mobile Number): ")
        password = input("Please enter your Password: ")
        login_user = self._verify_user(user_name, password)
        if login_user is not None:
            self._show_home_page(login_user)

    def _verify_user(self, user_name, password):
        '''
        Verify the user credentials.
        '''
        for user in self.users:
            if user.mobile_number == user_name and user.password == password:
                print("You have been successfully Signed in.")
                return user
        print("Invalid Username or Password. Please try again.")
        return None

    def _show_home_page(self, user):
        '''
        Proceed user to access system.
        '''
        # Define application constants
        START_ORDERING = "2.1"
        PRINT_STATISTICS = "2.2"
        LOG_OUT = "2.3"
        while True:
            user_choice = input(f"Please Enter {START_ORDERING} to Start ordering."
                                "\nPlease Enter {PRINT_STATISTICS} to Print statistics."
                                "\nPlease Enter {LOG_OUT} to Log out. --> ").strip()
            if user_choice == START_ORDERING:
                ordering = Ordering(user)
                order = ordering.start_ordering()
                selected_items = order.get_selected_items()
                payment = Payment(user, selected_items)
                paid_item = payment.process_payment()
                self.paid_orders.append(paid_item)
            elif user_choice == PRINT_STATISTICS:
                pass
            elif user_choice == LOG_OUT:
                break
                # Go to the main menu - Login page
            else:
                print("Invalid choice. Please enter a valid choice.")


####### Main #######


def main():
    restaurant = Restaurant()
    restaurant.open()


if __name__ == "__main__":
    main()
