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


# In[52]:


import pymysql
import hashlib
import random
import pandas as pd
from datetime import datetime, timezone, timedelta

class AccountOperations:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def generate_account_number(self):
        with self.connection.cursor() as cursor:
            while True:
                account_number = ''.join(str(random.randint(0, 9)) for _ in range(9))

                cursor.execute("SELECT AccountNumber FROM `Account` WHERE AccountNumber = %s", account_number)
                existing_account = cursor.fetchone()

                if not existing_account:
                    return account_number

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def create_account(self):
        try:
            teller_code = input("Enter your Employee Code: ")
            employee_id, branch_id = teller_code[:-1], teller_code[-1]

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Employee WHERE EmployeeID = %s AND BranchID = %s AND Position = 'Teller'",
                               (employee_id, branch_id))
                teller = cursor.fetchone()

                if not teller:
                    print("Invalid Teller code. Only Tellers can create accounts.")
                    return

                user_email = input("Enter user's email: ").lower()
                user_password = input("Enter user's password: ")

                cursor.execute("SELECT PersonID FROM UserCredentials WHERE Email = %s AND Password = %s",
                               (user_email, self.hash_password(user_password)))
                user = cursor.fetchone()[0]

                if not user:
                    print("Invalid user credentials.")
                    return

                cursor.execute("SELECT AccountType FROM Account WHERE PersonID = %s", user)
                existing_accounts = cursor.fetchall()

                
                existing_accounts_df = pd.DataFrame(existing_accounts, columns=['AccountType'])
                print("Existing Accounts:")
                if len(existing_accounts_df) == 0:
                    print('You do not have any account')
                else:
                    print(existing_accounts_df)
                
                if len(existing_accounts) >= 2:
                    print("User can have only one checking account and one savings account.")
                    return


                if existing_accounts:
                    if 'checking' in existing_accounts_df['AccountType'].values and 'savings' in existing_accounts_df['AccountType'].values:
                        print("User already has both checking and savings accounts. Cannot create more accounts.")
                        return

                    if 'Checking' in existing_accounts_df['AccountType'].values:
                        account_type = input("Please type 'savings' to confirm you want to create a Savings Account: ").lower()
                    elif 'Savings'.upper() in existing_accounts_df['AccountType'].values:
                        account_type = input("Please type 'checking' to confirm you want to create a Checking Account: ").lower()

                else:
                    account_type = input("Create an account (checking/savings): ").lower()

                if account_type not in ['checking', 'savings']:
                    print("Invalid account type. Please choose either 'checking' or 'savings'.")
                    return

                cursor.execute("SELECT MAX(AccountID) AS HighestAccountID FROM Account")
                highest_account_id = cursor.fetchone()[0]
                new_account_id = highest_account_id + 1

                account_number = self.generate_account_number()

                initial_deposit = float(input("Enter the initial deposit amount (up to $2000): "))

                if initial_deposit > 2000:
                    print("Initial deposit cannot exceed $2000. Please enter a valid amount.")
                    return

                pst_now = datetime.now(timezone(timedelta(hours=-8)))

                cursor.execute("INSERT INTO `Account` (AccountID, AccountNumber, AccountType, CurrentBalance, DateOpen, AccountStatus, PersonID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                               (new_account_id, account_number, account_type.capitalize(), initial_deposit, pst_now, 'Active', user))
                cursor.execute("INSERT INTO Transaction (AccountID, TransactionType, Amount, TransactionDate) VALUES (%s, %s, %s, %s)",
                               (new_account_id, 'deposit', initial_deposit, pst_now))

                self.connection.commit()
                print(f"{account_type.capitalize()} account creation successful!")

        except Exception as e:
            self.connection.rollback()
            print("Account creation error:", e)

#
createAccount = AccountOperations(
    host='34.94.165.202',
    user='root',
    password='thereisnopassword',
    database='banking_system'
)

createAccount.create_account()


# In[ ]:




