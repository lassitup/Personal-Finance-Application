import sqlite3

def create_new_transaction_table():
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE transactions 
                   (transaction_date TEXT, post_date TEXT, description TEXT, 
                   category TEXT, type TEXT, amount REAL, memo TEXT)""") 
    cursor.close()

#Use to_sql to load to database after I've created the user's table manage 'manually' after this
def insert_transactions_from_file(transaction_list):
    con = sqlite3.connect('Database/personal_finance_db.db')
    cursor = con.cursor()
    #executemany to perform repeated SQL statements
    cursor.executemany("""INSERT INTO transactions VALUES(?, ?, ?, ?, ?, ?, ?)""", transaction_list)
    con.commit()




# All Transactions will be in one table - bank, CC all - need to ensure all fields are all encompassing