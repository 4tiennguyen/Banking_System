DROP TABLE IF EXISTS `Transaction`;
DROP TABLE IF EXISTS `Account`	;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Branch;
DROP TABLE IF EXISTS UserCredentials;


CREATE TABLE UserCredentials (
    PersonID INTEGER NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Password VARCHAR(100) NOT NULL,
    PRIMARY KEY (PersonID),
    UNIQUE (Email)
);

CREATE TABLE Person (
	PersonID Integer NOT NULL AUTO_INCREMENT,
    `Name` Varchar(50)  NOT NULL,
    DOB DateTime NOT NULL,
    Email  Varchar(50) NOT NULL,
    PhoneNumber  Varchar(20) NOT NULL,
    Address  Varchar(100) NOT NULL,
    Primary key (PersonID)
    );
    
CREATE TABLE `Account` (
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

CREATE TABLE `Transaction` (
    TransactionID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    AccountID INT,
    TransactionType VARCHAR(50),
    Amount FLOAT,
    TransactionDate DATETIME,
    TransferAccountID INT,
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


SELECT * FROM UserCredentials;
SELECT * FROM Person;
SELECT * FROM Account;
SELECT * FROM Employee;
SELECT * FROM Branch;
SELECT * FROM Transaction ORDER BY TransactionID DESC;
-- WHERE Amount = 8;

SELECT AccountID, AccountType FROM Account WHERE AccountNumber = '43136785'; 