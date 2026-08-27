import sqlite3
# Application needs to create database if one doesn't exist



# -------------------------- Table Creation Functions ------------------------------------

def create_new_vendor_table():
    """ Tests if vendor and related alias tables already exist in the database and, if not, creates the tables """

    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()

    # Query the master table to check if the vendor table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendors';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if master_table is not None and 'Vendors' in master_table:
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
    if master_table is not None and 'Vendor_Alias' in master_table:
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



    # TODO: Will need ability to add in card name and tie to user - will do
def create_new_transaction_table():
    """ Tests if transaction table already exists in the database and, if not, creates the table """

    # Change to absolute path instead of relative path
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()


    # Query the master table to check if the transaction table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Transactions';")
    master_table = res.fetchone()

    # Check each returned table to see if Transactions is already included
    if master_table is not None and 'Transactions' in master_table:
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
                    vendor_id INTEGER,
                    FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id),
                    UNIQUE(transaction_date, description, amount, count));""") 
    con.close()
    


# -------------------------- Data Query Functions ------------------------------------

def get_vendors():
    """ Returns a list of tuples containing all known vendors (ID, Name and Category) from DB """
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()

    # Query the master table to check if the vendor table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendors';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if master_table is not None and 'Vendors' in master_table:
        res = cursor.execute("SELECT * FROM Vendors")
        vendors = res.fetchall()
        con.close()
        return vendors
    con.close()
    return "Vendor table does not exist"


def get_vendor_aliases():
    """ Returns a dictionary of all known vendors aliases (alias name, vendor_id) from DB """
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()

    # Query the master table to check if the vendor table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendor_Alias';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if master_table is not None and 'Vendor_Alias' in master_table:
        res = cursor.execute("SELECT vendor_alias, vendor_id FROM Vendor_Alias")
        vendor_aliases = res.fetchall()
        con.close()
        alias_map = {alias[0]: alias[1] for alias in vendor_aliases}
        return alias_map
    
    con.close()
    return "Vendor Alias table does not exist"


def get_vendor_types():
    """ Returns a lsit of tuples of all known   from DB """
    # TODO: need to clean this up to remove duplicates (can use a set)

    # extract all vendors from DB
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()

    # Query the master table to check if the vendor table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendors';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if master_table is not None and 'Vendors' in master_table:
        res = cursor.execute("SELECT type FROM Vendors")
        vendors = res.fetchall()
        con.close()
        return vendors
    con.close()
    return "Vendor table does not exist"


def get_vendor(vendor_name):
    # extract all vendors from DB
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()

    # Query the master table to check if the vendor table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendors';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if master_table is not None and 'Vendors' in master_table:
        # need to add condition if vendor isn't found (try/except)?
        res = cursor.execute("SELECT * FROM Vendors WHERE vendor_name=?;", (vendor_name,))
        vendor = res.fetchall()
        con.close()
        return vendor
    con.close()
    return "Vendor table does not exist"


def get_transactions():
    # extract all vendors from DB
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()

    # Query the master table to check if the vendor table as already been created
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendors';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if master_table is not None and 'Vendors' in master_table:
        # need to add condition if vendor isn't found (try/except)?
        res = cursor.execute("SELECT * FROM Transactions;")
        transactions = res.fetchall()
        con.close()
        return transactions
    con.close()
    return "Transactions table does not exist"





# -------------------------- Data Insert Functions ------------------------------------

def insert_transactions_from_file(transaction_list, vendor_trie, vendor_aliases):
    """ 
    function handles entering transactions, vendors and vendor aliases

    """

    # Determine if Transaction Table exists, if not create it before loading transactions
    create_new_transaction_table()

    
    for tranx in transaction_list:

        # Vendor Determination Portion

        # TODO: going to need a second trie instance for vendor types user can select from
        if tranx[2].lower().strip() not in vendor_aliases:
            print(tranx)
            # prompt user to select or provide a vendor
            vendor_name = input("Provide Vendor Name: ").lower().strip()
            is_word, vendor_id, vendor_type = vendor_trie.search(vendor_name)
            if not is_word:
                # enter both vendor and alias into the database
                vendor_type = input("Provide Vendor Type: ").lower().strip()
                insert_vendor(vendor_name, vendor_type)
                vendor_details = get_vendor(vendor_name)
                vendor_id = vendor_details[0][0]
                vendor_trie.insert(vendor_name, vendor_type, vendor_id)

                # Add new alias to the database
                insert_vendor_alias(tranx[2].lower().strip(), vendor_id)

            # Add new alias to the vendor_alias dictionary with the related vendor number
            vendor_aliases[tranx[2].lower().strip()] = vendor_id
        # Assign the vendor id asigned to the already known alias to the transaction
        else:
            vendor_id = vendor_aliases[tranx[2].lower().strip()]

        # Transaction DB Load Portion

        con = sqlite3.connect('Database/personal_finance_db.db')
        cursor = con.cursor()
        # After we've identified the appropriate vendor, load the transaction the the DB
        try:
            # In order to use default values, we have to specify the columns we're inserting into in SQL
            cursor.execute("INSERT INTO Transactions (card_issuer, transaction_date, description, amount, vendor_id) VALUES(?, ?, ?, ?, ?);", (tranx[0], tranx[1], tranx[2], tranx[3], vendor_id))
        except sqlite3.Error as er:
            # Check for specific SQL error code for the unique constraint being violated
            if er.sqlite_errorcode == 2067:
                # Have user review the transaction and reenter it into the DB if it's a valid duplicate
                print(tranx)
                decision = input("(D)uplicate or (V)alid Transaction: ")
                if decision.lower() == 'd':
                    # TODO:Do I need to commit / close here? Need to think through when to open and close connections appropriately
                    con.commit()
                    con.close()
                    #Ignore transaction and move on if duplicate
                    continue
                else:
                    # Query all records that are 'duplicates' then find the current max value for count of these records and then increment the max value in the 'count' field by 1 for new record
                    res = cursor.execute("SELECT count FROM transactions WHERE transaction_date=? AND description=? AND amount=?", (tranx[1], tranx[2], tranx[3]))
                    duplicates = res.fetchall()
                    # Max compares tuples within the list lexographically to find the largest
                    max_count = max(duplicates)[0]
                    try:
                        cursor.execute("INSERT INTO transactions (card_issuer, transaction_date, description, amount, count, vendor_id) VALUES(?, ?, ?, ?, ?, ?)", (tranx[0], tranx[1], tranx[2],tranx[3], max_count + 1, vendor_id))
                    except sqlite3.Error as er2:
                        # TODO: Need to determine how to gracefully handle the errors
                        print("Database Load Error Encountered")
            else:
                # TODO: Need to determine how to gracefully handle the errors
                print("Database Load Error Encountered")
            #print(er.sqlite_errorname)
            #print(er.sqlite_errorcode)
        con.commit()
        con.close()

    


def insert_vendor(vendor, type, con=None):
    # enter new vendor into DB
    # if we are already provided a DB connection, use the provided connection
    db_con = con
    if db_con is None:
        db_con = sqlite3.connect('Database/personal_finance_db.db')

    cursor = db_con.cursor()
    # Query the master table to ensure vendor table exists
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendors';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if master_table is not None and 'Vendors' in master_table:
        try:
            cursor.execute("INSERT INTO Vendors (vendor_name, type) VALUES (?, ?);", (vendor, type))
        except sqlite3.Error as er:
            # Check for specific SQL error code for the unique constraint being violated
            if er.sqlite_errorcode == 2067:
                print("Vendor already exists in the database")
            else:
                # Need to determine how to gracefull hanndled the errors
                print("Database Load Error Encountered")

    # if we are already provided a DB connection, we don't want to commit / close the connection independently here
    if con is None:
        db_con.commit()
        db_con.close()



def insert_vendor_alias(alias, vendor_id, con=None):
    # enter new vendor alias into DB
    # if we are already provided a DB connection, use the provided connection
    db_con = con
    if db_con is None:
        db_con = sqlite3.connect('Database/personal_finance_db.db')

    cursor = db_con.cursor()
    # Query the master table to ensure vendor table exists
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Vendor_Alias';")
    master_table = res.fetchone()

    # check each returned table to see if Vendors is already included
    if master_table is not None and 'Vendor_Alias' in master_table:
        try:
            cursor.execute("INSERT INTO Vendor_Alias (vendor_alias, vendor_id) VALUES (?, ?);", (alias, vendor_id))
        except sqlite3.Error as er:
            # Check for specific SQL error code for the unique constraint being violated
            if er.sqlite_errorcode == 2067:
                print("Vendor Alias already exists in the database")
            else:
                # Need to determine how to gracefull hanndled the errors
                print("Database Load Error Encountered")

    # if we are already provided a DB connection, we don't want to commit / close the connection independently here
    if con is None:
        db_con.commit()
        db_con.close()




# All Transactions will be in one table - bank, CC all - need to ensure all fields are all encompassing