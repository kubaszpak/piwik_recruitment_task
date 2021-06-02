# piwik_recruitment_task

A recruitment task of copying values from one mysql table to another one, keeping in mind that databases could be placed on different servers.

## Usage

To use this script you need a command line with a working mysql server. The other tool you need is python mysql connector. You can install it from [here](https://dev.mysql.com/downloads/connector/python/8.0.html)
or simply by running:

```
pip install mysql-connector
```

Testing - for testing I chose pytest. Install it via:
```
pip install pytest
```

## Running the application
<br>
Before running the application make sure you have prepared two databases both containing the same Titles table as referenced. One containing 443308 rows and one with the same structure, but fully empty. If you don't have the databases ready, clone this 

[repository](https://github.com/datacharmer/test_db) and run:

```
mysql < employees.sql
```
To then clone this repository I used [this](https://stackoverflow.com/questions/675289/mysql-cloning-a-mysql-database-on-the-same-mysql-instance) stackoverflow thread. After that I cleared the table from one of them with:

```MYSQL
USE <DATABASE_NAME>;
DELETE FROM TITLES;
```
Now everything should be ready.
To start the application you need to run the following command:

```
python connect.py
```
You will then be asked to provide the database information and if the databases are placed on the same server. Then based on that information specified proccesses will run to copy contents of the first table to the other one. __Keep in mind that the password is hidden, so the characters you type won't show up in the command line__

## Test

To test the application run:
```
python -m pytest -s
```
The test checks if after running the script the database has the same amount of rows as the original one.

In addition I modified the testing script again from [this](https://github.com/datacharmer/test_db) repository so you can also check if everything worked, by running:

```
mysql -t -u <username> -p < test_employees_md5.sql
```

## Description of the implemented improvements
<br>
I started off with the test of how long would the application copy the rows one by one using this method: (Result: 85-95 seconds)

```python
cursor_from.execute("SELECT * FROM Titles")

for (emp_no, title, from_date, to_date) in cursor_from:
    cursor_to.execute("INSERT INTO Titles VALUES (%s, %s, %s, %s)",
                        (emp_no, title, from_date, to_date))
```

I then tried adding a config parameter to the cursor to see if it changes anything (buffered = True). It only lowered time by a couple of seconds.

I knew these would for sure not be my final solution, but I gave them a try. A different interesting idea was copying the table with the following SQL Query: (Result: 5 seconds)

```python
cursor_dst.execute(
    f"CREATE TABLE {db_dst.database}.Titles AS SELECT * FROM {db_src.database}.Titles")
```

This command lowered the execution time to just 5 seconds, but it required that the table didn't exist at the time in the second database. This would be fine, if I could DROP THE TABLE at the beginning, but the instruction didn't specify if I could discard all of the rows from the table.

Then I had these two ideas and I decided to keep them both in the solution. Why? The first one does not work if the databases aren't placed one the same server, but it is faster and more reliable.

Solution I - Result (Execution time: ~ 5 seconds)
```python
sql_query = f"INSERT INTO {db_dst.database}.Titles (emp_no, title, from_date, to_date) SELECT * FROM {db_src.database}.Titles"

cursor_src.execute(sql_query)
```

Solution II - When the databases are placed on different servers (uses two db.connections) - Result (Execution time: ~ 10 seconds)

```python
cursor_src = db_src.cursor(buffered=True)
cursor_dst = db_dst.cursor(buffered=True)

select_query = f"SELECT * FROM {db_src.database}.Titles"
insert_query = f"INSERT INTO {db_dst.database}.Titles (emp_no, title, from_date, to_date) VALUES (%s, %s, %s, %s)"

cursor_src.execute(select_query)

fetched_values = cursor_src.fetchall()
cursor_dst.executemany(insert_query, fetched_values)
```