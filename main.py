__author__ = "Radek Warowny"
__licence__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Radek Warowny"
__email__ = "radekwarownydev@gmail.com"
__status__ = "Demo"


import getpass
import math
import sqlite3
import pandas as pd
import os
import shutil
import sys
import time
from db import db_conn, check_user, insert_word

words = []  # list of words typed in current session


def print_centre(s):
    print(s.center(shutil.get_terminal_size().columns))


def logo():
    print_centre('░██████╗░░█████╗░██╗░░░░░██████╗░  ██╗░░░░░██╗░██████╗████████╗')
    print_centre('██╔════╝░██╔══██╗██║░░░░░██╔══██╗  ██║░░░░░██║██╔════╝╚══██╔══╝')
    print_centre('██║░░██╗░██║░░██║██║░░░░░██║░░██║  ██║░░░░░██║╚█████╗░░░░██║░░░')
    print_centre('██║░░╚██╗██║░░██║██║░░░░░██║░░██║  ██║░░░░░██║░╚═══██╗░░░██║░░░')
    print_centre('╚██████╔╝╚█████╔╝███████╗██████╔╝  ███████╗██║██████╔╝░░░██║░░░')
    print_centre('░╚═════╝░░╚════╝░╚══════╝╚═════╝░  ╚══════╝╚═╝╚═════╝░░░░╚═╝░░░')
    print_centre("𝕓𝕪 ℝ𝕒𝕕𝕖𝕜  PRESS q to QUIT")


def introduction():
    os.system('clear')
    print_centre("Struggling with learning a foreign language? ")
    time.sleep(1)
    print_centre("Tired of flashcards and memorising glossaries? ")
    time.sleep(1)
    print_centre("If so, the GOLD LIST method may help.")
    time.sleep(1)
    print_centre("PRESS ANY KEY")

    input()
    os.system('clear')

    print()
    print_centre(" +-------------------------+ +--------------------------+")
    print_centre(" |                         | |                          |")
    print_centre(" |                         --->                         |")
    print_centre(" |                         | |                          |")
    print_centre(" |                         | |      1st DISTILLATION    |")
    print_centre(" |        MAIN LIST        | |          17 WORDS        |")
    print_centre(" |        25 WORDS         | |                          |")
    print_centre(" |                         | |                          |")
    print_centre(" |                         | |                          |")
    print_centre(" |   ▲                     | +----------------------|---+")
    print_centre(" +---|---------------------+ +----------------------|---+")
    print_centre(" +---|---------------------+ |                      ▼   |")
    print_centre(" |                         | |                          |")
    print_centre(" |                         | |      2nd DISTILLATION    |")
    print_centre(" |    3rd DISTILLATION     | |          11 WORDS        |")
    print_centre(" |        7 WORDS         <---                          |")
    print_centre(" |                         | |                          |")
    print_centre(" |                         | |                          |")
    print_centre(" +-------------------------+ +--------------------------+")
    print()
    print_centre("You start by typing words from the dictionary.")
    time.sleep(1)
    print_centre("Then you wait for at least two weeks to find out")
    time.sleep(1)
    print_centre("that you almost miraculously remembered 30% words")
    time.sleep(1)
    print_centre("from each list. All thanks to the power of moving information")
    time.sleep(1)
    print_centre("from short to long-term memory")
    time.sleep(1)
    print_centre("PRESS ANY KEY")

    input()
    os.system('clear')


def login_interface():
    os.system('clear')

    logo()  # application logo

    try:
        print_centre('USERNAME: ')
        username = input(''.center(112))

        if username == 'q':
            print_centre("PROGRAM TERMINATES")
            time.sleep(1)
            sys.exit()
        print_centre('PASSWORD: ')
        password = getpass.getpass(''.center(112))  # getpass renders input invisible
        from db import check_user, create_user, insert_word, db_conn
        if not username or not password:
            print_centre('INVALID INPUT')
        else:

            if not check_user(password)[1]:  # CREATE ACCOUNT INTERFACE
                print_centre('CREATE ACCOUNT(Y/N): ')
                response = getpass.getpass(''.center(112))
                if response.lower() != 'y':

                    print_centre('PROGRAM TERMINATES')
                    time.sleep(1)
                    sys.exit()
                else:
                    introduction()
                    create_user(username, password)
                    check_user(password)
                    print()
                    print_centre('PROGRAM STARTS')
                    print()
                    time.sleep(1)
            else:
                pass
            return password
    except ValueError as e:
        print(e)


def dict_load():

    # Loads in CSV dictionary file

    df = pd.read_csv('en_dict.csv')
    df.columns = ['word', 'grammar', 'explanation']
    output = df[['word', 'explanation']]
    return output


