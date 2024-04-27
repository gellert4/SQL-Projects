@staticmethod
    def check_out(db, member):
        # Fetch cart contents
        cart_contents = db.execute_with_fetchall(f"""
            SELECT c.isbn, b.title, b.price, c.qty
            FROM cart c
            JOIN books b ON c.isbn = b.isbn
            WHERE c.userid = '{member.userid}'
        """)

        # Display cart contents header
        print("\nCurrent Cart Contents:\n")
        print("ISBN \t\t Title \t\t\t\t\t\t    $ Qty  Total")
        print("-" * 84)
        total_amount = 0

        # Display cart contents
        for cart_item in cart_contents:
            isbn, title, price, qty = cart_item
            total_item_price = price * qty

            # Display each cart item using a fixed-width format
            print(
                f"{isbn} \t {title[:40]:<45} ${price:.2f}  "
                f"{qty:<3} ${total_item_price:.2f}"
            )
            print("-" * 84)
            # Update total_amount with the current item's total price
            total_amount += total_item_price

        # Display total
        print(f"Total \t\t\t\t\t\t\t\t\t  ${total_amount:.2f}")
        print("-" * 84)
        # Ask user to proceed to check out
        proceed = input("Proceed to check out (Y/N)?: ")
        if proceed.lower() == 'y':
            # Fetch user's address
            address_details = db.execute_with_fetchall(
                f"SELECT address, city, zip "
                f"FROM members WHERE userid = '{member.userid}'"
            )

            # Check if the result is not empty
            if address_details:
                address_details = address_details[0]
            else:
                print("\nError: User address not found.")
                return  # Return or handle the error accordingly

            # Fetch the maximum ono value
            max_ono_query = "SELECT MAX(ono) FROM orders"
            max_ono_result = db.execute_with_fetchall(max_ono_query)
            max_ono = (
                max_ono_result[0][0]
                if max_ono_result and max_ono_result[0][0]
                else 0
            )

            # Increment the maximum ono to get a new unique value
            new_ono = max_ono + 1

            # Insert the order with the manually obtained ono value
            insert_order_query = (
                f"INSERT INTO orders (ono, userid, shipaddress, "
                f"shipcity, shipzip) VALUES ({new_ono}, "
                f"'{member.userid}', '{address_details[0]}', "
                f"'{address_details[1]}', '{address_details[2]}')"
            )

            # Save order to Order table
            db.execute_with_commit(insert_order_query)

            # Fetch the order id of the order just created
            max_ono_query = (
                f"SELECT MAX(ono) FROM orders "
                f"WHERE userid = '{member.userid}'"
            )
            max_ono_result = db.execute_with_fetchall(max_ono_query)
            if max_ono_result and max_ono_result[0][0] is not None:
                order_id = max_ono_result[0][0]
            else:
                print("\nError: Failed to retrieve order_id.")
                return  # Return or handle the error accordingly

            # Save books to 'odetails' table
            for item in cart_contents:
                isbn, title, price, qty = item
                amount = price * qty
                odetails_query = (
                    f"INSERT INTO odetails (ono, isbn, qty, amount) "
                    f"VALUES ({order_id}, '{isbn}', {qty}, {amount})"
                )

                # Save order details to odetails table
                db.execute_with_commit(odetails_query)

                # Clear the cart after successful checkout
                db.execute_with_commit(
                    f"DELETE FROM cart "
                    f"WHERE userid = '{member.userid}'"
                )

                # Display invoice
                print(f"\n\t\t\tInvoice for Order no.{order_id}\n")
                print("Shipping Address:")
                print(f"Name: \t\t {member.fname}, {member.lname}")
                print(f"Address: \t {address_details[0]}")
                print(f"\t\t {address_details[1]}")
                print(f"\t\t {address_details[2]}")
                print("-" * 84)
                print("ISBN \t\t Title \t\t\t\t\t\t    $  Qty  Total")
                print("-" * 84)

                # Display each cart item in the invoice section
                for item in cart_contents:
                    isbn, title, price, qty = item
                    total_item_price = price * qty

                    # Display each cart item using a fixed-width format
                    print(
                        f"{isbn} \t {title[:40]:<45} ${price:.2f}  "
                        f"{qty:<3} ${total_item_price:.2f}"
                    )
                    print("-" * 84)

                # Display total and estimated delivery date
                print(f"Total = \t\t\t\t\t\t\t\t  ${total_item_price:.2f}")
                current_date = datetime.datetime.now()
                estimated_delivery_date = (
                    current_date + datetime.timedelta(days=7)
                )
                print(
                    f"\nEstimated delivery date: "
                    f"{estimated_delivery_date}\n"
                )
                input("Press enter to go back to Menu")