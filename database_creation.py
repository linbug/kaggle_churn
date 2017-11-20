import sqlite3
import csv


def main():
    # open the connection
    db = sqlite3.connect('data/mydb')
    cur = db.cursor()

    # create the members table
    cur.execute('''
        CREATE TABLE members(
        msno TEXT PRIMARY KEY,
        city INTEGER,
        bd INTEGER,
        gender TEXT,
        registered_via INTEGER,
        registration_init_time TEXT)
        ''')

    # create the transactions table
    cur.execute('''
        CREATE TABLE transactions(
        transaction_id INTEGER PRIMARY KEY,
        msno TEXT,
        payment_method_id INTEGER,
        payment_plan_days INTEGER,
        plan_list_price INTEGER,
        actual_amount_paid INTEGER,
        is_auto_renew INTEGER,
        transaction_date INTEGER,
        membership_expire_date INTEGER,
        is_cancel INTEGER)
        ''')

    # create the user_logs table
    cur.execute('''
        CREATE TABLE user_logs(
        msno TEXT,
        date TEXT,
        num_25 INTEGER,
        num_50 INTEGER,
        num_75 INTEGER,
        num_985 INTEGER,
        num_100 INTEGER,
        num_unq INTEGER,
        total_secs FLOAT,
        PRIMARY KEY (msno, date))
        ''')

    # create the training table
    cur.execute('''
        CREATE TABLE training(
        msno TEXT,
        is_churn INTEGER
        )
        ''')

    # create the sample_submission table
    cur.execute('''
        CREATE TABLE sample_submission(
        msno TEXT,
        is_churn INTEGER
        )
        ''')

    # insert members data into database
    with open('data/churn_comp_refresh/members_v2.csv', 'rt') as f:
        dicts = csv.DictReader(f)
        to_db = [
            (d['msno'],
                d['city'],
                d['bd'],
                d['gender'],
                d['registered_via'],
                d['registration_init_time']) for d in dicts]

        cur.executemany(
            '''INSERT INTO members
            (msno, city, bd, gender, registered_via, registration_init_time)
            VALUES (?, ?, ?, ?, ?, ?);''', to_db)

    # insert transactions data into database
    with open('data/churn_comp_refresh/transactions_v2.csv', 'rt') as f:
        dicts = csv.DictReader(f)
        to_db = [
            (
                d['msno'],
                d['payment_method_id'],
                d['payment_plan_days'],
                d['plan_list_price'],
                d['actual_amount_paid'],
                d['is_auto_renew'],
                d['transaction_date'],
                d['membership_expire_date'],
                d['is_cancel'],
            )
            for d in dicts]

        cur.executemany(
            '''INSERT INTO transactions
            ('msno', 'payment_method_id',
            'payment_plan_days',
            'plan_list_price',
            'actual_amount_paid',
            'is_auto_renew',
            'transaction_date',
            'membership_expire_date', 'is_cancel')
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''', to_db)

    # insert user_logs into database
    with open('data/churn_comp_refresh/user_logs_v2.csv', 'rt') as f:
        dicts = csv.DictReader(f)
        to_db = [
            (
                d['msno'],
                d['date'],
                d['num_25'],
                d['num_50'],
                d['num_75'],
                d['num_985'],
                d['num_100'],
                d['num_unq'],
                d['total_secs'],
                )
            for d in dicts]

    # insert training data into database
    with open('data/churn_comp_refresh/train_v2.csv', 'rt') as f:
        dicts = csv.DictReader(f)
        to_db = [
            (
                d['msno'],
                d['is_churn'],
                )
            for d in dicts]

        cur.executemany(
            '''INSERT INTO training
            ('msno', 'is_churn')
            VALUES (?, ?);''', to_db)
        db.commit()

    # insert test data into database
    with open('data/churn_comp_refresh/sample_submission_v2.csv', 'rt') as f:
        dicts = csv.DictReader(f)
        to_db = [
            (
                d['msno'],
                d['is_churn'],
                )
            for d in dicts]

        cur.executemany(
            '''INSERT INTO sample_submission
            ('msno', 'is_churn')
            VALUES (?, ?);''', to_db)
        db.commit()
