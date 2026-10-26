
"""
Shoe Warehouse Stock Manager

This program reads shoe information from inventory.txt.
Stores each shoe as a Shoe object inside a list and provides a menu to:
- View all shoes in inventory
- Add a new shoe to inventory
- Restock the shoe with the lowest quantity
- Search for a shoe by its code (SKU)
- Show the total value of every item (cost * quantity)
- Show the shoe with the highest quantity (on sale)
"""

class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        """
        Create a new Shoe object and store its information.

        Parameters:
            country: The country where the shoe is stored.
            code: The shoe's unique stock code.
            product: The name of the shoe.
            cost: The cost of one shoe.
            quantity: How many shoes are in stock.
        """
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        """
        Get the cost of this shoe.

        Returns:
            The cost of the shoe.
        """
        # Return the cost of this shoe.
        return self.cost

    def get_quantity(self):
        """
        Get the quantity of this shoe in stock.

        Returns:
            The number of shoes currently in stock.
        """
        # Return how many of this shoe are in stock.
        return self.quantity

    def __str__(self):
        """
        Create a readable description of the shoe.

        Returns:
            A string showing the country, code, product,
            cost and quantity of the shoe.
        """
        # Return a readable string describing this shoe.
        return (
            "Country:  {}\n".format(self.country)
            + "Code:     {}\n".format(self.code)
            + "Product:  {}\n".format(self.product)
            + "Cost:     R{:.2f}\n".format(self.cost)
            + "Quantity: {}".format(self.quantity)
        )


# Every Shoe object created gets stored in this list.
shoe_list = []

# The data file used to read and save shoe information.
FILE_NAME = "inventory.txt"


def read_shoes_data():
    """
    Read the shoe information from inventory.txt.

    Skip the first line because it contains the headings.
    Create a Shoe object for each shoe and add it to list.
    Display an error message if the file empty, cannot be found
    or if a cost or quantity is not a valid number.
    """
    # Clear the list to prevent duplicate entries when reloading.
    shoe_list.clear()

    try:
        with open(FILE_NAME, "r") as file:
            next(file, None)  # Skip the first line (column headings).

            for line in file:
                line = line.strip()

                # Ignore blank lines.
                if line == "":
                    continue

                # Each line contains Country, Code, Product, Cost, Quantity.
                parts = line.split(",")

                # Check if the line has the correct number of columns.
                if len(parts) != 5:
                    print(
                        "Skipping badly formatted line: {}".format(line)
                    )
                    continue

                country, code, product, cost, quantity = parts

                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)

        print(
            "Loaded {} shoes from {}.".format(
                len(shoe_list), FILE_NAME
            )
        )

    except FileNotFoundError:
        print(
            "Error: {} was not found in this folder.".format(FILE_NAME)
        )

    except ValueError:
        print(
            "Error: a cost or quantity in the file "
            "is not a valid number."
        )


def save_shoes_data():
    """
    Save all the shoe information to inventory.txt.

    Write the headings first and then save each shoe
    from shoe_list to the file.
    Display an error message if the file cannot be saved.
    """
    try:
        with open(FILE_NAME, "w") as file:
            # Write the column headings.
            file.write("Country,Code,Product,Cost,Quantity\n")

            for shoe in shoe_list:
                file.write(
                    "{},{},{},".format(
                        shoe.country, shoe.code, shoe.product
                    )
                    + "{},{}\n".format(
                        shoe.cost, shoe.quantity
                    )
                )

    except OSError:
        print("Error: the inventory file could not be written.")


def get_number(prompt, number_type):
    """
    Ask the user to enter a valid number.

    Keep asking until the user enters a number that is
    not negative.

    Parameters:
        prompt: The message shown when asking for a number.
        number_type: The type of number needed, int or float.

    Returns:
        The valid number entered by the user.
    """
    while True:
        try:
            value = number_type(input(prompt))

            if value < 0:
                print("Please enter a number that is 0 or more.")
                continue

            return value

        except ValueError:
            print("That is not a valid number. Please try again.")


def capture_shoes():
    """
    Allow the user to add a new shoe to the inventory.

    Ask for the country, code, product, cost and quantity.
    Create a new Shoe object and add it to shoe_list.
    Save the updated inventory to inventory.txt.
    """
    # Ask the user for new shoe information.
    print("\nCapture a new shoe")

    country = input("Country:  ").strip()
    code = input("Code:     ").strip().upper()
    product = input("Product:  ").strip()

    cost = get_number("Cost:     ", float)
    quantity = get_number("Quantity: ", int)

    # Create a new Shoe object and add it to the list.
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)

    # Save the updated inventory to the file.
    save_shoes_data()

    print(
        "\n{} ({}) has been added to the inventory.".format(
            product, code
        )
    )


