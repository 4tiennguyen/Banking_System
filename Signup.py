#!/usr/bin/env python
# coding: utf-8

# In[5]:


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
from User import User
pst = pytz.timezone('America/Los_Angeles')
pd.set_option('display.max_columns', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)


# In[21]:


print("***************************************************************")
print("Welcome to the Signup Process")
class BankSignup:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def signup(self):
        

        # Get employee code
        employee_code = input("Enter your Employee Code: ")

        try:
            employee_id, branch_id = employee_code[:-1], employee_code[-1]

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Employee WHERE EmployeeID = %s AND BranchID = %s", (employee_id, branch_id))
                employee = cursor.fetchone()

                if employee and employee[1] == 'Teller':
                    while True:
                        try:
                            
                            new_user = User.create_user(self.connection, cursor)
                            while True:
                                confirm_edit = input("Do you want to confirm this information? (yes/no): ").lower()
                                if confirm_edit == "no":
                                    new_user.edit_user(self.connection, cursor)
                                else:
                                    break
                            new_user.add_user_to_database(self.connection, cursor)

                            signup_another = input("Do you want to sign up another user? (yes/no): ").lower()
                            if signup_another != 'yes':
                                break

                        except Exception as e:
                            self.connection.rollback()
                            print("Signup error:", e)
                            break

                else:
                    print("Invalid employee code or position. Only Tellers are allowed to sign up new users.")

        except Exception as e:
            self.connection.rollback()
            print("Unexpected error:", e)

# Example usage:
bank_signup = BankSignup(
    host='34.94.165.202',
    user='root',
    password='thereisnopassword',
    database='banking_system'
)

bank_signup.signup()


# In[ ]:




