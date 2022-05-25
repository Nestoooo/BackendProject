import json
import sqlite3

def create_table():
    print(" >>> ", create_table.__name__)
    conn = sqlite3.connect('quizesdata.db')
    cur = conn.cursor()
    #cur.execute("DROP TABLE IF EXISTS QUIZES;")
    #cur.commit()
    cur.execute("CREATE TABLE QUIZES ("
                "QUIZ_NAME TEXT (200) NOT NULL,"
                "QUIZ NVARCHAR (3000) NOT NULL);")

def drop_table():
    print(" >>> ", drop_table.__name__)
    conn = sqlite3.connect('quizesdata.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS QUIZES;")

def add_quiz(q_name, q_data):
    print(" >>> ", add_quiz.__name__)
    conn = sqlite3.connect('quizesdata.db')
    cur = conn.cursor()
    insert_string = "INSERT INTO QUIZES VALUES ('" + q_name + "','" + q_data + "');"
    cur.execute(insert_string)
    conn.commit()
    conn.close()


def get_all():
    print(" >>> ", get_all.__name__)
    conn = sqlite3.connect('quizesdata.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZES")
    records = cur.fetchall()
    conn.commit()
    return records


def get_quiz(this_quiz):
    print(" >>> ", get_quiz.__name__)
    conn = sqlite3.connect('quizesdata.db')
    cur = conn.cursor()
    cur.execute("SELECT QUIZ FROM QUIZES WHERE QUIZ_name = '" + this_quiz + "';")
    records = cur.fetchall()
    conn.commit()
    return records
    
def count_quizes():
    print(" >>> ", count_quizes.__name__)
    conn = sqlite3.connect('quizesdata.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUIZES")
    records = cur.fetchall()
    conn.commit()
    return len(records)

def delete_quiz(this_quiz):
    print(" >>> ", delete_quiz.__name__)
    conn = sqlite3.connect('quizesdata.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM QUIZES WHERE QUIZ_NAME = '" + this_quiz + "';")
    conn.commit()



