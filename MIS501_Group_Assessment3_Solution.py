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

    def process_order(self):
        pass

    def get_selected_items(self):
        return self.menu.selected_items


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


class DeliveryOrder(OnlineOrder):
    def __init__(self, user):
        super().__init__(user)


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
        self.number_of_persons = 0
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
        print("** Your Order Details:")
        for item in self.ordered_items:
            print(f"{item.name.ljust(10)} - AUD {item.price}")
            order_amount += item.price
        return order_amount

    def validate_date(self, date_string):
        '''
        Validate the date.
        '''
        DATE_FORMAT = r'^\d{2}/\d{2}/\d{4}$'
        if not re.match(DATE_FORMAT, date_string):
            return False
        try:
            input_date = datetime.strptime(date_string, "%d/%m/%Y")
            current_date_string = datetime.now().strftime("%d/%m/%Y")
            current_date = datetime.strptime(current_date_string, "%d/%m/%Y")
            return input_date >= current_date

        except ValueError:
            return False
        return True

    def validate_time(self, time_string):
        '''
        Validate the time.
        '''
        TIME_FORMAT = r'^\d{2}:\d{2}$'
        if not re.match(TIME_FORMAT, time_string):
            return False
        try:
            datetime.strptime(time_string, "%H:%M")
        except ValueError:
            return False
        return True


class DineInPayment(Payment):
    def __init__(self, user, ordered_items):
        super().__init__(user, ordered_items)

    def calculate_total_with_service_charge(self, order_amount):
        SERVICE_CHARGE = 0.15  # 15% service charge
        total_amount = order_amount + order_amount * SERVICE_CHARGE
        print(f"** Your total payable amount is: {total_amount} AUD "
              f"including AUD {order_amount * SERVICE_CHARGE: .2f} for service charge.")
        return total_amount

    def proceeding_order(self, order_id, total_amount):
        dine_in_payment_item = DineInPaymentItem()
        dine_in_payment_item.username = self.user.mobile_number
        dine_in_payment_item.order_id = order_id
        dine_in_payment_item.total_amount_paid = total_amount

        dine_in_date_of_visit = input(
            "Please enter the Date of Booking for Dine in: ")
        while not self.validate_date(dine_in_date_of_visit):
            print("Invalid date. Please enter a valid date.")
            dine_in_date_of_visit = input(
                "Please enter the Date of Booking for Dine in: ")
        dine_in_payment_item.date_of_visit = dine_in_date_of_visit

        dine_in_time_of_visit = input(
            "Please enter the Time of Booking for Dine in: ")
        while not self.validate_time(dine_in_time_of_visit):
            print("Invalid time. Please enter a valid time.")
            dine_in_payment_item.time_of_visit = input(
                "Please enter the Time of Booking for Dine in: ")
        dine_in_payment_item.time_of_visit = dine_in_time_of_visit

        dine_in_number_of_person = input(
            "Please enter the Number of Persons: ")
        while not dine_in_number_of_person.isdigit():
            print("Invalid number of persons. Please enter a valid number of persons.")
            dine_in_number_of_person = input(
                "Please enter the Number of Persons: ")
        dine_in_payment_item.number_of_persons = dine_in_number_of_person

        print("----Thank You for entering the details, Your Booking is confirmed.")
        return dine_in_payment_item


class PickupPayment(Payment):
    def __init__(self, user, ordered_items):
        super().__init__(user, ordered_items)

    def calculate_total_with_service_charge(self, order_amount):
        total_amount = order_amount
        print(f"** Your total payable amount is: {total_amount} AUD"
              " without any service charge.")

    def proceeding_order(self, order_id, total_amount):
        pickup_payment_item = PickupPaymentItem()
        pickup_payment_item.username = self.user.mobile_number
        pickup_payment_item.order_id = order_id
        pickup_payment_item.total_amount_paid = total_amount

        pickup_date = input("Please enter the Date of Pickup: ")
        while not self.validate_date(pickup_date):
            print("Invalid date. Please enter a valid date.")
            pickup_date = input("Please enter the Date of Pickup: ")
        pickup_payment_item.pickup_date = pickup_date

        pickup_time = input("Please enter the Time of Pickup: ")
        while not self.validate_time(pickup_time):
            print("Invalid time. Please enter a valid time.")
            pickup_time = input("Please enter the Time of Pickup: ")
        pickup_payment_item.pickup_time = pickup_time

        pickup_person = input("Please enter the Name of the Person: ")
        while not re.match(r'^[A-Za-z\s]+$', pickup_person):
            print("Invalid name. Please enter a valid name.")
            pickup_person = input("Please enter the Name of the Person: ")
        pickup_payment_item.pickup_person = pickup_person

        print("---- Thank You for entering the details, Your Booking is confirmed.")
        return pickup_payment_item


