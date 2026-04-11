import sqlite3

def create_new_transaction_table():
    con = sqlite3.connect('personal_finance_db.db')
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE credit_card_transactions 
                   (transaction_date TEXT, post_date TEXT, description TEXT, 
                   category TEXT, type TEXT, amount REAL, memo TEXT)""") 
    cursor.close()

#Use to_sql to load to database after I've created the user's table manage 'manually' after this