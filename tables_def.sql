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
ALTER TABLE Person
ADD CONSTRAINT unique_email UNIQUE (Email);
CREATE INDEX idx_Transaction_TransactionDate ON Transaction(TransactionDate);
/*
SELECT * FROM UserCredentials order by PersonID DESC;
SELECT * FROM Person order by PersonID DESC;
SELECT * FROM Account order by AccountID DESC;
SELECT * FROM Employee;
SELECT * FROM Branch;
SELECT * FROM Transaction ORDER BY TransactionID DESC;
-- WHERE Amount = 8;

SELECT B.BranchName, COUNT(A.AccountID) AS TotalAccounts
FROM Account A
JOIN Person P ON A.PersonID = P.PersonID
JOIN Employee E ON P.PersonID = E.PersonID
JOIN Branch B ON E.BranchID = B.BranchID
GROUP BY B.BranchName;

SELECT t.TransactionID, t.TransactionType, 
        t.Amount, t.TransactionDate, 
        t.TransferAccountID,  a.AccountID, 
        a.AccountNumber, a.AccountType
FROM Transaction t INNER JOIN 
     Account a ON t.AccountID = a.Account;

SELECT t.TransactionID, t.TransactionType, 
       t.Amount, t.TransactionDate, 
       t.TransferAccountID, a.AccountID, 
       a.AccountNumber, a.AccountType
FROM Account a INNER JOIN 
     Transaction t ON t.AccountID = a.AccountID;
     
SELECT email, COUNT(email)
FROM Person
GROUP BY email
HAVING COUNT(email) > 1;

SELECT *
FROM Person
WHERE DOB > '1980-01-01';

SELECT t.TransactionID, t.TransactionType, t.Amount, t.TransactionDate, 
       t.TransferAccountID, a.AccountID, a.AccountNumber, a.AccountType
FROM Transaction t 
INNER JOIN Account a ON t.AccountID = a.AccountID
WHERE t.TransactionDate >=  time  ;
 -- NOW() - INTERVAL 90 DAY
 
*/
 
 
 
 
 
 
 
 
 


