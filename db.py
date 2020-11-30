import shutil
import sqlite3

__author__ = "Radek Warowny"
__licence__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Radek Warowny"
__email__ = "radekwarownydev@gmail.com"
__status__ = "Demo"


def print_centre(s):
    print(s.center(shutil.get_terminal_size().columns))


def db_conn():

    # Open existing or create new databse

    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    try:
        # Create table 'Users' in database
        cur.execute("""CREATE TABLE Users 
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
             username TEXT NOT NULL, 
             password TEXT NOT NULL,
             account_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
             )""")
        # Create table 'word_explanation' in database
        cur.execute("""CREATE TABLE word_explanation
            (page_id INTEGER PRIMARY KEY AUTOINCREMENT, 
             word TEXT NOT NULL,
             explanation TEXT NOT NULL,
             user_id INTEGER NOT NULL,
             page_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
             FOREIGN KEY (user_id) REFERENCES Users(user_id)
             )""")

        # Create table 'Distillations' in database
        cur.execute("""CREATE TABLE Distillations
            (distillation_id INTEGER PRIMARY KEY AUTOINCREMENT, 
             distillation TEXT NOT NULL,
             page_id INTEGER,
             distillation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
             FOREIGN KEY (page_id) REFERENCES Pages(page_id)
             )""")
        # Insert first user

        dummy_data = """INSERT IGNORE INTO Users (username, password)  
                VALUES (?,?);"""
        data_tuple = ('dummy', '0000')
        cur.execute(dummy_data, data_tuple)
        conn.commit()

    except sqlite3.Error as error:
        pass  # Needs a tweak as it throws error every time it tries to insert into users
    finally:
        if conn:
            conn.close()


def create_user(username, password):

    # Connect to database

    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    # Insert variables into database
    try:
        sqlite_insert_with_param = """INSERT INTO Users (username, password) 
        VALUES (?,?);"""

        data_tuple = (username, password)
        cur.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        print_centre("USER ADDED")

        cur.close()

    except sqlite3.Error as error:
        print_centre("FAILED TO ADD USER")
    finally:
        if conn:
            conn.close()


def check_user(password):

    password = (password,)
    conn = None
    try:
        conn = sqlite3.connect('goldlist_db.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT user_id FROM Users WHERE password =?', password)
        output = cur.fetchone()
        if output is not None:
            flag = True
        else:
            output = highest_id()
            flag = False

        return output, flag
    except sqlite3.Error as e:

        print_centre(f"Error {e.args[0]}")
    finally:
        if conn:
            conn.close()


def highest_id():
    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    last_id = cur.execute('SELECT max(user_id) FROM Users;')
    output = last_id.fetchall()[0]

    cur.close()
    conn.close()

    return output


def insert_word(word, explanation, user_id):
    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    try:
        sqlite_insert_with_param = """insert into word_explanation (word, explanation, user_id) VALUES (?,?,?);"""

        data_tuple = (word, explanation, user_id)
        cur.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        cur.close()

    except sqlite3.Error as error:
        print_centre("Failed to insert Python variables into word_explanation table.")
        print_centre(error)
    finally:
        if conn:
            conn.close()








