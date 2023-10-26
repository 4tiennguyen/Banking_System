
CREATE TABLE Person (
	PersonID Integer NOT NULL AUTO_INCREMENT,
    `Name` Varchar(50)  NOT NULL,
    DOB DateTime NOT NULL,
    Email  Varchar(50) NOT NULL,
    PhoneNumber  Varchar(20) NOT NULL,
    Address  Varchar(100) NOT NULL,
    Primary key (PersonID)
    );
    
CREATE TABLE Account (
    AccountID INT PRIMARY KEY,
    AccountNumber VARCHAR(20) UNIQUE,
    AccountType VARCHAR(50),
    CurrentBalance FLOAT,
    InterestRate FLOAT,
    DateOpen DATE,
    DateClose DATE,
    AccountStatus VARCHAR(50),
    PersonID INT,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
);

CREATE TABLE Transaction (
    TransactionID INT PRIMARY KEY,
    AccountID INT,
    TransactionType VARCHAR(50),
    Amount FLOAT,
    TransactionDate DATETIME,
    FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
);

CREATE TABLE Branch (
    BranchID INT PRIMARY KEY,
    BranchName VARCHAR(100),
    Address VARCHAR(100),
    PhoneNumber Varchar(20)
);

CREATE TABLE Employee(
	EmployeeID INT PRIMARY KEY,
    Position VARCHAR(50),
    PersonID INT NOT NULl,
    BranchID INT NOT NULL,
    FOREIGN KEY (BranchID) REFERENCES Branch(BranchID),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
);