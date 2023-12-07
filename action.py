#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import random
import pandas as pd
import pymysql
from faker import Faker
from datetime import datetime, timedelta,time 
from dateutil.relativedelta import relativedelta  # Import relativedelta for date calculations
from dateutil.parser import parse  # Import parse for date string to datetime conversion
import pymysql
from datetime import datetime, timezone
from datetime import datetime
import pytz
import hashlib
import re
pst = pytz.timezone('America/Los_Angeles')
pd.set_option('display.max_columns', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)


# In[2]:


import pymysql
import hashlib
import pandas as pd
from datetime import datetime, timezone, timedelta
import re

class BankingSystem:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.pst = timezone(timedelta(hours=-8))  # Assuming PST time zone

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def deposit_funds(self, user_id, account_type):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {user_id} AND AccountType = '{account_type}'")
            account_info = cursor.fetchone()

        if account_info:
            amount = float(input("Enter amount: "))

            current_balance = account_info[1]

            confirm = input(f"Are you sure you want to deposit ${amount} into your {account_type} account? (Yes/No): ")
            if confirm.lower() == 'yes':
                with self.connection.cursor() as action_cursor:
                    action_cursor.execute("COMMIT")
                    action_cursor.fetchall()
                    action_cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
                    action_cursor.execute("START TRANSACTION;")
                    action_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {user_id} AND AccountType = '{account_type}'")
                    account_info = action_cursor.fetchone()
                    current_balance = account_info[1]
                    try:
                        new_balance = current_balance + amount
                        pst_now = datetime.now(self.pst)
                        action_cursor.execute(f"UPDATE Account SET CurrentBalance = {new_balance} WHERE AccountID = {account_info[0]}")
                        action_cursor.execute("INSERT INTO Transaction (AccountID, TransactionType, Amount, TransactionDate) VALUES (%s, %s, %s, %s)", (account_info[0], 'deposit', amount, pst_now))
                        action_cursor.execute("COMMIT")
                        self.connection.commit()
                        print("Deposit successful.")
                    except Exception as e:
                        self.connection.rollback()
                        print("Error occurred during deposit. Rolling back changes.")
                        print("Error:", e)
            else:
                print("Deposit canceled by the user.")
        else:
            print(f"No {account_type} account found for the provided User ID.")

    def withdraw_funds(self, user_id, account_type):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {user_id} AND AccountType = '{account_type}'")
            account_info = cursor.fetchone()

        if account_info:
            amount = float(input("Enter amount: "))

            current_balance = account_info[1]

            confirm = input(f"Are you sure you want to withdraw ${amount} from your {account_type} account? (Yes/No): ")
            if confirm.lower() == 'yes':
                if amount > current_balance or amount <= 0:
                    print("Withdrawal amount is invalid. Transaction cancelled.")
                else:
                    with self.connection.cursor() as action_cursor:
                        action_cursor.execute("COMMIT")
                        action_cursor.fetchall()
                        action_cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
                        action_cursor.execute("START TRANSACTION")
                        action_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {user_id} AND AccountType = '{account_type}'")
                        account_info = action_cursor.fetchone()
                        current_balance = account_info[1]
                        try:
                            new_balance = current_balance - amount
                            pst_now = datetime.now(self.pst)
                            action_cursor.execute(f"UPDATE Account SET CurrentBalance = {new_balance} WHERE AccountID = {account_info[0]}")
                            action_cursor.execute("INSERT INTO Transaction (AccountID, TransactionType, Amount, TransactionDate) VALUES (%s, %s, %s, %s)", (account_info[0], 'withdraw', amount, pst_now))
                            action_cursor.execute("COMMIT")
                            self.connection.commit()
                            print("Withdrawal successful.")
                        except Exception as e:
                            self.connection.rollback()
                            print("Error occurred during withdrawal. Rolling back changes.")
                            print("Error:", e)
            else:
                print("Withdrawal canceled by the user.")
        else:
            print(f"No {account_type} account found for the provided User ID.")

    def transfer_within_accounts(self, sender_id, sender_account_type, recipient_account_type, amount):
        with self.connection.cursor() as sender_cursor:
            sender_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {sender_id} AND AccountType = '{sender_account_type}'")
            sender_account = sender_cursor.fetchone()

        with self.connection.cursor() as recipient_cursor:
            recipient_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {sender_id} AND AccountType = '{recipient_account_type}'")
            recipient_account = recipient_cursor.fetchone()

        if sender_account and recipient_account:
            sender_balance = sender_account[1]

            confirm = input(f"Are you sure you want to transfer ${amount} from your {sender_account_type} account to your {recipient_account_type} account? (Yes/No): ")
            if confirm.lower() == 'yes':
                if amount > sender_balance or amount <= 0:
                    print("Transfer amount is invalid. Transaction cancelled.")
                else:
                    with self.connection.cursor() as action_cursor:
                        action_cursor.execute("COMMIT")
                        action_cursor.fetchall()
                        action_cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
                        action_cursor.execute("START TRANSACTION")
                        action_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {sender_id} AND AccountType = '{sender_account_type}'")
                        sender_account = action_cursor.fetchone()
                        action_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {sender_id} AND AccountType = '{recipient_account_type}'")
                        recipient_account = action_cursor.fetchone()
                        try:
                            new_sender_balance = sender_balance - amount
                            action_cursor.execute(f"UPDATE Account SET CurrentBalance = {new_sender_balance} WHERE AccountID = {sender_account[0]}")
                            pst_now = datetime.now(self.pst)
                            action_cursor.execute("INSERT INTO Transaction (AccountID, TransactionType, Amount, TransactionDate, TransferAccountID) VALUES (%s, %s, %s, %s , %s)", (sender_account[0], 'transfer', amount, pst_now, recipient_account[0]))
                            new_recipient_balance = recipient_account[1] + amount
                            action_cursor.execute(f"UPDATE Account SET CurrentBalance = {new_recipient_balance} WHERE AccountID = {recipient_account[0]}")
                            action_cursor.execute("COMMIT")
                            self.connection.commit()
                            print("Internal transfer successful.")
                        except Exception as e:
                            self.connection.rollback()
                            print("Error occurred during internal transfer. Rolling back changes.")
                            print("Error:", e)
            else:
                print("Internal transfer canceled by the user.")
        else:
            print("One or both accounts not found.")

    def transfer_to_external(self, sender_id, recipient_id, recipient_account_type, amount):
        # Verify sender's account information
        with self.connection.cursor() as sender_cursor:
            sender_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {sender_id}")
            sender_account = sender_cursor.fetchone()

        # Verify recipient's account information
        with self.connection.cursor() as recipient_cursor:
            recipient_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {recipient_id} AND AccountType = '{recipient_account_type}'")
            recipient_account = recipient_cursor.fetchone()

        if sender_account and recipient_account:
            sender_balance = sender_account[1]

            confirm = input(f"Are you sure you want to transfer ${amount} to User ID {recipient_id}? (Yes/No): ")
            if confirm.lower() == 'yes':
                if amount > sender_balance or amount <= 0 or amount > 5000:
                    print("Transfer amount is invalid. Transaction cancelled.")
                else:
                    with self.connection.cursor() as action_cursor:
                        action_cursor.execute("COMMIT")
                        action_cursor.fetchall()
                        action_cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
                        action_cursor.execute("START TRANSACTION")
                        action_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {sender_id}")
                        sender_account = action_cursor.fetchone()
                        action_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {recipient_id} AND AccountType = '{recipient_account_type}'")
                        recipient_account = action_cursor.fetchone()
                        try:
                            new_sender_balance = sender_balance - amount
                            action_cursor.execute(f"UPDATE Account SET CurrentBalance = {new_sender_balance} WHERE AccountID = {sender_account[0]}")
                            pst_now = datetime.now(self.pst)
                            action_cursor.execute("INSERT INTO Transaction (AccountID, TransactionType, Amount, TransactionDate, TransferAccountID) VALUES (%s, %s, %s, %s ,%s )", (sender_account[0], 'Send', amount, pst_now, recipient_account[0]))
                            action_cursor.execute("INSERT INTO Transaction (AccountID, TransactionType, Amount, TransactionDate, TransferAccountID) VALUES (%s, %s, %s, %s ,%s )", (recipient_account[0], 'Receive', amount, pst_now, sender_account[0]))
                            new_recipient_balance = recipient_account[1] + amount
                            action_cursor.execute(f"UPDATE Account SET CurrentBalance = {new_recipient_balance} WHERE AccountID = {recipient_account[0]}")
                            action_cursor.execute("COMMIT")
                            self.connection.commit()
                            print("External transfer successful.")
                        except Exception as e:
                            self.connection.rollback()
                            print("Error occurred during external transfer. Rolling back changes.")
                            print("Error:", e)
            else:
                print("External transfer canceled by the user.")
        else:
            print("One or both users don't have an account.")

    def banking_transactions(self, action, user_id):
        with self.connection.cursor() as sender_cursor:
            sender_cursor.execute(f"SET AUTOCOMMIT=0;")
            sender_account = sender_cursor.fetchall()

        if action == 'deposit':
            account_type = input("Enter Account Type (e.g., checking, savings): ").lower()
            self.deposit_funds(user_id, account_type)
        elif action == 'withdraw':
            account_type = input("Enter Account Type (e.g., checking, savings): ").lower()
            self.withdraw_funds(user_id, account_type)
        elif action == 'transfer':
            within_or_external = input("Enter transfer type (within/external): ").lower()
            with self.connection.cursor() as sender_cursor:
                sender_cursor.execute(f"SELECT AccountID, CurrentBalance FROM Account WHERE PersonID = {user_id}")
                sender_account = sender_cursor.fetchall()
            if within_or_external == 'within':
                if len(sender_account) == 1:
                    print('You only have one account. Could not make a transfer')
                else:
                    from_account_type = input("Enter Account Type to transfer from (e.g., checking, savings): ").lower()
                    to_account_type = input("Enter Account Type to transfer to (e.g., checking, savings): ").lower()
                    amount = float(input("Enter transfer amount: "))
                    # Process transfer between user's accounts
                    self.transfer_within_accounts(user_id, from_account_type, to_account_type, amount)
            elif within_or_external == 'external':
                recipient_account = str(input("Enter Recipient's Account: "))
                with self.connection.cursor() as recipient_cursor:
                    recipient_cursor.execute(f"SELECT AccountID, AccountType FROM Account WHERE AccountNumber = '{recipient_account}'")
                    recipient_account = recipient_cursor.fetchone()
                recipient_id = recipient_account[0]
                recipient_account_type = recipient_account[1]
                amount = float(input("Enter transfer amount: "))
                # Process transfer to different user's accounts
                self.transfer_to_external(user_id, recipient_id, recipient_account_type, amount)
            else:
                print("Invalid transfer type. Please enter 'within' or 'external'.")

    def show_user_transactions(self, email):
        try:
            with self.connection.cursor() as cursor:
                req = input("How many days of transactions do you want to view?")
                query = f"""
                    SELECT T.TransactionDate, A.AccountType, T.TransactionType, CONCAT('$', T.Amount) AS Amount,
                            A1.AccountNumber, P1.Email
                    FROM Transaction T
                    LEFT JOIN Account A ON T.AccountID = A.AccountID
                    LEFT JOIN Person P ON A.PersonID = P.PersonID
                    LEFT JOIN Account A1 ON T.TransferAccountID = A1.AccountID
                    LEFT JOIN Person P1 ON A1.PersonID = P1.PersonID
                    WHERE P.Email = '{email}'
                    ORDER BY T.TransactionDate DESC LIMIT {req};
                """

                cursor.execute(query)
                info = cursor.fetchall()
                if len(info) == 0:
                    print("No transactions found.")
                else:
                    print('--------------- Transaction ------------------ ')
                    df = pd.DataFrame(info, columns=['Date', 'Account', 'Type', 'Amount', 'From Account Number', 'From Email'])
                    df.Type = df.Type.str.capitalize()
                    print(df.to_string(index=False))

        except Exception as e:
            print("Transaction error:", e)

    def show_user_balance(self, email):
        query = f"""
            SELECT A.AccountNumber, A.AccountType, A.CurrentBalance
            FROM Account A
            JOIN Person P ON A.PersonID = P.PersonID
            WHERE P.Email = '{email}';
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                info_account = cursor.fetchall()
                #print(info_account)
                df_acc = pd.DataFrame(info_account, columns=['Account Number', 'Account Type', 'Current Balance'])
                print(df_acc)

        except Exception as e:
            print("Error fetching balance:", e)

    def update_profile(self, email):
        query = f"""
            SELECT Name, DOB, Email, PhoneNumber, Address
            FROM Person P 
            WHERE P.Email = '{email}';
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            info = cursor.fetchall()
            df = pd.DataFrame(info, columns=['Name', 'Date of Birth', 'Email', 'Phone Number', 'Address'])
            print('Name         : ', df['Name'].to_string(index=False))
            print('Date of Birth: ', df['Date of Birth'].to_string(index=False))
            print('Email        : ', df['Email'].to_string(index=False))
            print('Phone Number : ', df['Phone Number'].to_string(index=False))
            print('Address      : ', df['Address'].to_string(index=False))

        print('What information would you like to update? ')
        print('1. Email')
        print('2. Password')
        print('3. Phone Number')
        print('4. Address')
        print('5. Quit')

        action = int(input("Please enter option number: "))

        while action:
            with self.connection.cursor() as cursor:
                try:
                    if action == 1:
                        new_email = input("Enter new E-Mail: ").lower()

                        if not self.is_valid_email(new_email):
                            print("Invalid email format. Update canceled.")
                            break

                        cursor.execute("UPDATE Person SET Email = %s WHERE Email = %s", (new_email, email))
                        cursor.execute("UPDATE UserCredentials SET Email = %s WHERE Email = %s", (new_email, email))
                    elif action == 3:
                        new_phone = input("Enter new phone number (e.g., 1-245-829-0562): ")

                        if not self.is_valid_phone_number(new_phone):
                            print("Invalid phone number format. Update canceled.")
                            break
                        cursor.execute("UPDATE Person SET PhoneNumber = %s WHERE Email = %s", (new_phone, email))
                    elif action == 2:
                        new_password = input("Enter new password: ")
                        hashed_password = self.hash_password(new_password)
                        cursor.execute("UPDATE UserCredentials SET Password = %s WHERE Email = %s", (hashed_password, email))
                    elif action == 4:
                        new_address = input("Enter new address: ")
                        cursor.execute("UPDATE Person SET Address = %s WHERE Email = %s", (new_address, email))
                    elif action == 5:
                        break
                    else:
                        print("Invalid Option.")
                        break

                    print('Updated successfully!')
                    self.connection.commit()

                except Exception as e:
                    self.connection.rollback()
                    print("Update error:", e)

            print('What information would you like to update? ')
            print('1. Email')
            print('2. Password')
            print('3. Phone Number')
            print('4. Address')
            print('5. Quit')
            action = int(input("Please enter option number: "))

    def is_valid_email(self, email):
        # Regular expression for a simple email format check
        email_regex = r'^\S+@\S+\.\S+$'
        return re.match(email_regex, email) is not None

    def is_valid_phone_number(self, phone_number):
        # Regular expression for a simple phone number format check
        phone_regex = r'^\d{1,3}-\d{1,3}-\d{1,4}-\d{1,4}$'
        return re.match(phone_regex, phone_number) is not None

    def login(self):
        while True:
            req = input("Welcome, please type 'login' or 'quit' to end: ").lower()
            while req not in ['login', 'quit']:
                print("Invalid input.")
                req = input("Please enter 'login' or 'quit': ").lower()

            if req == 'quit':
                print("Exiting the system.")
                break

            elif req == 'login':
                email = input("Enter your email: ")
                password = input("Enter your password: ")

                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM UserCredentials WHERE Email = %s", email)
                    user = cursor.fetchone()

                    if user and user[2] == hashed_password:
                        print("Login successful!")

                        # Show user balance
                        self.show_user_balance(email)

                        while True:
                            # Show user transactions
                            print('***********************************')
                            print('Options: ')
                            print('1. View Transaction')
                            print('2. Deposit')
                            print('3. Withdraw')
                            print('4. Transfer')
                            print('5. Update Profile')
                            print('6. Logout')
                            print('***********************************')

                            action = int(input("Please enter option number: "))

                            if action == 6:
                                print("Logout successful!")
                                break
                            elif action == 5:
                                self.update_profile(email)
                                continue_action = input("Do you want to continue? (yes/no): ").lower()
                                if continue_action == 'no':
                                    print("Logout successful!")
                                    break
                            elif action == 1:
                                self.show_user_transactions(email)
                                continue_action = input("Do you want to continue? (yes/no): ").lower()
                                if continue_action == 'no':
                                    print("Logout successful!")
                                    break
                            elif action == 2:
                                self.banking_transactions('deposit', user[0])
                                print('-----------------------------------')
                                # Show user current account balance
                                self.show_user_balance(email)

                                continue_action = input("Do you want to continue? (yes/no): ").lower()
                                if continue_action == 'no':
                                    print("Logout successful!")
                                    break
                            elif action == 3:
                                self.banking_transactions('withdraw', user[0])
                                print('-----------------------------------')
                                # Show user current account balance
                                self.show_user_balance(email)

                                continue_action = input("Do you want to continue? (yes/no): ").lower()
                                if continue_action == 'no':
                                    print("Logout successful!")
                                    break
                            elif action == 4:
                                self.banking_transactions('transfer', user[0])
                                print('-----------------------------------')
                                # Show user current account balance
                                self.show_user_balance(email)

                                continue_action = input("Do you want to continue? (yes/no): ").lower()
                                if continue_action == 'no':
                                    print("Logout successful!")
                                    break
                            else:
                                print("Invalid action. Please enter 'deposit', 'withdraw', 'transfer', or 'quit'.")
                    else:
                        print("Invalid email or password. Please try again.")
connection = pymysql.connect(
    host='34.94.165.202',
    user='root',  # enter your username
    password='thereisnopassword',  # enter your password 
    database='banking_system'
)             
banking_system = BankingSystem(
    host='34.94.165.202',
    user='root',
    password='thereisnopassword',
    database='banking_system')













































# 1. Email: sjsu@sjsu.edu  
# Pass : hello 
# 2. Email: cras.eget@protonmail.edu  
# Pass: m8dnpCi34h
# 
# 

# # DEMO

# In[5]:


banking_system.login()


# In[ ]:





# In[ ]:





# In[ ]:




