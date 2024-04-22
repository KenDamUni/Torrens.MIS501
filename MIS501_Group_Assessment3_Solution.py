from datetime import datetime
import re
import random
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
        self._process_food_menu(
            f"Enter {len(self.food_items) + 1} to Check out.\n", is_check_out=True)

    def process_food_drink_menu(self):
        '''
        Show the food and drink menu.
        '''
        self._process_food_menu(
            f"Enter {len(self.food_items) + 1} for Drinks Menu.\n")
        self._process_drink_menu()

    def _process_food_menu(self, last_food_menu, is_check_out=False):
        '''
        Process the food menu.
        '''
        food_menu = self._get_menu(self.food_items)
        LAST_MENU_INDEX = len(self.food_items) + 1
        food_menu += last_food_menu  # Add last item to the food menu
        print(food_menu)
        while True:
            food_choice = input("---> ").strip()
            if food_choice.isdigit():
                choice_index = int(food_choice) - 1
                if 0 <= choice_index < len(self.food_items):
                    choice_item = self.food_items[choice_index]
                    self.selected_items.append(choice_item)
                    print(f"You have selected {choice_item.name} ")
                elif int(food_choice) == LAST_MENU_INDEX:
                    if is_check_out and len(self.selected_items) == 0:
                        print("No items selected. Please select items to proceed.")
                    else:
                        break
                else:
                    print("Invalid choice. Please enter a valid choice.")
            else:
                print("Invalid choice. Please enter a valid choice.")
        return

    def _process_drink_menu(self):
        drink_menu = self._get_menu(self.drink_items)
        CHECK_OUT = len(self.drink_items) + 1
        check_out_item = f"Enter {CHECK_OUT} to Check out.\n"
        drink_menu += check_out_item
        print(drink_menu)
        while True:
            drink_choice = input("----> ").strip()
            if drink_choice.isdigit():
                choice_index = int(drink_choice) - 1
                if 0 <= choice_index < len(self.drink_items):
                    choice_item = self.drink_items[choice_index]
                    self.selected_items.append(choice_item)
                    print(f"You have selected {choice_item.name}")
                elif int(drink_choice) == CHECK_OUT:
                    break
                else:
                    print("Invalid choice. Please enter a valid choice.")
            else:
                print("Invalid choice. Please enter a valid choice.")

    def _get_menu(self, items):
        menu = ""
        for index, item in enumerate(items):
            menu += f"Enter {index + 1}" + \
                f" for {item.name.ljust(10)} Price AUD {item.price}\n"
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
        self.menu.process_food_drink_menu()


class OnlineOrder(Order):
    def __init__(self, user):
        super().__init__(user)

    def process_order(self):
        self.menu.process_food_menu()


class SelfPickupOrder(OnlineOrder):
    def __init__(self, user):
        super().__init__(user)
        self.pickup_time = ""

    def process_order(self):
        self.menu.process_food_menu()


class DeliveryOrder(OnlineOrder):
    def __init__(self, user):
        super().__init__(user)
        self.delivery_address = ""


class Ordering:
    def __init__(self, user):
        self.user = user
        self.order = Order(user)

    def start_ordering(self):
        # Define application constants
        DINE_IN = "1"
        ORDER_ONLINE = "2"
        BACK_TO_PREVIOUS = "3"
        while True:
            ordering_choice = input(
                f"Please Enter {DINE_IN} for Dine in."
                f"\nPlease Enter {ORDER_ONLINE} for Order Online."
                f"\nPlease Enter {BACK_TO_PREVIOUS} to go to Previous Menu.---> ").strip()
            if ordering_choice == DINE_IN:
                self.order = DineInOrder(self.user)
                break
            elif ordering_choice == ORDER_ONLINE:
                self._ordering_online()
                break
            elif ordering_choice == BACK_TO_PREVIOUS:
                break

        return self.order

    def _ordering_online(self):
        # Define application constants
        SELF_PICKUP = "1"
        HOME_DELIVERY = "2"
        BACK_TO_PREVIOUS = "3"
        while True:
            ordering_ol_choice = input(
                f"Please Enter {SELF_PICKUP} for Self Pickup."
                f"\nPlease Enter {HOME_DELIVERY} for Home Delivery."
                f"\nPlease Enter {BACK_TO_PREVIOUS} to go to Previous Menu.---> ").strip()
            if ordering_ol_choice == SELF_PICKUP:
                self.order = SelfPickupOrder(self.user)
                break
            elif ordering_ol_choice == HOME_DELIVERY:
                self.order = DeliveryOrder(self.user)
                break
            elif ordering_ol_choice == BACK_TO_PREVIOUS:
                break

####### Payment Component #######


class PaymentItem:
    def __init__(self):
        self.username = ""
        self.order_id = ""
        self.created_date = datetime.now()
        self.total_amount_paid = 0


class DineInPaymentItem(PaymentItem):
    def __init__(self):
        super().__init__()
        self.type_of_order = "Dine In"
        self.Number_of_Persons = 0
        self.date_of_visit = ""
        self.time_of_visit = ""


class PickupPaymentItem(PaymentItem):
    def __init__(self):
        super().__init__()
        self.type_of_order = "Pickup"
        self.pickup_time = ""
        self.pickup_date = ""
        self.pickup_person = ""


