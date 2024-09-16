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

    def request_user_information(self, list_existing_mobile_number):
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
        while not re.match(MOBILE_NUMBER_PATTERN, mobile_number) or mobile_number in list_existing_mobile_number:
            print("Mobile number is invalid or existed."
                  "Please enter a valid mobile number.")
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

        while not self.__validate_dob(dob):
            print("Invalid Date of Birth. Please enter a valid Date of Birth.")
            dob = input(input_message)

        self.full_name = full_name
        self.mobile_number = mobile_number
        self.password = password
        self.dob = dob
        self.address = address

    def __validate_dob(self, dob):
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
        self.__process_food_menu(
            f"Enter {len(self.food_items) + 1} to Check out.\n", is_check_out=True)

    def process_food_drink_menu(self):
        '''
        Show the food and drink menu.
        '''
        self.__process_food_menu(
            f"Enter {len(self.food_items) + 1} for Drinks Menu.\n")
        self.__process_drink_menu()

    def __process_food_menu(self, last_food_menu, is_check_out=False):
        '''
        Process the food menu.
        '''
        food_menu = self.__get_menu(self.food_items)
        LAST_MENU_INDEX = len(self.food_items) + 1
        food_menu += last_food_menu  # Add last item to the food menu
        print("------- Menu -------")
        print(food_menu)
        while True:
            food_choice = input("\n###-:").strip()
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

    def __process_drink_menu(self):
        drink_menu = self.__get_menu(self.drink_items)
        CHECK_OUT = len(self.drink_items) + 1
        check_out_item = f"Enter {CHECK_OUT} to Check out.\n"
        drink_menu += check_out_item
        print(drink_menu)
        while True:
            drink_choice = input("###-: ").strip()
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

    def __get_menu(self, items):
        menu = ""
        for index, item in enumerate(items):
            menu += f"Enter {index + 1}" + \
                f" for {item.name.ljust(10)} Price AUD {item.price}\n"
        return menu
####### Order Component #######

# Order class is an abstract base class


class Order:
    def __init__(self, user):
        self.user = user
        self.menu = Menu()

    def process_order(self):
        pass

    def get_selected_items(self):
        return self.menu.selected_items

# DineInOrder class is a concrete class of Order class for Dine in order


class DineInOrder(Order):
    def __init__(self, user):
        super().__init__(user)

    def process_order(self):
        self.menu.process_food_drink_menu()

# OnlineOrder class is a concrete class of Order class for Online order


class OnlineOrder(Order):
    def __init__(self, user):
        super().__init__(user)

    def process_order(self):
        self.menu.process_food_menu()

# SelfPickupOrder class is a concrete class of OnlineOrder class for Self Pickup order


class SelfPickupOrder(OnlineOrder):
    def __init__(self, user):
        super().__init__(user)

# DeliveryOrder class is a concrete class of OnlineOrder class for Delivery order


class DeliveryOrder(OnlineOrder):
    def __init__(self, user):
        super().__init__(user)

# Ordering class is a component to start the ordering process


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
                f"-------------Ordering-------------\n"
                f"Please Enter {DINE_IN} for Dine in."
                f"\nPlease Enter {ORDER_ONLINE} for Order Online."
                f"\nPlease Enter {BACK_TO_PREVIOUS} to go to Previous Menu."
                "\n###-: ").strip()
            if ordering_choice == DINE_IN:
                self.order = DineInOrder(self.user)
                break
            elif ordering_choice == ORDER_ONLINE:
                self.order = self.__ordering_online()
                break
            elif ordering_choice == BACK_TO_PREVIOUS:
                break

        return self.order
    # a private method to order online

    def __ordering_online(self):
        # Define application constants
        SELF_PICKUP = "1"
        HOME_DELIVERY = "2"
        BACK_TO_PREVIOUS = "3"
        order = None
        while True:
            ordering_ol_choice = input(
                f"-------------Order Online-------------\n"
                f"*Please Enter {SELF_PICKUP} for Self Pickup."
                f"\n*Please Enter {HOME_DELIVERY} for Home Delivery."
                f"\n*Please Enter {BACK_TO_PREVIOUS} to go to Previous Menu."
                "\n###-: ").strip()
            if ordering_ol_choice == SELF_PICKUP:
                order = SelfPickupOrder(self.user)
                break
            elif ordering_ol_choice == HOME_DELIVERY:
                order = DeliveryOrder(self.user)
                break
            elif ordering_ol_choice == BACK_TO_PREVIOUS:
                break
        return order

