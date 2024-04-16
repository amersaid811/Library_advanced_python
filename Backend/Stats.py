from sql_connection import get_sql_connection
from datetime import datetime

def loans_by_month(connection, month):
    cursor = connection.cursor()
    query = "SELECT * FROM lib.loans WHERE EXTRACT(MONTH FROM LoanDate) = %s" 
    cursor.execute(query, (month,))
    
    # Fetch the results
    results = cursor.fetchall()

    # Return the fetched results
    return results

###########################################################################################

def loans_between_2months(connection, month1,month2):
    if (month1 >= month2):
            cursor = connection.cursor()
            query = "SELECT * FROM lib.loans WHERE EXTRACT(MONTH FROM LoanDate) BETWEEN %s AND %s"  
            cursor.execute(query, (month1,month2))

            # Fetch the results
            results = cursor.fetchall()

            # Return the fetched results
            return results
    else:
        print(f"Incorrect choosen Months")
        return None


###########################################################################################

def loans_return(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM lib.loans WHERE ReturnDate IS NOT NULL" 
    cursor.execute(query)
    
    # Fetch the results
    results = cursor.fetchall()

    # Return the fetched results
    return results

def top5_books(connection):
    cursor = connection.cursor()
    query = """
    SELECT b.BookID, b.Title, COUNT(l.LoanID) as Number_of_Loans
    FROM lib.books b
    JOIN lib.loans l ON b.BookID = l.BookID
    GROUP BY b.BookID, b.Title
    ORDER BY Number_of_Loans DESC
    LIMIT 5;
    """
    cursor.execute(query)
    
    # Fetch the results
    results = cursor.fetchall()

    # Return the fetched results
    return results

if __name__ == '__main__':
    connection = get_sql_connection()

    # Call the top5_books function
    results = top5_books(connection)

    # Display the fetched results
    if results:
        print("Top 5 books with the highest number of loans:")
        for result in results:
            print(result)
    else:
        print("No results found.")



     



 
