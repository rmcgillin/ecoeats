import sqlite3

def search_database(search_term):

    #Connect to the SQLite database
    conn = sqlite3.connect('EcoEats Database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM food_product WHERE product_name LIKE ?", ('%' + search_term + '%',))
    # fetch the results
    results = c.fetchall()

    #print resutls
    for row in results:
        print(row)
    # close the database connection
    c.close()

search_term = "example"
search_database(search_term)


