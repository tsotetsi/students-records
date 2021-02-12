import sqlite3
from flask import Flask, render_template, request


def init_sqlite_db():

    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, city TEXT, pin_code TEXT)')
    print("Table created successfully")
    conn.close()


init_sqlite_db()


app = Flask(__name__)

@app.route('/')
@app.route('/registration-form/')
def enter_new_student():
    return render_template('registration-form.html')


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            pin_code = request.form['pin-code']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO student (name, address, city, pin_code) VALUES (?, ?, ?, ?)", (name, address, city, pin_code))
                con.commit()
                msg = name + " was successfully added to the database."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            con.close()
            return render_template('results.html', msg=msg)


@app.route('/show-records/', methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM student")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return render_template('records.html', records=records)
