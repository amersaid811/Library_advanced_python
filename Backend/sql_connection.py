import mysql.connector

__cnx = None

def get_sql_connection():
    global __cnx

    try:
        if __cnx is None or not __cnx.is_connected():
            print("Opening MySQL connection")
            __cnx = mysql.connector.connect(user='root', password='amersaid95', database='lib')
    except mysql.connector.Error as err:
        print("Error:", err)
    
    return __cnx

def connection_close():
    global __cnx

    if __cnx is not None and __cnx.is_connected():
        print("Closing MySQL connection")
        __cnx.close()
        __cnx = None  # Reset the global connection variable

# Example usage:
# conn = get_sql_connection()
# Perform database operations using 'conn'
# connection_close()  # Close the connection when done
