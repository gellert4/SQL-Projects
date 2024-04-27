# Import necessary libraries
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error


# Function to establish a connection with the MySQL database
def connect_to_database():
    try:
        # Establish a connection with the MySQL database
        # Replace these values with your actual MySQL connection details
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gellert.123",
            database="book_store"
        )
        print("Connected to MySQL database")
        return connection
    except Error as e:
        print("Error connecting to MySQL database:", e)
        return None


# Function to register a new member
def register_member(connection):
    try:
        # Create a cursor object
        cursor = connection.cursor()
        # Get user input for registration details
        fname = input("Enter your first name: ")
        lname = input("Enter your last name: ")
        address = input("Enter your address: ")
        city = input("Enter your city: ")
        zip_code = input("Enter your zip code: ")
        phone = input("Enter your phone number (optional): ")
        email = input("Enter your email address: ")
        password = input("Enter your password: ")

        # SQL query to insert the new member into the Members table
        insert_query = (
            "INSERT INTO Members "
            "(fname, lname, address, city, zip, phone, email, password) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        member_data = (
            fname, lname, address, city, zip_code, phone, email, password
        )
        # Execute the query
        cursor.execute(insert_query, member_data)
        # Commit the transaction
        connection.commit()

        print("\nYou have registered successfully!")
        input("Press Enter to go back to Menu")

    except Error as e:
        print("Error registering member:", e)


# Function to login a member
def login_member(connection):
    try:
        # Create a cursor object
        cursor = connection.cursor()
        # Get user input for login details
        email = input("Enter your email address: ")
        password = input("Enter your password: ")

        # SQL query to check if the entered email and password match any
        # record in the Members table
        login_query = "SELECT * FROM Members WHERE email = %s " \
                      "AND password = %s"
        login_data = (email, password)
        # Execute the query
        cursor.execute(login_query, login_data)
        # Fetch the first record that matches the query
        member = cursor.fetchone()

        if member:
            print("Login successful!")
            return member
        else:
            print("Invalid email or password. Please try again.")
            return None
    except Error as e:
        print("Error logging in:", e)
        return None


# Function to display the member menu and handle member actions
def member_menu(db_connection, member):
    user_id = member[0]
    user_address = {
        'fname': member[1],
        'lname': member[2],
        'address': member[3],
        'city': member[4],
        'zip': member[5]
    }
    while True:
        # Display the member menu
        print("\n***********************************************")
        print("***                                         ***")
        print("***      Welcome to Online Book Store       ***")
        print("***              Member menu                ***")
        print("***                                         ***")
        print("***********************************************\n")
        print("            1. Browse by Subject")
        print("            2. Search by Author/Title")
        print("            3. Check Out")
        print("            4. Logout\n")

        # Get user input for the menu choice
        choice = input("Enter your choice: ")

        # Handle the user's choice
        if choice == "1":
            browse_by_subject(db_connection, user_id)
        elif choice == "2":
            search_by_author_title(db_connection)
        elif choice == "3":
            check_out(db_connection, user_id, user_address)
        elif choice == "4":
            logout()
            break
        else:
            print("Invalid choice. Please try again.")


# Function for browsing books by subject
def browse_by_subject(connection, user_id):
    try:
        # Create a cursor object
        cursor = connection.cursor()
        # Execute a query to get all distinct subjects from the Books table
        cursor.execute("SELECT DISTINCT subject FROM Books ORDER BY subject")
        # Fetch all subjects
        subjects = cursor.fetchall()

        # Print all subjects
        for i, subject in enumerate(subjects):
            print(f"{i+1}. {subject[0]}")

        # Get user input for the chosen subject
        choice = int(input("Enter your choice: ")) - 1
        chosen_subject = subjects[choice][0]

        # Execute a query to get all books of the chosen subject
        query = "SELECT * FROM Books WHERE subject = %s"
        cursor.execute(query, (chosen_subject,))
        # Fetch all books
        books = cursor.fetchall()

        # Print all books and handle user actions
        i = 0
        while i < len(books):
            for j in range(2):
                if i+j < len(books):
                    book = books[i+j]
                    print(f"\nAuthor: {book[1]}\nTitle: {book[2]}\nISBN: {book[0]}\nPrice: {book[4]}\nSubject: {book[3]}")

            action = input("\nEnter ISBN to add to cart or 'n' to browse "
                           "or ENTER to go back to menu: ")

            # Handle user actions
            if action == '':
                return
            elif action.lower() == 'n':
                i += 2
            else:
                # Get user input for the quantity and add the book to the cart
                quantity = int(input("Enter quantity: "))
                cursor.execute("INSERT INTO Cart(userid, isbn, qty) "
                               "VALUES(%s, %s, %s)",
                               (user_id, action, quantity))
                connection.commit()
                print("Book added to cart.")

    except Error as e:
        print("Error browsing by subject:", e)


