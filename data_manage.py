import csv
import pandas as pd
import Database.database_manage as dbm
import vendor_trie as vt



# will later add ability to select database
dbm.create_new_transaction_table()
dbm.create_new_vendor_table()



vendor_aliases = dbm.get_vendor_aliases()
vendor_types = dbm.get_vendor_types()

vendors = vt.VendorTrie()
vendors.populate_trie_from_db()



# Function to determine correction position for entry into the DB and perform lookup in Trie for transaction naming
def parse_transactions(transactions):
    # Transaction Table Headers: Date, Description, Amount
    # Would like to give user the option to select which column of the csv match
    # determine the position in the original file, use that to place into 
    position_list = []
    # Next will return the current row with the first being the header
    header = next(transactions)
    
    # Later will give user options based on their declared cards in their profile
    # obtain the position of where the needed column currently is in the input file
    # we then know from which column to extract the needed data in the original input file
    for index in range(len(header)):
        column = header[index].lower()
        # Don't want to include any 'post dates'
        if 'date' in column and 'post' not in column:
            # need insert the value into the postion what where we need it to be
            position_list.insert(0, index)
        elif 'description' in column:
            position_list.insert(1, index)
        elif 'amount' in column:
            position_list.insert(2, index)
   
    card_issuer = input("Enter Name of Card Issuer: ")
    # create new transaction list with values in correct position for DB entry
    updated_transactions = []
    for transaction in transactions:
        # change to a date object?
        date = transaction[position_list[0]]
        description = transaction[position_list[1]]
        # Convert to a float
        amount = float(transaction[position_list[2]])
        if amount < 0:
            amount *= -1
        # I'll also need to add the type in here once I have trie / db scheme setup
        updated_transactions.append([card_issuer, date, description, amount])

    return updated_transactions


# Once GUI in place, option will be available for user to select file to load, for now use input
def load_transactions():    
    #transaction_filename = input("Enter Transaction CSV File Name: ")
    #transaction_filename = "Transactions/test_amex_transactions.csv"
    transaction_filename = "Transactions/test_amex_transactions.csv"

    db_to_load = []

    with open(transaction_filename, newline='') as csv_file:
        transactions = csv.reader(csv_file)
        db_to_load = parse_transactions(transactions)
        # Need to test for Refunds / Returns / Payments

    dbm.insert_transactions_from_file(db_to_load, vendors, vendor_aliases)




load_transactions()