# Import necessary functions from the 'database' module
from database import (
    connect_to_database,  # Function to establish a connection to the database
    register_member,  # Function to register a new member
    login_member,  # Function to login a member
    member_menu  # Function to display the member menu
)


# Main function to run the BookStore application
def main():
    # Connect to the MySQL database
    db_connection = connect_to_database()

    # Main menu loop
    while True:
        # Display main menu options
        print("\n***********************************************")
        print("***                                         ***")
        print("***     Welcome to The OnlineBookStore      ***")
        print("***                                         ***")
        print("***********************************************\n")
        print("            1. Member Login")
        print("            2. New Member Registration")
        print("            q. Quit\n")

        # Get user input for main menu choice
        choice = input("Enter your choice: ")

        # Perform actions based on user choice
        if choice == "2":
            # Register a new member
            register_member(db_connection)
        elif choice == "1":
            # Login a member
            member = login_member(db_connection)
            # If login is successful, display the member menu
            if member:
                member_menu(db_connection, member)
        elif choice == "q":
            # Quit the application
            print("Quitiing...")
            break
        else:
            # Invalid choice
            print("Invalid choice. Please try again.")

    # Close the database connection
    if db_connection:
        db_connection.close()


# If this script is run directly (not imported), run the main function
if __name__ == "__main__":
    main()
