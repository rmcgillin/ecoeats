from flask import Flask, render_template, request, redirect, session, url_for
from app import app, db
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('EcoEats Database.db')
cur = conn.cursor();
cur.execute("select product_id, product_name from food_product")
# desc = cur.description
# column_names=[col[0] for col in desc]
# available_items= [dict(column_names, row)
# for row in cur.fetchall()]
# # available_items = []
results=cur.fetchall()
available_items = {result[0]: result[1] for result in results}
app.config['SECRET_KEY'] = 'the random string'  


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # check login credentials against the database
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('EcoEats Database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
        if cursor.fetchone() is not None:
            # if authentication is successful, set session cookie and redirect to the menu page
            session['email'] = email
            conn.close()
            return redirect('/menu.html')
        else:
            # if authentication fails, show login error
            conn.close()
            return render_template('login.html', error='Invalid login')
    else:
        # show login page
        return render_template('login.html')

#link db
@app.route('/menu.html')
def menu():
    if 'email' in session:
        # show the menu page
        return render_template('menu.html', forename = 'Rebecca' )
    else:
        # if user is not authenticated, redirect to login page
        return redirect('/login.html')

@app.route('/signup.html')
def signup():
    cursor = conn.cursor()

    forename = input("Enter your forename: ")
    surname = input("Enter your surname: ")
    email = input("Enter your email address: ")
    password = input("Enter your password: ")
    phone_number = input("Enter your phone number:")

# SQL query to insert a new user into the "users" table
    insert_query = """
    INSERT INTO users (forename, surname, email, password, phone_number)
    VALUES (?, ?, ?, ?, ?)
    """

# Execute the query with user information as parameters
    cursor.execute(insert_query, (forename, surname, email, password, phone_number))


# Commit the changes to the database
    conn.commit()

# Close the connection
    conn.close()
    return render_template('signup.html')

@app.route('/search')
def search(product_name):
    render_template("search.html")

@app.route('/favourites')
def favourites():
    conn = sqlite3.connect('EcoEats Database.db')
    c = conn.cursor()
    available_items = ""
    c.execute('select product_name from food_product, favourites where favourites.product_id=food_product.product_id')
    data = c.fetchall()
    
    c.execute('SELECT DISTINCT product_id, product_name from food_product')
    available_items=c.fetchall()
    conn.close()
    return render_template('favourites.html',data=data, available_items=available_items)

@app.route('/add_favourites', methods = ["GET","POST"])
def add_favourites():
    item_id = request.form['favourite_item']
    conn = sqlite3.connect('EcoEats Database.db')
    cursor = conn.cursor()    
    cursor.execute('INSERT INTO favourites (user_id, product_id) VALUES (?, ?)',(1, item_id))
    
    QUERY = 'select food_product.product_name from favourites, users, food_product where food_product.product_id=favourites.product_id and favourites.user_id=users.id'
    cursor = conn.cursor()
    cursor.execute(QUERY)
    data = cursor.fetchall()
    cursor.execute('SELECT DISTINCT product_id, product_name from food_product')
    available_items=cursor.fetchall()
 
    conn.commit()
    conn.close()
    return render_template('favourites.html',data=data, available_items=available_items)

if __name__ == '__main__':
    app.run(debug=True)
