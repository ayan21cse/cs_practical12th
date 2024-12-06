-- Step 1: Create the database
CREATE DATABASE bank290;

-- Step 2: Use the database
USE bank290;

-- Step 3: Create the accounts table with additional columns for father's name, mother's name, phone, and password
CREATE TABLE accounts (
    account_no INT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender CHAR(1),
    address VARCHAR(255),
    father_name VARCHAR(255),
    mother_name VARCHAR(255),
    phone VARCHAR(10),
    balance FLOAT,
    password VARCHAR(255)
);

-- Step 4: Create the transactions table with a reference to the account_no and account_name
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_no INT,
    account_name VARCHAR(255),
    type VARCHAR(50),
    amount FLOAT,
    date_time DATETIME,
    FOREIGN KEY (account_no) REFERENCES accounts(account_no)
);

-- Step 5: Query to display all data from the accounts table
SELECT * FROM accounts;

-- Step 6: Query to display all data from the transactions table
SELECT * FROM transactions;
