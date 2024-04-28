import json
import os
import tabulate

password = "pass123"


# This function just makes it easier to get a value from a dictionary
def getKey(object, key):
    return object[key]


# Splitting an array into chunks to paginate the logs (option 5)
def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i : i + chunk_size]


# The manager for the JSON File
class Inventory:
    def __init__(self, path):
        self.path = path
        self.db = self._getDB()

        """The default data"""

    def _getDB(self):
        """fetches the db"""
        with open(self.path, "r") as openfile:
            db = json.load(openfile)
            return self.readyDB(db)

    def readyDB(self, existingData):
        """
        Check if it needs to initiate the Database
        """
        if existingData == {}:
            with open(self.path, "w") as f:
                rawData = {
                    "woodTypes": ["redwood", "birch", "oak", "mango", "acacia"],
                    "oak": {"qty": 5000, "price": 3500},
                    "redwood": {"qty": 3000, "price": 5500},
                    "birch": {"qty": 6000, "price": 2500},
                    "mango": {"qty": 4500, "price": 3500},
                    "acacia": {"qty": 4000, "price": 4000},
                    "buyerInfo": [],
                    "supplierInfo": [],
                }
                json.dump(rawData, f, indent=2)
                return rawData
        else:
            return existingData

    # Rewrites data to json
    def updateDB(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    # Gets info about the wood (price, qty)
    def getWoodData(self, type):
        with open(self.path, "r") as f:
            db = json.load(f)
            qty, price = self.getKey(db, type)
            return qty, price

    def subtractWood(self, type, qty):
        if self.db[type]["qty"] > qty:
            self.db[type]["qty"] -= qty
            return True
        else:
            return False


# Manages the UI for the console
class ConsoleSystem:
    def __init__(self) -> None:
        pass

    def menu(self):
        print("Please type a number correlating to the choice you want to make!")
        print("1. View stock levels")
        print("2. Change price/quantity")
        print("3. Add an order from supplier")
        print("4. Add an order for buyer")
        print("5. View past logs")
        print("6. Calculate remaining revenue")
        print("7. Exit")
        print("\nType a number to enter your choice")

    def detailsMenu(self):
        print("Please type the number correlating to your choice!")
        print("1. Change the price")
        print("2. Change the quantity")
        print("3. Go back")
        print("\nType a number to enter your choice")

    def paginateMenu(self):
        print("Please type the number correlating to your choice!")
        print("1. Buyers")
        print("2. Suppliers")
        print("\nType a number to enter your choice")

    def clearConsole(self):
        """Simple 1 liner to clear console, makes it look prettier"""
        os.system("cls" if os.name == "nt" else "clear")


class User:
    """The class that handles verification. Not a practical one, unless the password is stored remotely."""

    def __init__(self):
        self.verified = False
        self.password = password

    def verify(self):
        """Verification of password"""
        while True:
            passw = input("Enter password: ")
            if passw == self.password:
                self.verified = True
                break
            else:
                print("Incorrect password!")


# Buyer Class ( not needed )
"""
class Order:
    # The class to manage orders. The type order will determine if it is a buyer or seller
    

    def __init__(
        self,
        orderType="buyer" or "supplier",
        name=str,
        type=str,
        qty=int,
        inv=Inventory,
        price=int,
    ):
        self.order = orderType
        self.name = name
        self.type = type
        self.qty = qty
        self.inventory = inv
        self.price = price

    def calcTotal(self):
        
        # Get the revenue generated
        
        qty, price = getKey(self.inventory, self.type)
        return price * self.qty

    def generateLog(self):
        # Get the revenue generated
        qty, price = getKey(self.inventory, self.type)
        return f"{self.order.upper()} | Name: {self.name} | Quantity: {self.qty} | Price($): {price}"

"""


class ModuleManager:
    def __init__(self, inv, console):
        self.inv = inv
        self.console = console

    def getStockLevels(self):
        """well shit."""
        object = self.inv.db
        types = getKey(object, "woodTypes")
        columns = ["Type", "Price ($)", "Quantity", "Value ($, million)"]
        tableData = []
        for type in types:
            obj = object[type]
            price = obj["price"]
            quantity = obj["qty"]
            tableData.append([type, price, quantity, (price * quantity) / 1000000])
        self.console.clearConsole()
        print(
            tabulate.tabulate(
                tableData, headers=columns, tablefmt="fancy_grid", numalign="center"
            )
        )
        print("\n\n\n")

    # change the details
    def changeDetails(self):
        self.console.clearConsole()
        self.console.detailsMenu()
        choiceType = "price"
        # Just verification checks.
        while True:
            choice = input()
            if choice.isdigit():
                if int(choice) <= 3 and int(choice) >= 1:
                    break
                else:
                    print("Enter a valid number!")
            else:
                print("Enter a valid number!")
        choice = int(choice)
        # choices
        if choice == 1:
            choiceType = "price"
        elif choice == 2:
            choiceType = "qty"
        elif choice == 3:
            # exit and go back
            return print("Going back...")
        print("Enter the type of wood you want to modify:")
        type = input()
        db = self.inv.db

        print(f"Enter your new quantity (Choice: {choiceType})")
        while True:
            value = input()
            if value.isdigit():
                if int(value) > 0:
                    break
                else:
                    pass
            else:
                print("That is not a number!")
        value = int(value)
        if type in db:
            db[type][choiceType] = value
            print(db)
            return self.inv.updateDB(db)
        else:
            return print(
                "\n\nAn unexpected error occured! Please check if you have the correct wood type!\n\n"
            )

    # My lord this took way too long

    def addOrderSupplier(self):
        self.console.clearConsole()
        print(
            "Please enter the supplier company name (Please ensure that there are no spelling errors)"
        )

        while True:
            name = input()
            if len(name.strip()) == 0:
                print("Name cannot be blank!")
            else:
                break

        print("Enter the type of wood they are selling")
        type = input()
        if type.lower() not in self.inv.db["woodTypes"]:
            return print("That wood type does not exist in our database!")

        print("Enter the quantiy of wood that they have sold")
        quantity = input()
        if not quantity.isdigit():
            return print("The quantity must be a number!")
        if int(quantity) < 0:
            return print("The quantity cannot be less than zero!")

        marketPrice = self.inv.db[type.lower()]["price"]
        print(f"Name: {name.capitalize()}")
        print(f"Wood Type: {type.lower().capitalize()}")
        print(f"Market price: {marketPrice}")
        print(f"Quantity: {quantity}")
        print("\n\nDo you confirm? (yes/no)")
        while True:
            flag = input()
            if flag == "yes" or flag == "no":
                break
            else:
                print("That is not a valid option")
        if flag == "yes":
            # newSupplier = Order("supplier", name, type.lower(), quantity, marketPrice)
            db = self.inv.db
            quantity = int(quantity)
            db["supplierInfo"].append(
                {
                    "type": "supplier",
                    "name": name,
                    "wood": type.lower(),
                    "quantity": quantity,
                    "price": marketPrice,
                }
            )
            db[type]["qty"] += quantity
            self.inv.updateDB(db)

            return print("Successfully added!")
        else:
            return print("Exiting this menu...")

    def addOrderBuyer(self):
        self.console.clearConsole()
        print(
            "Please enter the buyer company name (Please ensure that there are no spelling errors)"
        )

        while True:
            name = input()
            if len(name.strip()) == 0:
                print("Name cannot be blank!")
            else:
                break

        print("Enter the type of wood they are buying")
        type = input()
        if type.lower() not in self.inv.db["woodTypes"]:
            return print("That wood type does not exist in our database!")

        print("Enter the price of wood that they are buying at! Market price: ", self.inv.db[type.lower()]["price"])
        price = input()
        if not price.isdigit():
            return print("The price must be a number!")
        if int(price) < 0:
            return print("The price cannot be less than zero!")

        print("Enter the quantiy of wood that they have bought")
        quantity = input()
        if not quantity.isdigit():
            return print("The quantity must be a number!")
        if int(quantity) < 0:
            return print("The quantity cannot be less than zero!")

        print(f"Name: {name.capitalize()}")
        print(f"Wood Type: {type.lower().capitalize()}")
        print(f"Buying  Price: {price}")
        print(f"Quantity: {quantity}")
        print("\n\nDo you confirm? (yes/no)")
        while True:
            flag = input()
            if flag == "yes" or flag == "no":
                break
            else:
                print("That is not a valid option")
        if flag == "yes":
            # newBuyer = Order("buyer", name, type.lower(), quantity, self.inv)
            db = self.inv.db
            db["buyerInfo"].append(
                {
                    "type": "buyer",
                    "name": name,
                    "wood": type.lower(),
                    "quantity": quantity,
                    "price": price,
                }
            )
            db[type]["qty"] -= quantity
            self.inv.updateDB(db)
            return print("Successfully added!")
        else:
            return print("Exiting this menu...")

    def logsModule(self):
        db = self.inv.db
        logs = []
        self.console.paginateMenu()
        choice = input()

        if choice == "1":
            logs = db["buyerInfo"]
        elif choice == "2":
            logs = db["supplierInfo"]
        else:
            return print("Invalid option, exiting menu...\n\n")
        if len(logs) == 0:
            return print("The logs are empty.")
        chunks = list(split(logs, 10))
        index = 0
        self.console.clearConsole()
        print("----------------------LIST OF SUPPLIERS----------------------")
        for chunk in chunks[index]:
            print(
                f"{chunk['type']} | Name: {chunk['name']} | Price: {chunk['price']}$ per tonne | Qty: {chunk['quantity']} tonnes | Wood: {chunk['wood']}"
            )
        while True:
            print(
                f"\nPlease type which page you want to go to! There's {len(chunks)} page(s) in total.\nType -1 to exit!"
            )
            inp = input()
            if inp == "-1":
                return print("Exiting this menu...")
            else:
                if inp.isdigit():
                    if int(inp) > 0 and int(inp)-1 < len(chunks):
                        self.console.clearConsole()
                        index = int(inp)-1
                        for chunk in chunks[index]:

                            print(
                                f'{chunk["type"]} | Name: {chunk["name"]} | Price: {chunk["price"]}$ per tonne | Qty: {chunk["quantity"]} tonnes | Wood: {chunk["wood"]}'
                            )
                    else:
                        print("That page does not exist!")
                else:
                    print("That is not a number!")
    def generateRevenue(self):
        boughtValue = 0
        soldValue = 0
        for supplier in self.inv['db']['supplierInfo']:
            boughtValue += supplier['price']* supplier['quantity']
        for buyer in self.inv['db']['buyerInfo']:
            soldValue += buyer['price']* buyer['quantity']
        print("Value bought: ", boughtValue,"$")
        print("Value sold: ", soldValue,"$")
        print("Total Revenue remaining: ", soldValue-boughtValue,"$")
        return



# Main Class
def main():
    """--------------VARIABLES ---------------"""
    inventoryManager = Inventory("db.json")
    mainUser = User()
    consoleSystem = ConsoleSystem()
    modules = ModuleManager(inventoryManager, consoleSystem)
    exitCode = False
    """ --------------------------------------- """

    mainUser.verify()
    while not exitCode:
        if mainUser.verified:
            consoleSystem.menu()
            # Validates number
            while True:
                choice = input()
                if choice.isdigit():
                    if int(choice) < 8 and int(choice) > 0:
                        break
                    else:
                        print("Enter a valid number!")
                else:
                    print("Enter a valid number!")
        choice = int(choice)
        if choice == 1:
            """stockLevels Module"""
            modules.getStockLevels()
        elif choice == 2:
            modules.changeDetails()
        elif choice == 3:
            """"""
            modules.addOrderSupplier()
        elif choice == 4:
            """"""
            modules.addOrderBuyer()
        elif choice == 5:
            """"""
            modules.logsModule()
        elif choice == 6:
            """"""

        elif choice == 7:
            """Exit"""
            print("Exiting system...")
            exitCode = True


main()