class DeliveryPaymentItem(PaymentItem):
    def __init__(self):
        super().__init__()
        self.type_of_order = "Delivery"
        self.delivery_address = ""
        self.delivery_date = ""
        self.delivery_distance = ""


class Payment:
    def __init__(self, user, ordered_items):
        self.user = user
        self.ordered_items = ordered_items
        self.payment_item = PaymentItem()

    def process_payment(self):
        '''
        Process the payment.
        '''
        order_amount = self._calculate_order_amount()
        total_amount = self.calculate_total_with_service_charge(order_amount)
        order_id = self._create_order_id()
        self.proceeding_order(order_id, total_amount)

    def calculate_total_with_service_charge(self, order_amount):
        '''
        Calculate the service charge.
        '''
        pass

    def proceeding_order(self, order_id, total_amount):
        '''
        Proceed the order.
        '''
        pass

    def _create_order_id(self):
        '''
        Create the order ID.
        '''
        id = random.randint(1, 999)
        return f"B{id:03}"

    def _calculate_order_amount(self):
        '''
        Calculate the total amount of the order.
        '''
        order_amount = 0
        for item in self.ordered_items:
            order_amount += item.price
        return order_amount

    def validate_date(self, date):
        '''
        Validate the date.
        '''
        DATE_FORMAT = r'^\d{2}/\d{2}/\d{4}$'
        if not re.match(DATE_FORMAT, date):
            return False
        day, month, year = map(int, date.split("/"))
        try:
            input_date = datetime(year, month, day)
            if input_date < datetime.now():
                return False

        except ValueError:
            return False
        return True

    def validate_time(self, time):
        '''
        Validate the time.
        '''
        TIME_FORMAT = r'^\d{2}:\d{2}$'
        if not re.match(TIME_FORMAT, time):
            return False
        hour, minute = map(int, time.split(":"))
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            return False
        return True


class DineInPayment(Payment):
    def __init__(self, user, ordered_items):
        super().__init__(user, ordered_items)

    def calculate_total_with_service_charge(self, order_amount):
        SERVICE_CHARGE = 0.15  # 15% service charge
        total_amount = order_amount + order_amount * SERVICE_CHARGE
        print(f"Your total payable amount is: {total_amount} AUD"
              f"including AUD {order_amount * SERVICE_CHARGE} for service charge.")
        return total_amount

    def proceeding_order(self, order_id, total_amount):
        pass


class PickupPayment(Payment):
    def __init__(self, user, ordered_items):
        super().__init__(user, ordered_items)

    def calculate_total_with_service_charge(self, order_amount):
        total_amount = order_amount
        print(f"Your total payable amount is: {
              total_amount} AUD without any service charge.")

    def proceeding_order(self):
        pass


class DeliveryPayment(Payment):
    def __init__(self, user, ordered_items):
        super().__init__(user, ordered_items)

    def calculate_total_with_service_charge(self, order_amount):
        pass

    def proceeding_order(self):
        pass
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
                                f"\nPlease Enter {SIGN_IN} for Sign in."
                                f"\nPlease Enter {QUIT} for Quit."
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
            user_choice = input(
                f"Please Enter {START_ORDERING} to Start ordering."
                f"\nPlease Enter {PRINT_STATISTICS} to Print statistics."
                f"\nPlease Enter {LOG_OUT} to Log out. --> ").strip()
            if user_choice == START_ORDERING:
                ordering = Ordering(user)
                order = ordering.start_ordering()
                if order is not None:
                    self._process_payment(user, order)
            elif user_choice == PRINT_STATISTICS:
                pass
            elif user_choice == LOG_OUT:
                break
                # Go to the main menu - Login page
            else:
                print("Invalid choice. Please enter a valid choice.")

    def _process_payment(self, user, order):
        '''
        Process the payment.
        '''
        # Define application constants
        PAYMENT = "Y"
        CANCEL = "N"
        while True:
            payment_choice = input(f"Please Enter {PAYMENT} to proceed to Checkout or"
                                   f"\nEnter {CANCEL} to cancel Order.\n---> ").strip()
            if payment_choice == PAYMENT:
                self._make_payment(user, order)
                break
            elif payment_choice == CANCEL:
                break
            else:
                print("Invalid choice. Please enter a valid choice.")

    def _make_payment(self, user, order):
        '''
        Make the payment.
        '''
        if isinstance(order, DineInOrder):
            payment = DineInPayment(user, order.get_selected_items())
        elif isinstance(order, PickupPayment):
            payment = PickupPayment(user, order.get_selected_items())
        elif isinstance(order, DeliveryOrder):
            if user.address == "":
                message = "You have not mentioned your address while signing up." + \
                    "\n Please Enter Y if would like to enter your address." + \
                    "\n Enter N if you would like to select other mode of order."
                print(message)
                while True:
                    address_choice = input("---->").strip()
                    if address_choice.capitalize == "Y":
                        address = input("Please enter your address: ").strip()
                        user.address = address
                        break
                    elif address_choice.capitalize == "N":
                        break
                    else:
                        print("Invalid choice. Please enter a valid choice.")
            if user.address != "":
                payment = DeliveryPayment(user, order.get_selected_items())


####### Main #######


def main():
    restaurant = Restaurant()
    restaurant.open()


if __name__ == "__main__":
    main()
