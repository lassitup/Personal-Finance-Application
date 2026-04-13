import csv
import pandas as pd
import Database.database_manage as dbm



# will later add ability to select database
#dbm.create_new_transaction_table()

# Once GUI in place, option will be available for user to select file to load, for now use input
def load_transactions():    
    #transaction_filename = input("Enter Transaction CSV File Name: ")
    transaction_filename = "test_transactions.csv"

    db_to_load = []

    with open(transaction_filename, newline='') as csv_file:
        transactions = csv.reader(csv_file)
        for transaction in transactions:
            #print(transaction)
            db_to_load.append(transaction)

    dbm.insert_transactions_from_file(db_to_load)




load_transactions()