# Function for searching books by author/title
def search_by_author_title(connection):
    try:
        # Create a cursor object
        cursor = connection.cursor()
        # Get user input for the search type
        search_type = input("Enter 1 for Author Search, 2 for Title Search: ")
        search_query = ""
        if search_type == "1":
            # Get user input for the author substring and search query
            substring = input("Enter author substring: ")
            search_query = "SELECT * FROM Books WHERE author LIKE %s"
        elif search_type == "2":
            # Get user input for the title substring and search query
            substring = input("Enter title substring: ")
            search_query = "SELECT * FROM Books WHERE title LIKE %s"

        # Execute the search query
        cursor.execute(search_query, ('%' + substring + '%',))
        # Fetch all books that match the search query
        books = cursor.fetchall()

        # Display search results
        for book in books:
            print(book)  # Adjust display as per requirement
    except Error as e:
        print("Error searching by author/title:", e)


# Function for checking out and generating an invoice
def check_out(connection, user_id, user_address):
    try:
        # Create a cursor object
        cursor = connection.cursor()

        # Query to fetch cart contents
        cart_query = "SELECT c.isbn, b.title, b.price, c.qty, (b.price * c.qty) AS total " \
                     "FROM Cart c INNER JOIN Books b ON c.isbn = b.isbn " \
                     "WHERE c.userid = %s"
        cursor.execute(cart_query, (user_id,))
        # Fetch all items in the cart
        cart_contents = cursor.fetchall()

        # If the cart is empty, print a message and return
        if not cart_contents:
            print("Your cart is empty.")
            return

        # Display cart contents header
        print("\nCurrent Cart Contents:\n")
        print("ISBN \t\t Title \t\t\t\t\t\t    $ Qty  Total")
        print("-" * 84)
        # Initialize total amount for the cart
        total_amount = 0

        # Loop through each item in the cart
        for item in cart_contents:
            # Unpack item details
            isbn, title, price, qty, total_item_price = item
            # If the title is longer than 30 characters, truncate and add '...'
            title = title[:30] + '...' if len(title) > 30 else title
            # Print item details in a formatted string
            print(
                f"{isbn} \t {title[:40]:<45} ${price:.2f}  "
                f"{qty:<3} ${total_item_price:.2f}"
            )
            # Add the total price of this item to the total amount
            total_amount += total_item_price

        # Calculate the total price of all items in the cart
        total_price = sum(item[4] for item in cart_contents)
        # Print the total price
        print(f"Total = \t\t\t\t\t\t\t\t  ${total_price:7.2f}")
        # Print a line for visual separation
        print("-" * 84)

        # Ask the user if they want to proceed to check out
        proceed = input("Proceed to check out (Y/N)?: ").strip().lower()
        # If the user does not want to proceed, return from the function
        if proceed != 'y':
            return

        # Calculate the shipment date as one week from now
        shipment_date = datetime.now() + timedelta(weeks=1)

        # Insert a new order into the Orders table
        order_query = "INSERT INTO Orders (userid, createDate, shipAddress, shipCity, shipZip) " \
                      "VALUES (%s, CURDATE(), %s, %s, %s)"
        cursor.execute(order_query, (user_id, user_address['address'],
                                     user_address['city'],
                                     user_address['zip']))
        # Get the ID of the newly inserted order
        order_id = cursor.lastrowid

        # Insert the details of the order into the OrderDetails table
        order_details_query = "INSERT INTO OrderDetails (ono, isbn, qty, amount) " \
                              "VALUES (%s, %s, %s, %s)"
        for item in cart_contents:
            cursor.execute(order_details_query, (order_id, item[0], item[3], item[4]))

        # Clear the user's cart
        clear_cart_query = "DELETE FROM Cart WHERE userid = %s"
        cursor.execute(clear_cart_query, (user_id,))
        # Commit the changes to the database
        connection.commit()

        # Print the invoice for the order
        print(f"\n\t\t\tInvoice for Order no.{order_id}\n")
        print("Shipping Address")
        print(f"Name: \t\t {user_address['fname']} {user_address['lname']}")
        print(f"City: \t\t {user_address['city']}")
        print(f"Zip: \t\t {user_address['zip']}\n")
        print("--------------------------------------------------------------------------------")
        print("ISBN \t\t Title \t\t\t\t\t\t    $ Qty  Total")
        print("--------------------------------------------------------------------------------")
        for item in cart_contents:
            # If the title is longer than 30 characters, truncate it and add '...'
            title = item[1][:30] + '...' if len(item[1]) > 30 else item[1]
            print(f"{item[0]} \t {title:<45} ${item[2]:7.2f}  {item[3]:<3}   ${item[4]:7.2f}")
        print("--------------------------------------------------------------------------------")
        print(f"Total = \t\t\t\t\t\t\t\t  ${total_price:7.2f}")
        print("--------------------------------------------------------------------------------")
        # Print the estimated shipment date
        print(f"Estimated shipment date: {shipment_date.strftime('%Y-%m-%d')}")

        # Wait for the user to press enter to go back to the menu
        input("\nPress enter to go back to Menu")

    # Handle any errors that occur during checkout
    except Error as e:
        print("Error during check out:", e)


# Function for logging out
def logout():
    print("Logging out...")
    # No database operations needed for logout