####### Payment Component #######

# PaymentItem class is an abstract base class


class PaymentItem:
    def __init__(self):
        self.username = ""
        self.order_id = ""
        self.created_date = datetime.now()
        self.total_amount_paid = 0

# DineInPaymentItem class is a concrete class of PaymentItem class for Dine in payment


class DineInPaymentItem(PaymentItem):
    def __init__(self):
        super().__init__()
        self.type_of_order = "Dine In"
        self.number_of_persons = 0
        self.date_of_visit = ""
        self.time_of_visit = ""

# PickupPaymentItem class is a concrete class of PaymentItem class for Pickup payment


class PickupPaymentItem(PaymentItem):
    def __init__(self):
        super().__init__()
        self.type_of_order = "Pickup"
        self.pickup_time = ""
        self.pickup_date = ""
        self.pickup_person = ""

# DeliveryPaymentItem class is a concrete class of PaymentItem class for Delivery payment


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
    # a method to process the payment in multiple steps

    def process_payment(self):
        '''
        Process the payment.
        '''
        order_amount = self.__calculate_order_amount(
        )  # calculate the total amount of the order
        total_amount = self.calculate_total_with_service_charge(
            order_amount)  # calculate the total amount with service charge
        order_id = self.__create_order_id()  # create the order ID
        payment_item = self.proceeding_order(
            order_id, total_amount)  # proceed the order
        return payment_item
    # abstract method to calculate the total amount with service charge

    def calculate_total_with_service_charge(self, order_amount):
        '''
        Calculate the service charge.
        '''
        pass
    # abstract method to proceed the order

    def proceeding_order(self, order_id, total_amount):
        '''
        Proceed the order.
        '''
        pass
    # a private method to create the order ID, following the format Bxxx

    def __create_order_id(self):
        '''
        Create the order ID.
        '''
        id = random.randint(1, 999)
        return f"B{id:03}"
    # a private method to calculate the total amount of the order

    def __calculate_order_amount(self):
        '''
        Calculate the total amount of the order.
        '''
        order_amount = 0
        print("** Your Order Details:")
        for item in self.ordered_items:
            print(f"{item.name.ljust(10)} - AUD {item.price}")
            order_amount += item.price
        return order_amount
    # a method to validate the date can be used in subclasses

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

    # a method to validate the time can be used in subclasses
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

# DineInPayment class is a concrete class of Payment class for Dine in payment


class DineInPayment(Payment):
    def __init__(self, user, ordered_items):
        super().__init__(user, ordered_items)
    # the implementation of the abstract method to calculate the total amount with service charge

    def calculate_total_with_service_charge(self, order_amount):
        SERVICE_CHARGE = 0.15  # 15% service charge
        total_amount = order_amount + order_amount * SERVICE_CHARGE
        print(f"** Your total payable amount is: {total_amount} AUD "
              f"including AUD {order_amount * SERVICE_CHARGE: .2f} for service charge.")
        return total_amount
    # the implementation of the abstract method to proceed the order

    def proceeding_order(self, order_id, total_amount):
        dine_in_payment_item = DineInPaymentItem()
        dine_in_payment_item.username = self.user.mobile_number
        dine_in_payment_item.order_id = order_id
        dine_in_payment_item.total_amount_paid = total_amount
        print("-- Details for Dine in Order --")
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

        dine_in_number_of_person = input("Please enter "
                                         "the Number of Persons: ")
        while not dine_in_number_of_person.isdigit() or int(dine_in_number_of_person) < 0:
            print("Invalid number of persons. Please enter a valid number of persons.")
            dine_in_number_of_person = input(
                "Please enter the Number of Persons: ")
        dine_in_payment_item.number_of_persons = dine_in_number_of_person

        print("----Thank You for entering the details, Your Booking is confirmed.")
        return dine_in_payment_item


class PickupPayment(Payment):
    def __init__(self, user, ordered_items):
        super().__init__(user, ordered_items)
    # the implementation of the abstract method to calculate the total amount with service charge

    def calculate_total_with_service_charge(self, order_amount):
        total_amount = order_amount
        print(f"** Your total payable amount is: {total_amount} AUD"
              " without any service charge.")
        return total_amount
    # the implementation of the abstract method to proceed the order

    def proceeding_order(self, order_id, total_amount):
        pickup_payment_item = PickupPaymentItem()
        pickup_payment_item.username = self.user.mobile_number
        pickup_payment_item.order_id = order_id
        pickup_payment_item.total_amount_paid = total_amount
        print("-- Details for Pick up Order --")
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

