import pandas as pd
import database_manage as dbm

transaction_df = pd.read_csv('fake_2025_cc_transactions.csv')

#amounts = transaction_df.iloc[-3:]

#dbm.create_new_transaction_table()

print(transaction_df.head())
        