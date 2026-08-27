import csv
#import pandas as pd
import Database.database_manage as dbm
import vendor_trie as vt
import datetime as dt







# Function to determine correction position for entry into the DB and perform lookup in Trie for transaction naming
# Function returns a list of correctly positioned transactions ready for entry into the DB
def parse_transactions(transactions):
    '''
    Places the details of each transaction in the loaded file into the proper database table positioning
    
    transactions: CSV Reader object containing all transactions from the loaded credit card file
    '''
    # Transaction Table Headers: Date, Description, Amount
    # Would like to give user the option to select which column of the csv match via the GUI
    # determine the position in the original file - use this to identify index to extract for placement in DB table
    position_list = []
    # Next will return the current row with the first being the header
    header = next(transactions)
    
    # TODO: Later will give user options based on their declared cards in their profile

    # obtain the position of where the needed column currently is in the input file
    # we then know from which column to extract the needed data in the original input file
    for index in range(len(header)):
        column = header[index].lower()
        # Don't want to include any 'post dates'
        if 'date' in column and 'post' not in column:
            # need to insert the value into the postion what where we need it to be in the Tranx DB table
            position_list.insert(0, index)
        elif 'description' in column:
            position_list.insert(1, index)
        elif 'amount' in column:
            position_list.insert(2, index)
   
    card_issuer = input("Enter Name of Card Issuer: ")
    # Create new transaction list with values in correct position for DB entry
    # The first element in transactions is the first row of actual data
    updated_transactions = []
    for transaction in transactions:
        # change to a date object - Need to ensure they are the same format for all transactions
        date = transaction[position_list[0]]
        # Convert date to date object
        paren_pos1 = date.index("/")
        paren_pos2 = date.rindex("/")
        day = int(date[paren_pos1+1: paren_pos2])
        month = int(date[:paren_pos1])
        year = date[paren_pos2+1:]
        # Determine if the year value provided is 2 or 4 characters
        if len(year) == 2:
            #Im only concerned with future tranx right now
            year = int(year)
            year += 2000
        else:
            year = int(year)
        
        date = dt.date(year, month, day)

        description = transaction[position_list[1]]
        # Convert to a float
        amount = float(transaction[position_list[2]])
        # If tranx amounts are presented as negative values, convert to positive - Everything should be positive in DB
        if amount < 0:
            amount *= -1

        updated_transactions.append([card_issuer, date, description, amount])

    return updated_transactions


# TODO: Once GUI in place, option will be available for user to select file to load, for now use hard coded input
def load_credt_card_transactions():    
    #transaction_filename = input("Enter Transaction CSV File Name: ")
    #transaction_filename = "Transactions/test_amex_transactions.csv"
    #transaction_filename = "Transactions/test_amex_transactions_resampled.csv"
    transaction_filename = "Transactions/test_amex_transactions_unique.csv"
    #transaction_filename = "Transactions/test_amex_duplicates.csv"

    db_to_load = []

    with open(transaction_filename, newline='') as csv_file:
        transactions = csv.reader(csv_file)
        db_to_load = parse_transactions(transactions)

    dbm.insert_transactions_from_file(db_to_load, vendors, vendor_aliases)


def load_bank_transactions():
    pass


if __name__ == "__main__":

     # will later add ability to select database
    dbm.create_new_transaction_table()
    dbm.create_new_vendor_table()


    # Returns a dictionary of eahc known vendor alias mapped to its affiliated vendor number
    vendor_aliases = dbm.get_vendor_aliases()

    # Returns a list of tuples each containing a known vendor type
    vendor_types = dbm.get_vendor_types()

    # Returns the head of a new Vendor Trie
    vendors = vt.VendorTrie()
    # Returns the head of a new transaction type Trie
    transaction_types = vt.VendorTrie()

    # Populates the Trie with all known vendors and related details (ID, Type, Word Status)
    vendors.populate_trie_from_db("vendors")
    transaction_types.populate_trie_from_db("types")
    load_credt_card_transactions()