# DeliveryPayment class is a concrete class of Payment class for Delivery payment


class DeliveryPayment(Payment):
    def __init__(self, user, ordered_items):
        super().__init__(user, ordered_items)
        self.distance = 0
    # the implementation of the abstract method to calculate the total amount with service charge

    def calculate_total_with_service_charge(self, order_amount):
        service_charge = 0
        total_amount = order_amount + service_charge
        print(f"Your total payable amount is: {total_amount} AUD"
              " and there will be an additional charge for Delivery.")
        return total_amount
    # the implementation of the abstract method to proceed the order

    def proceeding_order(self, order_id, total_amount):
        delivery_payment_item = DeliveryPaymentItem()
        delivery_payment_item.username = self.user.mobile_number
        delivery_payment_item.order_id = order_id
        delivery_payment_item.total_amount_paid = total_amount
        delivery_payment_item.delivery_address = self.user.address
        print("-- Details for Delivery Order --")
        delivery_date = input("Please enter the Date of Delivery: ")
        while not self.validate_date(delivery_date):
            print("Invalid date. Please enter a valid date.")
            delivery_date = input("Please enter the Date of Delivery"
                                  "(DD/mm/yyyy): ")
        delivery_payment_item.delivery_date = delivery_date

        delivery_time = input("Please enter the Time of Delivery(HH:mm): ")
        while not self.validate_time(delivery_time):
            print("Invalid time. Please enter a valid time.")
            delivery_time = input("Please enter the Time of Delivery: ")
        delivery_payment_item.delivery_time = delivery_time

        delivery_charge = self.__calculate_delivery_charge()

        # Delivery can not be done for more than 12 KM.
        if delivery_charge == -1:
            print("Delivery can not be done for more than 12 KM."
                  "Please select Pick up order.")
            return None
        elif delivery_charge > 0:
            delivery_payment_item.total_amount_paid += delivery_charge
            print(f"Your total payable amount is: {delivery_payment_item.total_amount_paid} AUD"
                  f" including AUD {delivery_charge} for delivery charge.")
            print("---- Thank You for your Order, Your Order has been confirmed.")
        return delivery_payment_item

    def __calculate_delivery_charge(self):
        '''
        Calculate the delivery charge based on the distance.
        '''
        # Define application constants
        FROM_0_TO_4_KM = 3
        FROM_4_TO_8_KM = 6
        FROM_8_TO_12_KM = 10
        service_msg = "*A fix charges for delivery based on the distance.*" + \
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
        # Calculate the delivery charge based on the distance
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

####### Statistics Component #######


