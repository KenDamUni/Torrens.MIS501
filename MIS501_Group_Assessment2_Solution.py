def signup(self):
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    if username in self.users:
        print("Username already exists. Please choose another one.")
    else:
        self.users[username] = password
        print("User created successfully!")


def signin(self):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in self.users and self.users[username] == password:
        print("Login successful!")
    else:
        print("Invalid username or password.")


def run(self):
    while True:
        print("\n1- Sign up\n2- Sign in\n3- Quit application")
        choice = input("Enter your choice: ")
        if choice == '1':
            self.signup()
        elif choice == '2':
            self.signin()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please choose a valid option.")