class DeliveryPayment(Payment):
    def __init__(self, user, ordered_items):
        super().__init__(user, ordered_items)
        self.distance = 0

    def calculate_total_with_service_charge(self, order_amount):
        service_charge = 0
        total_amount = order_amount + service_charge
        print(f"Your total payable amount is: {total_amount} AUD"
              " and there will be an additional charge for Delivery.")

    def proceeding_order(self, order_id, total_amount):
        delivery_payment_item = DeliveryPaymentItem()
        delivery_payment_item.username = self.user.mobile_number
        delivery_payment_item.order_id = order_id
        delivery_payment_item.total_amount_paid = total_amount
        delivery_payment_item.delivery_address = self.user.address

        delivery_date = input("Please enter the Date of Delivery: ")
        while not self.validate_date(delivery_date):
            print("Invalid date. Please enter a valid date.")
            delivery_date = input("Please enter the Date of Delivery: ")
        delivery_payment_item.delivery_date = delivery_date

        delivery_time = input("Please enter the Time of Delivery: ")
        while not self.validate_time(delivery_time):
            print("Invalid time. Please enter a valid time.")
            delivery_time = input("Please enter the Time of Delivery: ")
        delivery_payment_item.delivery_time = delivery_time

        delivery_charge = self._calculate_delivery_charge()

        # Delivery can not be done for more than 12 KM.
        if delivery_charge == -1:
            print("Delivery can not be done for more than 12 KM."
                  "Please select Pick up order.")
            return None
        elif delivery_charge > 0:
            delivery_payment_item.total_amount_paid += int(delivery_charge)
            print(f"Your total payable amount is: {delivery_payment_item.total_amount_paid} AUD"
                  f" including AUD {delivery_charge} for delivery charge.")
        return delivery_payment_item

    def _calculate_delivery_charge(self):
        '''
        Calculate the delivery charge based on the distance.
        '''
        # Define application constants
        FROM_0_TO_4_KM = 3
        FROM_4_TO_8_KM = 6
        FROM_8_TO_12_KM = 10
        service_msg = " A fix charges for delivery based on the distance." + \
            f"\nMore than 0 to 4 KM : ${FROM_0_TO_4_KM}" + \
            f"\nMore than 4 to 8 KM : ${FROM_4_TO_8_KM}" + \
            f"\nMore than 8 to 12 KM : ${FROM_8_TO_12_KM}" + \
            "\nMore than 12 KM : No delivery can be done."
        print(service_msg)
        distance = input("Please enter the distance from the Restaurant: ")
        while not distance.isdigit():
            print("Invalid distance. Please enter a valid distance.")
            distance = input("Please enter the distance from the Restaurant: ")
        self.distance = distance
        if 0 < int(distance) <= 4:
            return FROM_0_TO_4_KM
        elif 4 < int(distance) <= 8:
            return FROM_4_TO_8_KM
        elif 8 < int(distance) <= 12:
            return FROM_8_TO_12_KM
        elif int(distance) > 12:
            self.distance = 0
            print("Delivery can not be done for more than 12 KM.")
            return -1  # Return -1 if delivery can not be done.

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
                    order.process_order()
                    if len(order.get_selected_items()) > 0:
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
        PAYMENT = 'Y'
        CANCEL = 'N'
        while True:
            payment_choice = input(f"Please Enter {PAYMENT} to proceed to Checkout or"
                                   f"\nEnter {CANCEL} to cancel Order.\n---> ").strip().capitalize()
            if payment_choice == PAYMENT:
                payment = self._make_payment(user, order)
                if payment is not None:
                    payment.process_payment()
                    self.paid_orders.append(payment.payment_item)
                break
            elif payment_choice == CANCEL:
                break
            else:
                print("Invalid choice. Please enter a valid choice.")

    def _make_payment(self, user, order):
        '''
        Make the payment.
        '''
        payment = None
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
                    address_choice = input("---->").strip().capitalize()
                    if address_choice == "Y":
                        address = input("Please enter your address: ").strip()
                        user.address = address
                        break
                    elif address_choice == "N":
                        break
                    else:
                        print("Invalid choice. Please enter a valid choice.")
            if user.address != "":
                payment = DeliveryPayment(user, order.get_selected_items())
        return payment


####### Main #######


def main():
    restaurant = Restaurant()
    restaurant.open()


if __name__ == "__main__":
    main()
