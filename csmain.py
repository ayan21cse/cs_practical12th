import mysql.connector
import random
import re

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ayan",
    database="bank290"
)
cursor = conn.cursor()

def validate_password(password):
    if (len(password) >= 8 and
        any(c.isupper() for c in password) and
        any(c.islower() for c in password) and
        any(c.isdigit() for c in password) and
        any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)):
        return True
    return False

def create_account():
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender (M/F): ")
    address = input("Enter Address: ")
    father_name = input("Enter Father's Name: ")
    mother_name = input("Enter Mother's Name: ")
    phone = input("Enter Phone Number: ")

    while not (phone.isdigit() and len(phone) == 10):
        print("Phone number must be a 10-digit numeric value.")
        phone = (input("Enter Phone Number: "))

    deposit = float(input("Enter Initial Deposit: "))

    # Generate a random 6-digit account number
    account_no = random.randint(100000, 999999)

    # Generate a secure password
    print("Create a password. It must be at least 8 characters, contain one uppercase letter, one lowercase letter, one number, and one special character.")
    password = input("Enter Password: ")

    while not validate_password(password):
        print("Password does not meet the criteria. Please try again.")
        password = input("Enter Password: ")

    # Insert into the accounts table
    query = "INSERT INTO accounts (account_no, name, age, gender, address, father_name, mother_name, phone, balance, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (account_no, name, age, gender, address, father_name, mother_name, phone, deposit, password)
    cursor.execute(query, values)
    conn.commit()

    print(f"Account created successfully! Your Account Number is: {account_no}")

def authenticate():
    account_no = int(input("Enter Account Number: "))
    password = input("Enter Password: ")

    query = "SELECT password FROM accounts WHERE account_no = %s"
    cursor.execute(query, (account_no,))
    result = cursor.fetchone()

    if result is None or result[0] != password:
        print("Authentication failed! Invalid account number or password.")
        return None

    return account_no

def deposit_money():
    account_no = authenticate()
    if account_no is None:
        return

    amount = float(input("Enter Amount to Deposit: "))

    # Check if account exists
    query = "SELECT name FROM accounts WHERE account_no = %s"
    cursor.execute(query, (account_no,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found!")
        return

    name = result[0]

    # Update balance
    query = "UPDATE accounts SET balance = balance + %s WHERE account_no = %s"
    cursor.execute(query, (amount, account_no))
    
    # Record transaction
    query = "INSERT INTO transactions (account_no, account_name, type, amount, date_time) VALUES (%s, %s, %s, %s, NOW())"
    cursor.execute(query, (account_no, name, "Deposit", amount))
    conn.commit()

    print("Amount Deposited Successfully!")

def withdraw_money():
    account_no = authenticate()
    if account_no is None:
        return

    amount = float(input("Enter Amount to Withdraw: "))

    # Check balance and account existence
    query = "SELECT balance, name FROM accounts WHERE account_no = %s"
    cursor.execute(query, (account_no,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found!")
        return

    balance, name = result

    if amount > balance:
        print("Insufficient balance!")
    else:
        # Update balance
        query = "UPDATE accounts SET balance = balance - %s WHERE account_no = %s"
        cursor.execute(query, (amount, account_no))
        
        # Record transaction
        query = "INSERT INTO transactions (account_no, account_name, type, amount, date_time) VALUES (%s, %s, %s, %s, NOW())"
        cursor.execute(query, (account_no, name, "Withdraw", amount))
        conn.commit()

        print("Amount Withdrawn Successfully!")

def check_balance():
    account_no = authenticate()
    if account_no is None:
        return

    query = "SELECT balance, name FROM accounts WHERE account_no = %s"
    cursor.execute(query, (account_no,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found!")
        return

    balance, name = result
    print(f"Account Holder: {name}")
    print(f"Current Balance: {balance}")

def display_transactions():
    account_no = authenticate()
    if account_no is None:
        return

    query = "SELECT account_name, type, amount, date_time FROM transactions WHERE account_no = %s"
    cursor.execute(query, (account_no,))
    transactions = cursor.fetchall()

    if not transactions:
        print("No transactions found for this account.")
        return

    print("\nTransaction History:")
    print("-----------------------------------------")
    print("Account Name | Type | Amount | Date & Time")
    print("-----------------------------------------")
    for transaction in transactions:
        print(f"{transaction[0]} | {transaction[1]} | {transaction[2]} | {transaction[3]}")

while True:
    print("-----------------------------------------")
    print("\nBanking Management System")
    print("-----------------------------------------")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Display Transactions")
    print("6. Exit")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        create_account()
    elif choice == 2:
        deposit_money()
    elif choice == 3:
        withdraw_money()
    elif choice == 4:
        check_balance()
    elif choice == 5:
        display_transactions()
    elif choice == 6:
        print("-----------------------------------------")
        print("Thank you for using the Banking Management System!")
        print("-----------------------------------------")
        break
    else:
        print("Invalid choice! Please try again.")
