import sqlite3
import csv



def load_cc_detail(file_name):
    con = sqlite3.connect('personal_finance.db')

    cur = con.cursor()

    with open("fake_2025_cc_transactions.csv", "r", newline="") as cc_file:
        transactions = csv.reader(cc_file)
        transactions_list = []
        for transaction in transactions:
            transactions_list.append(transaction)
            
    #print(transactions_list)

    for index in range(1,len(transactions_list)):
        #Use sqlite3 module's execute parameter substitution instead of string operations such as f string
        vals = (transactions_list[index][0], transactions_list[index][1], transactions_list[index][2], transactions_list[index][3], transactions_list[index][4], float(transactions_list[index][5]), transactions_list[index][6])
        cur.execute("INSERT INTO credit_card_transactions ('TRANSACTION_DATE', 'POST_DATE', 'DESCRIPTION', 'CATEGORY', 'TYPE', 'AMOUNT', 'MEMO') VALUES (?,?,?,?,?,?,?)", vals)


    con.commit()