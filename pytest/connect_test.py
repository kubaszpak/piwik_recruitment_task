import connect
from getpass import getpass
import mysql.connector


def test_transfer():
    print('Enter information about the database with the Titles table, that you would like to check: ')
    host = input("Host: ")
    user = input("User: ")
    password = getpass()
    database = input("Database: ")

    db = mysql.connector.connect(
        host=host, user=user, passwd=password, database=database)

    cursor = db.cursor()

    sql_query = f"SELECT COUNT(*) FROM Titles"

    cursor.execute(sql_query)
    (number_of_rows,) = cursor.fetchone()

    db.close()

    assert number_of_rows == 443308


# def test_transfer():
#     number_of_inserted_rows = connect.transfer()
#     assert number_of_inserted_rows == 443308