def view_all():
    """
    Display all the shoes currently in the inventory.

    Go through shoe_list and print the information
    for each shoe using the __str__ method.
    Display a message if the list is empty.
    """
    # Print the details of every shoe in the list.
    if not shoe_list:
        print("The stock is empty. Load the inventory data first.")
        return

    print("\nALL SHOES")

    for shoe in shoe_list:
        print(shoe)
        print("=" * 25)


def re_stock():
    """
    Find the shoe with the lowest quantity in stock.

    Ask the user if they want to restock this shoe.
    If yes, ask how many shoes to add and update the quantity.
    Save the updated information to inventory.txt.
    """
    # Check which shoe has the lowest quantity.
    if not shoe_list:
        print(
            "The stock is empty. Load the inventory first "
            "- Choose Option 1 to Load!"
        )
        return

    lowest = shoe_list[0]

    for shoe in shoe_list:
        if shoe.get_quantity() < lowest.get_quantity():
            lowest = shoe

    print("\nShoe with the lowest stock")
    print(lowest)

    answer = input(
        "Do you want to restock this shoe? (y/n): "
    ).strip().lower()

    if answer == "y":
        extra = get_number(
            "How many would you like to add? ", int
        )

        # Add the new stock to the existing quantity.
        lowest.quantity += extra

        # Save the updated quantity to the inventory file.
        save_shoes_data()

        print(
            "{} now has {} in stock. "
            "Inventory has been updated.".format(
                lowest.product, lowest.quantity
            )
        )

    else:
        print("No changes made.")


def search_shoe():
    """
    Search for a shoe using its stock code.

    Ask the user to enter a shoe code and check
    each shoe in shoe_list for a matching code.

    Returns:
        The Shoe object if a matching code is found.
        None if the shoe cannot be found.
    """
    # Ask for a shoe code and return the matching Shoe object.
    code = input(
        "\nEnter the shoe code to search for: "
    ).strip().upper()

    for shoe in shoe_list:
        if shoe.code == code:
            return shoe

    return None


def value_per_item():
    """
    Calculate and display the total stock value of each shoe.

    Multiply the cost by the quantity for every shoe.
    Display the shoe code, product name and total value
    in columns that are easy to read.
    """
    # Print the total stock value of every shoe.
    if not shoe_list:
        print(
            "The stock is empty. Load the inventory first "
            "- Choose Option 1 to Load!"
        )
        return

    print("\nSTOCK VALUE PER ITEM")
    print("-" * 54)

    # Print column headings.
    print("{:<12} {:<25} {:>15}".format(
        "CODE", "PRODUCT", "VALUE"
    ))

    print("-" * 54)

    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()

        # Format the currency before aligning it.
        formatted_value = "R{:.2f}".format(value)

        print("{:<12} {:<25} {:>15}".format(
            shoe.code, shoe.product, formatted_value
        ))

    print("-" * 54)


def highest_qty():
    """
    Find the shoe with the highest quantity in stock.

    Compare the quantities of all shoes in shoe_list.
    Display the shoe with the highest quantity
    and show that this shoe is on sale.
    """
    # Find the shoe with the highest quantity and show it on sale.
    if not shoe_list:
        print(
            "The stock is empty. Load the inventory first "
            "- Choose Option 1 to Load!"
        )
        return

    # Similar to re_stock(), but find the highest quantity.
    highest = shoe_list[0]

    for shoe in shoe_list:
        if shoe.get_quantity() > highest.get_quantity():
            highest = shoe

    print("\nON SALE: This shoe has the most stock!")
    print(highest)


# Main menu.
def main():
    """
    Start the warehouse stock management program.

    Load the shoe information from inventory.txt.
    Display the main menu and allow the user to choose
    which function they want to use.
    Keep displaying the menu until the user chooses to exit.
    """
    # Load inventory data when the program starts.
    read_shoes_data()

    # Display the menu until the user chooses to exit.
    while True:
        print(
            "\nNIKE WAREHOUSE MENU:\n"
            "1 - Reload shoes from file\n"
            "2 - Capture a new shoe\n"
            "3 - View all shoes\n"
            "4 - Restock the lowest-quantity shoe\n"
            "5 - Search for a shoe by code\n"
            "6 - Show value per item\n"
            "7 - Show the highest-quantity shoe (on sale)\n"
            "0 - Exit"
        )

        choice = input("Choose an option: ").strip()

        if choice == "1":
            read_shoes_data()

        elif choice == "2":
            capture_shoes()

        elif choice == "3":
            view_all()

        elif choice == "4":
            re_stock()

        elif choice == "5":
            found = search_shoe()

            if found is None:
                print("No shoe with that code was found.")

            else:
                print("\nShoe found")
                print(found)

        elif choice == "6":
            value_per_item()

        elif choice == "7":
            highest_qty()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print(
                "That is not a valid option. "
                "Please choose 0 to 7."
            )


main()
