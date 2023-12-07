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
class User:
    def __init__(self, name, dob, email, phone_number, address, hashed_password):
        self.name = name
        self.dob = dob
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.hashed_password = hashed_password
    def set_person_id(self, pid):
        self._person_id = pid
    @classmethod
    def hash_password(cls, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    @classmethod
    def create_user(cls, connection, cursor):
        # Get user details
        name = input("Enter the new user's full name: ")
        dob = input("Enter the new user's date of birth (YYYY-MM-DD): ")
        email = input("Enter the new user's email: ").lower()

        cursor.execute("SELECT * FROM Person WHERE Email = %s", email)
        existing_user = cursor.fetchone()

        if existing_user:
            print("Email already exists. Please choose a different email.")
            return

        phone_number = input("Enter the new user's phone number: ")
        address = input("Enter the new user's address: ")
        password = input("Enter the new user's password: ")

        hashed_password = User.hash_password(password)
        user_info_table = pd.DataFrame(
            {
                'Name': [name],
                'Date of Birth': [dob],
                'Email': [email],
                'Phone Number': [phone_number],
                'Address': [address],
            }
        )
        print("Please review the entered information:")
        print(user_info_table)
        return User(name, dob, email, phone_number, address, hashed_password)
    def edit_user(self, connection, cursor):
        edit_field = input("Which information would you like to edit? "
                           "(name/date of birth/email/phone number/address/password): ").lower()
        if edit_field == 'name':
            self.name = input("Enter the corrected full name: ")
        elif edit_field == 'date of birth':
            self.dob = input("Enter the corrected date of birth (YYYY-MM-DD): ")
        elif edit_field == 'email':
            email = input("Enter the corrected email: ").lower()
            cursor.execute("SELECT * FROM Person WHERE Email = %s", email)
            existing_user = cursor.fetchone()
            if existing_user:
                print("Email already exists. Update canceled.")
                return
            else:
                self.email = email
        elif edit_field == 'phone number':
            self.phone_number = input("Enter the corrected phone number: ")
        elif edit_field == 'address':
            self.address = input("Enter the corrected address: ")
        elif edit_field == 'password':
            password = input("Enter the corrected password: ")
            self.hashed_password = User.hash_password(password)
    def add_user_to_database(self, connection, cursor):
        cursor.execute("INSERT INTO Person (`Name`, DOB, Email, PhoneNumber, Address) VALUES (%s, %s, %s, %s, %s)",
                       (self.name, self.dob, self.email, self.phone_number, self.address))
        person_id = cursor.lastrowid
        self.set_person_id(person_id)

        cursor.execute("INSERT INTO UserCredentials (PersonID, Email, Password) VALUES (%s, %s, %s)",
                       (self._person_id, self.email, self.hashed_password))

        connection.commit()
        print("Signup successful!")