import sqlite3
import vendor_trie
# Application needs to create database if one doesn't exist



# -------------------------- Table Creation Functions ------------------------------------
# Will need ability to add in card name and tie to user - will do
def create_new_transaction_table():
    # Change to absolute path instead of relative path
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()


    # Query the master table to check if the transaction table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Transactions';")
    master_table = res.fetchone()

    # check each returned table to see if Transactions is already included
    if 'Transactions' in master_table:
        con.close()
        return 
    # if the table isn't already in the DB, create it
    cursor.execute("""CREATE TABLE Transactions 
                (id INTEGER PRIMARY KEY, 
                    card_issuer TEXT,
                    transaction_date TEXT,
                    description TEXT, 
                    amount REAL,
                    count INTEGER DEFAULT 0,
                    UNIQUE(transaction_date, description, amount, count));""") 
    con.close()


def create_new_vendor_table():
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()

    # Query the master table to check if the vendor table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendors';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if 'Vendors' in master_table:
        con.close()
        return 
    # if the table isn't already in the DB, create it
    cursor.execute("""CREATE TABLE Vendors 
                (vendor_id INTEGER PRIMARY KEY,
                 vendor_name TEXT,
                 type TEXT,
                 UNIQUE(vendor_name));""") 
    
    # Query the master table to check if the Vendor_Aliases table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendor_Alias';")
    master_table = res.fetchone()
    # check each returned table to see if Vendor_Alias is already included
    if 'Vendor_Alias' in master_table:
        con.close()
        return 
    cursor.execute("""CREATE TABLE Vendor_Alias 
                (alias_id INTEGER PRIMARY KEY,
                 vendor_alias TEXT,
                 vendor_id INTEGER,
                 FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id),
                 UNIQUE(vendor_alias));    
                 """) 
    con.close()
    


def get_vendors():
    # extract all vendors from DB
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()

    # Query the master table to check if the vendor table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendors';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if 'Vendors' in master_table:
        res = cursor.execute("SELECT * FROM Vendors")
        vendors = res.fetchall()
        con.close()
        return vendors
    con.close()
    return "Vendor table does not exist"


def get_vendor_aliases():
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()

    # Query the master table to check if the vendor table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendor_Alias';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if 'Vendor_Alias' in master_table:
        res = cursor.execute("SELECT vendor_alias, vendor_id FROM Vendor_Alias")
        vendor_aliases = res.fetchall()
        con.close()
        return vendor_aliases
    con.close()
    return "Vendor Alias table does not exist"




# Need to determine how to load / check for duplicate - what kind of field do I need
def insert_transactions_from_file(transaction_list, vendor_trie, vendor_aliases):
    # function handles entering transactions, vendors and vendor aliases
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()
    # Use 'executemany' to perform repeated SQL statements
    # Insert Null as first value passed it - this will allow SQLite to autoincrement the primary key
    #cursor.executemany("""INSERT INTO transactions VALUES(NULL, ?, ?, ?);""", transaction_list)

    # Place all vendor names encountered from the transaction - this will subsequently be added to the vendor_alias table
    # use a set for quicker access time
    transaction_vendor_aliases = set()
    
    transactions_to_review = []
    for tranx in transaction_list:

        # This actually has to happen before loading the transactions so we can associate the transaction with the vendor
        # Now that each transaction is loaded to the database, we need to load the vendor info into the database
        # We have all of the new alias names from the loan. we need to link them up to their identifying name
        # Ideally, I'd like to show the user a list of known vendor names and have them associate the alias with that vendor. 
        
        # Initial steps
        # before we load the transactions:
        # 1. Query the database to obtain all of the current known aliases (we'll have all associated vendor ID's) - place these in a dictionary with their name as the key and vendor ID as the value
        # 2. Load all known vendors into the trie (we'll populate it initially from db) - we'll have it's vendor id within the trie nodes at the target ending node
        # 3. When the transaction load runs, we'll check within the vendor alias dictionary to see if it has already been seen.if the alias already exists, I want it to auto associate with the vendor id, and continues on. If it hasn't, we'll prompt the user to select which vendor it belongs to
        # we can print out the available vendors for now (later will be a list they can review) and then using the trie, the user can input (with autocomplete/suggest) - if the option doesn't exist, the user can provide to create a new vendor

        if tranx[2] not in transaction_vendor_aliases:
            #vendors_loaded.append(tranx[2])
            transaction_vendor_aliases.add(tranx[2])

        # After we've identified the appropriate vendor, load the transaction the the DB
        try:
            # In order to use default values, we have to specify the columns we're inserting into in SQL
            cursor.execute("INSERT INTO Transactions (card_issuer, transaction_date, description, amount) VALUES(?, ?, ?, ?);", (tranx[0], tranx[1], tranx[2], tranx[3]))
        except sqlite3.Error as er:
            # Check for specific SQL error code for the unique constraint being violated
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
                    # update that account as we go - could keep a new column in the DB for duplicate counts
                    # query all records that are 'duplicates' then find the current max value for count of these records and then increment by 1 for new record
                    res = cursor.execute("SELECT count FROM transactions WHERE transaction_date=? AND description=? AND amount=?", (tranx[1], tranx[2], tranx[3]))
                    duplicates = res.fetchall()
                    max_count = max(duplicates)[0]
                    try:
                        cursor.execute("INSERT INTO transactions (card_issuer, transaction_date, description, amount, count) VALUES(?, ?, ?, ?, ?)", (tranx[0], tranx[1], tranx[2],tranx[3], max_count + 1))
                    except sqlite3.Error:
                        # Need to determine how to gracefull hanndled the errors
                        print("Database Load Error Encountered")
            else:
                # Need to determine how to gracefull hanndled the errors
                print("Database Load Error Encountered")
            #print(er.sqlite_errorname)
            #print(er.sqlite_errorcode)

    for vendor_alias in transaction_vendor_aliases:
        # check if the alias is already in the dictionary, we have the vendor ID and can simply add to the alias table
        #  if not, it needs to be added and the user needs to determine the apprpriate vendor 
            # user can view current known vendors via the trie, if there isn't a match, user can add new vendor to DB
        pass



    # Going to have to test for duplicates as it enters the transactions into the DB
    # Will use UNIQUE constrain for all fields and keep track of the number of duplicates we encounter
    # Append those ID's to a list and then we can manually determine which ones are duplicates when done
    # and set them to delete
    # Will I need to insert each individual line and check for error?
    







    con.commit()




# All Transactions will be in one table - bank, CC all - need to ensure all fields are all encompassing