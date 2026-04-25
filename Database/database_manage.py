import sqlite3


def create_new_transaction_table():
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()
    
    # Query the master table to check if the transaction table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master;")
    master_table = res.fetchone()
    # check first to ensure the master table isn't empty and then test if the table is already created
    if master_table is not None and 'transactions' in master_table:
        cursor.close()
        return 
    # if the table isn't already in the DB, create it
    cursor.execute("""CREATE TABLE transactions 
                   (id INTEGER PRIMARY KEY, 
                    transaction_date TEXT,
                    description TEXT, 
                    amount REAL,
                    count INTEGER DEFAULT 0,
                    UNIQUE(transaction_date, description, amount, count));""") 
    cursor.close()


# Need to determine how to load / check for duplicate - what kind of field do I need
def insert_transactions_from_file(transaction_list):
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()
    # Use 'executemany' to perform repeated SQL statements
    # Insert Null as first value passed it - this will allow SQLite to autoincrement the primary key
    #cursor.executemany("""INSERT INTO transactions VALUES(NULL, ?, ?, ?);""", transaction_list)
    transactions_to_review = []
    for tranx in transaction_list:
        try:
            cursor.execute("INSERT INTO transactions (transaction_date, description, amount) VALUES(?, ?, ?)", (tranx[0], tranx[1], tranx[2]))
        except sqlite3.Error as er:
            if er.sqlite_errorcode == 2067:
                # Have user review the transaction and reenter it into the DB
                print(tranx)
                decision = input("(D)uplicate or (V)alid Transaction: ")
                if decision.lower() == 'd':
                    #Ignore transaction and move on if duplicate
                    continue
                else:
                    # Re-enter it into the database - need to detemrine how to modify it for entry so constraint isn't violated
                    # maybe can extract the duplicate item from database, keep a map of the count of how many times we've encountered it and
                    # update that account as we good - could keep a new column in the DB for duplicate counts
                    transactions_to_review.append(tranx)
            else:
                print()
    print(transactions_to_review)
            #print(er.sqlite_errorname)
            #print(er.sqlite_errorcode)

    # Going to have to test for duplicates as it enters the transactions into the DB
    # Will use UNIQUE constrain for all fields and keep track of the number of duplicates we encounter
    # Append those ID's to a list and then we can manually determine which ones are duplicates when done
    # and set them to delete
    # Will I need to insert each individual line and check for error?


    con.commit()




# All Transactions will be in one table - bank, CC all - need to ensure all fields are all encompassing