def user_input():

    print('\n\n\n')

    user_word = input(''.center(90))
    if user_word == "":
        interface()
    elif user_word == 'q':
        show_menu()
    else:
        try:
            word = user_word.split(' ', 1)[0]
            explanation = user_word.split(' ', 1)[1]
            word = word.title()
            explanation = explanation.title()
            words.append(word)
            insert_word(word, explanation, user_id[0])

        except IndexError:
            print_centre("\n\t\tINPUT MUST NOT BE BLANK.")
            time.sleep(2)
            interface()
        return interface()


def interface():
    # Main application interface

    # loads in one word - explanation pair from dictionary CSV file
    sample = word_explanation.sample(1)
    final_word = sample.to_string(index=False, header=False)
    word = str(final_word.split(' ')[1])
    explanation = ' '.join(final_word.split(' ')[3:])
    explanation = str(explanation)

    os.system('clear')  # clears the screen so interface stays at the top
    print_centre("*** 🅆🄾🅁🄳 ********** 🄴🅇🄿🄻🄰🄽🄰🅃🄸🄾🄽  *** PAGE NO {} ***\n".format(count_pages()))

    print(', '.join(words))
    print_centre('{} --- {}'.format(str(word), str(explanation)))

    user_input()


def get_last_word():

    # gets last word saved by the by the user

    user = (user_id[0],)
    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    cur.execute('SELECT  min(word) FROM word_explanation WHERE user_id =?', user)
    output = cur.fetchone()[0]
    print_centre(output)

    cur.close()
    conn.close()


# def show_list(n):
#
#     # shows all words saved in current session
#     os.system('clear')
#     user = (user_id[0],)
#     conn = sqlite3.connect('goldlist_db.sqlite')
#     cur = conn.cursor()
#
#     cur.execute('SELECT word FROM word_explanation WHERE user_id =?', user)
#     rows = cur.fetchall()
#     no = 1
#     for row in range(n):
#         print("{}. {}".format(no, row[0]))
#         no += 1
#     count_pages()
#     cur.close()
#     conn.close()


def count_pages():

    # counts all user pages

    user = (user_id[0],)
    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    cur.execute('SELECT COUNT(word) FROM word_explanation WHERE user_id =?', user)
    number = int(cur.fetchone()[0])
    pages = (number / 25) + 1
    pages = math.floor(pages)
    if pages == 0:
        pages = 1

    cur.close()
    conn.close()
    return pages


def show_pages():
    os.system('clear')
    print()
    print_centre('YOU CURRENTLY HAVE {} PAGES.'.format(count_pages()))
    print_centre('CHOSE PAGE')
    print()
    n = int(getpass.getpass(''.center(112)))

    # shows all words saved in current session
    os.system('clear')
    user = (user_id[0],)
    conn = sqlite3.connect('goldlist_db.sqlite')
    cur = conn.cursor()

    cur.execute('SELECT word FROM word_explanation WHERE user_id =?', user)
    rows = cur.fetchall()
    no = 1
    for row in rows:
        print("{}. {}".format(no, row[0]))
        no += 1
    count_pages()
    cur.close()
    conn.close()


def show_distill():
    os.system('clear')
    print()
    print_centre("YOUR DISTILLED WORDS: ")


def show_dict():
    os.system('clear')
    print()
    print_centre("DICTIONARIES")
    print_centre("EN DE FR PL")
    print()
    print_centre("CURRENT DICTIONARY: EN")
    print()
    print_centre("(DICTIONARY CHANGE NOT SUPPORTED)")


def show_menu():
    os.system('clear')
    logo()
    print()
    print_centre("1. YOUR DICTIONARY")
    print_centre("2. YOUR PAGES")
    print_centre("3. YOUR DISTILLATIONS")
    print_centre("4. YOUR ACCOUNT")
    print_centre("PRESS 'S' TO START")
    print()

    option_input = getpass.getpass(''.center(112))
    if option_input == "q":
        print_centre('PROGRAM TERMINATES')
        time.sleep(1)
        sys.exit()
    if int(option_input) == 1:
        show_dict()
        getpass.getpass(''.center(112))
        show_menu()
    elif int(option_input) == 2:
        show_pages()
        getpass.getpass(''.center(112))
        show_menu()
    elif int(option_input) == 3:
        show_distill()
        getpass.getpass(''.center(112))
        show_menu()
    elif int(option_input) == 4:
        show_account()
        getpass.getpass(''.center(112))
        show_menu()
    elif option_input == "s":
        interface()
    else:
        print("\nINVALID INPUT")
        time.sleep(1)
        show_menu()


def show_account():
    os.system('clear')
    logo()
    print()
    print_centre("ADD NAME: ")
    print()
    print_centre("PRESS 's' TO START ")
    interface()
    print()
    print_centre(" PRESS 'q' TO QUIT ")
    print()
    option_input = getpass.getpass(''.center(112))
    if option_input == "s":
        interface()
    elif option_input == "q":
        show_menu()
    else:
        print_centre("INVALID INPUT")
        time.sleep(1)
        show_account()


db_conn()
user_id = check_user(login_interface())[0]
word_explanation = dict_load()  # 2. Loading Dictionary
interface()  # 4. Running Program