class Statistics:
    def __init__(self, paid_orders):
        self.paid_orders = paid_orders

    def print_statistics(self):
        '''
        Print the statistics.
        '''
        while True:
            # Define application constants
            ALL_DINE_IN_ORDERS = '1'
            ALL_PICKUP_ORDERS = '2'
            ALL_DELIVERIES = '3'
            ALL_ORDERS_ASCENDING = '4'
            TOTAL_AMOUNT = '5'
            BACK_TO_PREVIOUS = '6'
            statistics_choice = input(
                f"---- Statistics ----\n"
                f"Please Enter the Option to Print the Statistics."
                f"\n{ALL_DINE_IN_ORDERS} - All Dine in Orders."
                f"\n{ALL_PICKUP_ORDERS} - All Pick up Orders."
                f"\n{ALL_DELIVERIES} - All Deliveries."
                f"\n{ALL_ORDERS_ASCENDING} - All Orders (Ascending Order)."
                f"\n{TOTAL_AMOUNT} - Total Amount Spent on All Orders."
                f"\n{BACK_TO_PREVIOUS} - To go to Previous Menu."
                "\n###-: ").strip()
            if statistics_choice == ALL_DINE_IN_ORDERS:
                self.__print_all_dine()
            elif statistics_choice == ALL_PICKUP_ORDERS:
                self.__print_all_pickup()
            elif statistics_choice == ALL_DELIVERIES:
                self.__print_all_delivery()
            elif statistics_choice == ALL_ORDERS_ASCENDING:
                self.__print_all_orders()
            elif statistics_choice == TOTAL_AMOUNT:
                self.__print_total_amount()
            elif statistics_choice == BACK_TO_PREVIOUS:
                break
            else:
                print("Invalid choice. Please enter a valid choice.")

    def __print_all_dine(self):
        '''
        Print all dine in orders.
        '''
        dine_in_orders = [order for order in self.paid_orders if isinstance(
            order, DineInPaymentItem)]
        print("----All Dine in Orders----")
        self.__print_data(dine_in_orders)

    def __print_all_pickup(self):
        '''
        Print all pickup orders.
        '''
        # Filter all pickup orders
        pickup_orders = [order for order in self.paid_orders if isinstance(
            order, PickupPaymentItem)]
        print("----All Pickup Orders----")
        self.__print_data(pickup_orders)

    def __print_all_delivery(self):
        '''
        Print all delivery orders.
        '''
        # Filter all delivery orders
        delivery_orders = [order for order in self.paid_orders if isinstance(
            order, DeliveryPaymentItem)]
        print("----All Delivery Orders----")
        self.__print_data(delivery_orders)

    def __print_all_orders(self):
        '''
        Print all orders in ascending order.
        '''
        self.paid_orders.sort(key=lambda x: x.total_amount_paid)
        print("----All Orders in Ascending Order----")
        self.__print_data(self.paid_orders)

    def __print_total_amount(self):
        '''
        Print the total amount spent on all orders.
        '''
        total_amount = sum(
            [order.total_amount_paid for order in self.paid_orders])
        print(f"Total amount spent on all orders AUD: {total_amount}")

    def __print_data(self, orders):
        print("Order ID".ljust(20) + "Created Date".ljust(15) +
              "Total Amount Paid".ljust(20) + "Type of Order".ljust(20))
        for order in orders:
            print(f"{order.order_id.ljust(20)}{order.created_date.strftime('%d/%m/%Y').ljust(15)}"
                  f"{str(order.total_amount_paid).ljust(20)}{order.type_of_order.ljust(20)}")

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
            user_choice = input("---- Welcome to the Restaurant ----\n"
                                f"Please Enter {SIGN_UP}  for Sign up."
                                f"\nPlease Enter {SIGN_IN} for Sign in."
                                f"\nPlease Enter {QUIT} for Quit."
                                "\n###-: ").strip()

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
        list_existing_mobile_number = [
            user.mobile_number for user in self.users]
        user.request_user_information(list_existing_mobile_number)
        self.users.append(user)
        print("You have Successfully signed up.")

    def sign_in(self):
        '''
        Sign in the user.
        '''
        print("---- Sign In ----")
        user_name = input("Please enter your Username (Mobile Number): ")
        password = input("Please enter your Password: ")
        login_user = self._verify_user(user_name, password)
        if login_user is not None:
            self.__show_home_page(login_user)

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

    def __show_home_page(self, user):
        '''
        Proceed user to access system.
        '''
        # Define application constants
        START_ORDERING = "2.1"
        STATISTIC = "2.2"
        LOG_OUT = "2.3"
        while True:
            print("---- Home Page ----")
            usr_opt = input(f"\nPlease Enter {START_ORDERING} to Start ordering."
                            f"\nPlease Enter {STATISTIC} to Print statistics."
                            f"\nPlease Enter {LOG_OUT} to Log out.""\n###-: ").strip()
            if usr_opt == START_ORDERING:
                ordering = Ordering(user)
                order = ordering.start_ordering()
                if order is not None:
                    order.process_order()
                    if len(order.get_selected_items()) > 0:
                        self._process_payment(user, order)
            elif usr_opt == STATISTIC:
                statistics = Statistics(self.paid_orders)
                statistics.print_statistics()
            elif usr_opt == LOG_OUT:
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
            print("---- Payment ----")
            payment_choice = input(f"Please Enter {PAYMENT} to proceed to Checkout or"
                                   f"\nEnter {CANCEL} to cancel Order.\n###-: ").strip().capitalize()
            if payment_choice == PAYMENT:
                payment = self._make_payment(user, order)
                if payment is not None:
                    payment_item = payment.process_payment()
                    self.paid_orders.append(payment_item)
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
        elif isinstance(order, SelfPickupOrder):
            payment = PickupPayment(user, order.get_selected_items())
        elif isinstance(order, DeliveryOrder):
            if user.address == "":
                message = "You have not mentioned your address while signing up." + \
                    "\n Please Enter Y if would like to enter your address." + \
                    "\n Enter N if you would like to select other mode of order."
                print(message)
                while True:
                    address_choice = input("\n###-: ").strip().capitalize()
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
