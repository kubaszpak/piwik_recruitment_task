import mysql.connector
from getpass import getpass
import time


def get_valid_choice(prompt):
    # function gets correct yes/no input from user with specified prompt
    while True:
        decision = input(prompt)
        if decision.lower() not in ('y', 'n', 'yes', 'no'):
            continue
        return decision


def transfer():
    print('Enter information about the database with the Titles table, that you would like to send data from: ')
    host = input("Host: ")
    user = input("User: ")
    password = getpass()
    database = input("Database: ")

    inserted_rows = 0

    db_src = mysql.connector.connect(
        host=host, user=user, passwd=password, database=database)

    decision = get_valid_choice(
        'Is the database you want to send data to, assessible by the same user? (Y/N): ')

    if(decision.lower() in ('y', 'yes')):
        database = input(
            'Enter the name of the database you want to sent data to: ')

        cursor_src = db_src.cursor()

        start = time.time()

        sql_query = f"INSERT INTO {database}.Titles (emp_no, title, from_date, to_date) SELECT * FROM {db_src.database}.Titles"

        cursor_src.execute(sql_query)

        inserted_rows = cursor_src.rowcount

        db_src.commit()

    else:
        print(
            'Enter information about the database with the Titles table, that you would like to send data to: ')
        host = input("Host: ")
        user = input("User: ")
        password = getpass()
        database = input("Database: ")

        db_dst = mysql.connector.connect(
            host=host, user=user, passwd=password, database=database)
        
        start = time.time()

        cursor_src = db_src.cursor(buffered=True)
        cursor_dst = db_dst.cursor(buffered=True)

        select_query = f"SELECT * FROM {db_src.database}.Titles"
        insert_query = f"INSERT INTO {db_dst.database}.Titles (emp_no, title, from_date, to_date) VALUES (%s, %s, %s, %s)"

        cursor_src.execute(select_query)

        fetched_values = cursor_src.fetchall()
        cursor_dst.executemany(insert_query, fetched_values)

        inserted_rows = cursor_dst.rowcount

        db_dst.commit()

        cursor_dst.close()
        db_dst.close()

    cursor_src.close()
    db_src.close()
    end = time.time()
    print(end - start)
    return inserted_rows


if __name__ == '__main__':
    inserted_rows = transfer()
