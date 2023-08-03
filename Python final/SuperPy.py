import csv
import os
from datetime import datetime, date, timedelta
import string
from gooey import Gooey, GooeyParser
from openpyxl import Workbook


ALPHABET = string.ascii_uppercase

workbook = Workbook()
sheet = workbook.active


PATH_TXT =os.path.join(os.getcwd(), os.path.basename('time.txt'))
time_file_exists = os.path.isfile(PATH_TXT)  

def create_time_file(time):
    """
    Creates a time file and provides options to set or reset the system date.

    Parameters:
        time (str): A string representing either a number between 1 to 9 or the word "reset".
        
    Returns:
        None

    If the input 'time' is "reset", the function resets the system date to the current live date
    and removes the time file if it exists.

    If the input 'time' is a valid number between 1 to 9, the function adds the specified number 
    of days to the current system date and stores the result in a time file. The time file
    preserves the number of days, so it can be used to set the system date later.

    If the input 'time' is neither a number between 1 to 9 nor "reset", it displays an error 
    message indicating invalid input and instructs the user to use valid options.

    Example:
        create_time_file("reset")
        # Output: Your system date has been reset to live date: <current_date>

        create_time_file("5")
        # Output: Your current system date is now: <current_date + 5 days>
    """
    if time == "reset":
        print(f"Your system date has been reseted to live date: {date.today()} ")
        os.remove(PATH_TXT)
    elif time in "1234567890":
        print(f"Your current system date is now: {date.today() + timedelta(days=int(int(time)))}")
        with open(PATH_TXT, "w",encoding="utf-8") as write_file:
            write_file.write(time)
    else:
        print("That is an invalid input, use 1234567890 or the word reset")
        
if time_file_exists:
    with open(PATH_TXT, "r", encoding="utf-8") as read_file:
        num = read_file.read()
        now = date.today() + timedelta(days=int(int(num)))
else:
    now = date.today()
yesterday = now - timedelta(days=1)
tomorrow = now + timedelta(days=1)

@Gooey(
    program_name='My Supermarkt APP',
    show_preview_warning=False,
    advanced=True,
    navigation='TABBED',
    header_bg_color="#f69c00",

    menu=[{'name': 'Help', 'items': [{'type': 'AboutDialog',
                                      'menuTitle': 'About',
                                      'name': 'My Supermarket APP',
                                      'description': 'This is a little summary on how to use this app, you have three main options: 1 Buy is where you can purchase items to add to your store, 2 Sell is where you can sell the same items to your costumers, 3 Reports is where you can get your reports on how your store is going',
                                      'version': '1.2.1',
                                      'copyright': '2022', }]}]
)
def parser_function():
    """
    Command-line argument parser for My Supermarket tool.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.

    Description:
        The function uses GooeyParser to create a user-friendly command-line interface for the My Supermarket tool.
        Users can choose from different departments [Buy, Sell, Stock, Search_Report] to perform specific actions
        related to managing the supermarket inventory.

    Usage Examples:
        - To add a product to the store inventory:
            $ python my_supermarket.py Buy -p "Product_Name" -q 100 -b 1.99 -e "2023-07-31"

        - To sell a product from the store inventory:
            $ python my_supermarket.py Sell -p "Product_Name" -q 50 -s 2.49

        - To check the products currently available in the store inventory:
            $ python my_supermarket.py Stock --print

        - To search through the inventory history and generate a report:
            $ python my_supermarket.py Search_Report -from "2023-07-01" -till "2023-07-31" -Department "Revenue" --Export

        - To advance the program's current date for future simulation:
            $ python my_supermarket.py Advance_time -a 10

        - To reset the program's current date to the live date:
            $ python my_supermarket.py Advance_time -a reset

    """
    parser = GooeyParser(
        description="Welcome to the My Supermarket, the tool to help you run your store")
    subparser = parser.add_subparsers(
        dest='command', description="Choose from the diferent departments [Buy , Sell , Stock , Search_Report]")

    buy_parser = subparser.add_parser('Buy')
    sell_parser = subparser.add_parser('Sell')
    stock_parser = subparser.add_parser("Stock")
    search_parser = subparser.add_parser("Search_Report")
    advance_time_parser = subparser.add_parser("Advance_time")


    #############################################################################
    buy_parser.add_argument('-p', '--Product', required=True, type=str,
                            help="Product that you would like to ADD to your store")


    buy_parser.add_argument('-q', '--Quantity', required=True, type=int,
                            help="How many would you like add?")

    buy_parser.add_argument('-b', '--Bought', required=True, type=float,
                            help="The price you BOUGHT the product for")
    buy_parser.add_argument(
        '-e', '--Expiration',  required=True, help="Expiration date on the Product e. g (yyyy-mm-dd)", widget="DateChooser")

    ##############################################################################
    sell_parser.add_argument('-p', '--Product',  required=True, type=str,
                                help="Which product that you have in your store that you wish to SEll")
    sell_parser.add_argument('-q', '--Quantity', required=True, type=int,
                            help="How many would you like sell?")
    sell_parser.add_argument(
        '-s', '--Sell', required=True, type=float, help="Price you wish to SELL the product for")


    #############################################################################
    stock_group = stock_parser.add_argument_group(
        "Stock", "Check the products you currently have in your store")
    stock_group.add_argument(
        '-p', '--print', action="store_true", default=False)


    #########################################################################
    search_group = search_parser.add_argument_group(
        "Search_Report", "Search though inventory history ")

    search_group.add_argument('-from', '--Start',
                                help="Type in the dates you would like to see your inventory report (supported formats .e .g yyyy-mm-dd, now, yesterday, 3days, 5weeks 2months) ", widget="DateChooser")
    search_group.add_argument('-till', '--End',
                                help="Type in the dates you would like to see your inventory report (supported formats .e .g yyyy-mm-dd, now, yesterday, 3days, 5weeks 2months)", widget="DateChooser")
    search_group.add_argument('Department', choices=(
        "Inventory", "Revenue", "Profit", "Waste"), help="You have to pick wich report you would like to see")
    search_group.add_argument('-export', '--Export', action="store_true",  help="If you would like to export your report to an EXCEL sheet")
    #########################################################################
    advance_time_parser.add_argument('-a', '--Advance', help="You can change the current date, use this flag, to simulate action in the future, use the number of days in the future that you would like to change the current date in the program, or use the, reset, keyword to reset to original time ")
    
    args = parser.parse_args()
    return args


CSV_PATH = os.path.join(os.getcwd(), os.path.basename('bought.csv'))
bought_file_exists = os.path.isfile(CSV_PATH)

CSV_SELL_PATH = os.path.join(os.getcwd(), os.path.basename("sold.csv"))
sell_file_exists = os.path.isfile(CSV_SELL_PATH)

class SuperPy:
    """
    SuperPy - A small system to help manage the backend for a webstore or physical store.

    This class provides essential functions for managing the store's inventory, selling items, and generating reports.

    Class Attributes:
        sold_field_names (List[str]): The field names for the "sold" CSV file.
        bought_field_names (List[str]): The field names for the "bought" CSV file.

    Class Methods:
        incre(count) -> int: Static method to increment a count.
        open_read_bought() -> List[Dict]: Read and return the contents of the "bought" CSV file.
        open_read_sold() -> List[Dict]: Read and return the contents of the "sold" CSV file.
        check_lowest_ex(product, reader) -> int: Find the lowest number of days to product expiration in the "bought" CSV file.
        check_time(time) -> datetime.date: Convert the input time string to a valid datetime.date object.
        add_value(start, end, reader, r) -> float: Calculate the total value of products in the "bought" or "sold" CSV file.
        check_expired_products(reader) -> None: Update the "bought" CSV file to mark expired products.
        print_stock_or_waste(variable) -> None: Print products that are in stock or expired/wasted.
        check_same_product(product, quant, bought, expiration, key, price, reader) -> List[bool, int]: Check if a product with the same details exists in the "bought" or "sold" CSV file.
        bought_writer(reader) -> None: Write the updated contents of the "bought" CSV file.
        sold_writer(reader) -> None: Write the updated contents of the "sold" CSV file.
    """
    sold_field_names = ["ID", "Product","Quantity","Sold_price", "Sold_date",
                        "Expiration"]
    bought_field_names = ["ID", "Product","Quantity" , "Bought_price", "Bought_date",
                            "Expiration", "InStock"]
    @staticmethod
    def incre(count):
        """
        Increment the given count by 1.

        Parameters:
            count (int): The count to be incremented.

        Returns:
            int: The incremented count.
        """
        count += 1
        return count

    @staticmethod
    def open_read_bought():
        """
        Read and parse the 'bought.csv' file and return its content as a list of dictionaries.

        Returns:
            list: A list containing dictionaries, each representing a row in the 'bought.csv' file.
        """
        with open('bought.csv', 'r', newline="", encoding="utf-8") as output:
            csv_reader = csv.DictReader(output)
            copy_bought_reader = [line for line in csv_reader]

            return copy_bought_reader

    @staticmethod
    def open_read_sold():
        """
        Read and parse the 'sold.csv' file and return its content as a list of dictionaries.

        Returns:
            list: A list containing dictionaries, each representing a row in the 'sold.csv' file.
        """
        with open('sold.csv', 'r', newline="", encoding="utf-8") as sold_read:
            csv_sell_reader = csv.DictReader(sold_read)
            copy_sold_reader = [line for line in csv_sell_reader]
            return copy_sold_reader

    @staticmethod
    def check_lowest_ex(product, reader):
        """
        Find the lowest number of days until expiration for a given product in the inventory.

        Parameters:
            product (str): The name of the product to check for expiration.
            reader (list): A list of dictionaries representing the inventory.

        Returns:
            int: The lowest number of days until expiration for the given product.
        """

    @staticmethod
    def check_time(time):
        """
        Convert a time string into a corresponding date.

        Parameters:
            time (str): A string representing a time, e.g., 'now', 'yesterday', '2weeks', '3days', etc.

        Returns:
            datetime.date: The date corresponding to the input time string.
        """

    @staticmethod
    def add_value(start, end, reader, r):
        """
        Calculate the total value of products sold or bought within a given date range.

        Parameters:
            start (str): The start date of the range in the format 'yyyy-mm-dd'.
            end (str or None): The end date of the range in the format 'yyyy-mm-dd' or None.
            reader (list): A list of dictionaries representing the inventory or sold products.
            r (str): Either 'sold' or 'bought' to determine the type of transactions to consider.

        Returns:
            float: The total value of products sold or bought within the specified date range.
        """

    @staticmethod
    def check_expired_products(reader):
        """
        Check and mark expired products in the inventory.

        Parameters:
            reader (list): A list of dictionaries representing the inventory.

        Returns:
            None
        """

    @staticmethod
    def print_stock_or_waste(variable):
        """
        Print the inventory items marked as 'InStock' or 'Expired'.

        Parameters:
            variable (str): The value to filter the inventory items. Either 'True' for 'InStock' or 'Expired' for expired items.

        Returns:
            None
        """

    @staticmethod
    def check_same_product(product, quant, bought, expiration, key, price, reader):
        """
        Check if a product with specific details exists in the inventory and update its quantity if found.

        Parameters:
            product (str): The name of the product to check.
            quant (int): The quantity of the product to be added.
            bought (float): The price the product was bought for.
            expiration (str): The expiration date of the product in the format 'yyyy-mm-dd'.
            key (str): Either 'bought' or 'sold' to determine which file to update.
            price (str): Either 'Bought_price' or 'Sold_price' to access the appropriate price.
            reader (list): A list of dictionaries representing the inventory or sold products.

        Returns:
            list: A list containing two elements. The first element indicates if the product was found, and the second element is the last ID in the file (for writing new rows).
        """

    @staticmethod
    def bought_writer(reader):
        """
        Write the updated inventory to the 'bought.csv' file.

        Parameters:
            reader (list): A list of dictionaries representing the inventory.

        Returns:
            None
        """

    @staticmethod
    def sold_writer(reader):
        """
        Write the updated sold products to the 'sold.csv' file.

        Parameters:
            reader (list): A list of dictionaries representing the sold products.

        Returns:
            None
        """
        day_list = list()

        expiration_list = [line["Expiration"]
                            for line in reader if product == line["Product"] and line['InStock'] == "True"]
        
        if len(expiration_list) == 0:
            return print(f"Sorry! but you dont have anymore: {product}s in your inventory")

        for c_d in expiration_list: 
            # function to determine lowest expiration date
            # loop over each expiration date
            expiration_date = datetime.strptime(
                c_d, "%Y-%m-%d").date()
            amount_days = expiration_date - now

            # see amount of days till product is expired
            
            if int(amount_days.days) > 0:
                day_list.append(int(amount_days.days))
            
            lowest = min(day_list)

        return lowest
        writer = csv.DictWriter(
        open('sold.csv', 'w', newline=''), fieldnames=SuperPy.sold_field_names) #update bought file
        writer.writeheader()
        for line in reader:
            writer.writerow(line) 
    
# ####################################################################################################################################

class Buy(SuperPy):
    """
    Buy - Class for adding products to the store inventory.

    This class handles the process of adding new products to the store inventory.

    Args:
        product (str): The name of the product to be added.
        quantity (int): The quantity of the product to be added.
        bought (float): The price at which the product was bought.
        expiration (str): The expiration date of the product in the format "yyyy-mm-dd".

    Methods:
        add_inventory() -> None: Add the product to the store inventory.
    """
    def __init__(self, product, quantity,  bought, expiration):
        lower_product = product.lower()
        self.product = lower_product
        self.quantity = quantity
        self.bought = bought
        self.expiration = expiration

    def add_inventory(self):
        try:

            with open('bought.csv', 'a', newline="", encoding="utf-8") as add_input:
                csv_writer = csv.DictWriter(
                    add_input, fieldnames=SuperPy.bought_field_names)
                
                csv_reader = SuperPy.open_read_bought()
                if not bought_file_exists:
                    id = 1
                    csv_writer.writeheader()
                    csv_writer.writerow(
                        {"ID": id, 'Product': self.product, 'Quantity':self.quantity, 'Bought_price': self.bought, "Bought_date": now, 'Expiration': self.expiration, 'InStock': True})
                
                elif bought_file_exists:
                    key = "bought"
                    price = 'Bought_price'
                    result = SuperPy.check_same_product(self.product, self.quantity, self.bought, self.expiration, key,price, csv_reader)
                    
                    if result[0]:
                        
                        id = result[1]
                        csv_writer.writerow(
                        {"ID": SuperPy.incre(id), 'Product': self.product, 'Quantity':self.quantity, 'Bought_price': self.bought, "Bought_date": now, 'Expiration': self.expiration, 'InStock': True})


                    
        except Exception as e:
            print(e)
################################################################################################################################

class Sell(SuperPy):
    """
    Sell - Class for selling products from the store inventory.

    This class handles the process of selling products from the store inventory.

    Args:
        product (str): The name of the product to be sold.
        quantity (int): The quantity of the product to be sold.
        sold (float): The price at which the product is sold.

    Methods:
        sell_products() -> None: Sell the specified quantity of the product from the store inventory.
    """
    def __init__(self, product, quantity, sold):
        lower_product = product.lower()
        self.product = lower_product
        self.quantity = quantity
        self.sold = sold

    def sell_products(self):
        try:
            with open('sold.csv', 'a', newline="") as sold_input:
                csv_sell_writer = csv.DictWriter(
                    sold_input, fieldnames=SuperPy.sold_field_names)


                copy_bought_reader = SuperPy.open_read_bought()
                lowest = SuperPy.check_lowest_ex( #closest to expire
                        self.product, copy_bought_reader)

                if sell_file_exists:
                    csv_sell_reader = SuperPy.open_read_sold()
                    for line in csv_sell_reader:     # to get the ID number
                        c = line["ID"]
                        id = int(c)
                else:
                    id = 1
                
                if (bought_file_exists and self.product in  [p for element in copy_bought_reader for p in element.values()] ):      # check bought file exists and make sure that the item that we want to sell is in our inventory

                    condition = True # condition is True till the correct quantity was added to the sell file
                    
                    
                    for line in copy_bought_reader: # Here we will start iterating over the bought file to find the products that are closest to expire

                        expiration = line.get("Expiration") 
                        current_ex = datetime.strptime(
                            expiration, "%Y-%m-%d").date()
                        current_num = current_ex - now  # find out how many days miising till expiration of product on current line
                        
                        if int(current_num.days) > 0:  # check if the item is expired
                            correct_num = int(current_num.days)
                        else:
                            line["InStock"] = "Expired"

                        quant = int(self.quantity)

                        while condition:  # function that will count down quantity till 0
                            copy_bought_reader = SuperPy.open_read_bought()
                            for inner_line in copy_bought_reader:
                                
                                low = SuperPy.check_lowest_ex(
                                self.product, copy_bought_reader)

                                line_quant = int(inner_line["Quantity"])
                                
                                expiration = inner_line.get("Expiration")
                                current_ex = datetime.strptime(
                                    expiration, "%Y-%m-%d").date()
                                inner_current_num = current_ex - now
                                
                                
                                if int(current_num.days) > 0:  # check if the item is expired
                                    inner_current_num = int(current_num.days)
                                else:
                                    inner_line["InStock"] = "Expired"

                                SuperPy.bought_writer(copy_bought_reader)

                                if low == inner_current_num and self.product == inner_line['Product'] and inner_line["InStock"] == "True":
                                    
                                    if condition:

                                        if quant > line_quant:
                                            quant = quant - line_quant
                                            inner_line["Quantity"] = line_quant - line_quant

                                        else:
                                            x = quant
                                            quant = quant - quant
                                            inner_line['Quantity'] = line_quant - x

                                    if inner_line["Quantity"] == 0:
                                        inner_line["InStock"] = False
                
                                    if quant == 0:
                                        condition = False


                                    SuperPy.bought_writer(copy_bought_reader)   
                                  
                        if lowest == correct_num and self.product == line['Product']: #grab the product with the closest expiration date
                            
                            if not sell_file_exists:  # if sold file is not created yet
                                id = 1
                                if line["Quantity"] == 0:
                                    line["InStock"] = False

                                csv_sell_writer.writeheader()
                                csv_sell_writer.writerow(
                                    {"ID": id, 'Product': self.product, 'Quantity':self.quantity,
                                        'Sold_price': self.sold, "Sold_date": now, 'Expiration': expiration}
                                )
                                print("Item sold")
                                break # just to make sure it only runs once
                            if sell_file_exists:
                                sold_csv_reader = SuperPy.open_read_sold()
                                key = "sold"
                                price = 'Sold_price'
                                sell_result = SuperPy.check_same_product(self.product, self.quantity, self.sold, expiration, key,price, sold_csv_reader)
                                if sell_result[0]:

                                    id = sell_result[1]

                                    if line["Quantity"] == 0:
                                        line["InStock"] = False

                                    csv_sell_writer.writerow(
                                        {"ID": SuperPy.incre(id), 'Product': self.product, 'Quantity':self.quantity,
                                            'Sold_price': self.sold, "Sold_date": now, 'Expiration': expiration}
                                    )
                                    print("Item sold")
                                    break

                else:
                    
                    print("Your inventory file was not created, or is empty")
                    print(f"Or you dont have {self.product} in your inventory, please make sure you are spelling the Product correctly")


            SuperPy.bought_writer(copy_bought_reader)
            

        except Exception as e:
            print(e)


#################################################################################################################

class Report(SuperPy):
    """
    Report - Class for generating inventory, revenue, and profit reports.

    This class handles the generation of different types of reports based on the specified parameters.

    Args:
        sector (str): The type of report to be generated ("Inventory", "Revenue", or "Profit").
        sta_dat (str): The start date for the report in the format "yyyy-mm-dd".
        end_dat (str): The end date for the report in the format "yyyy-mm-dd".
        ex (bool): If True, the report will be exported to an Excel file.

    Methods:
        records() -> None: Generate the specified report based on the provided parameters.
    """
    def __init__(self, sector, sta_dat, end_dat, ex):
        self.sector = sector
        self.sta_dat = sta_dat
        self.end_dat = end_dat
        self.ex = ex

    def records(self):
        

        try:
            copy_bought_reader = SuperPy.open_read_bought()
            copy_sold_reader = SuperPy.open_read_sold()

            SuperPy.check_expired_products(copy_bought_reader)

            
            
            time_str = "{} {}".format(self.sta_dat," till " + self.end_dat if self.end_dat is not None else"")
            key_list = []
            if self.sector == "Inventory":
                table = Table(title="Inventory")
                for line in copy_bought_reader:
                    key_list.extend(line.keys())
                    for key , letter in zip(key_list, ALPHABET[:len(key_list)]):
                        table.add_column(key)
                        sheet[letter + "1"] = key
                    break
                
                row = 2
                for line in copy_bought_reader:
                    current_date = datetime.strptime(
                        line["Bought_date"], "%Y-%m-%d").date()

                    if self.end_dat is None:
                        the_date = SuperPy.check_time(self.sta_dat)
                        if the_date == current_date:
                            table.add_row("%s"%line["ID"],"%s"%line["Product"],"%s"%line["Quantity"],"%s"%line["Bought_price"],"%s"%line["Bought_date"],"%s"%line["Expiration"],"%s"%line["InStock"])
                            
                            for key ,letter in zip(key_list , ALPHABET[:len(key_list)]): # write eache row to the excell file

                                sheet[letter + str(row)] = line[key]
                        row +=1

                    if self.end_dat is not None:

                        stadate = self.sta_dat
                        endate = self.end_dat

                        start_date = datetime.strptime(
                            stadate, "%Y-%m-%d").date()

                        end_date = datetime.strptime(
                            endate, "%Y-%m-%d").date()

                        if start_date <= current_date and end_date >= current_date:
                            table.add_row("%s"%line["ID"],"%s"%line["Product"],"%s"%line["Quantity"],"%s"%line["Bought_price"],"%s"%line["Bought_date"],"%s"%line["Expiration"],"%s"%line["InStock"])

                            for key ,letter in zip(key_list , ALPHABET[:len(key_list)]): # write eache row to the excell file

                                sheet[letter + str(row)] = line[key]
                        row +=1
                
                
                console = Console()
                console.print(table)        
                if self.ex:
                    workbook.save(filename="inventory_rep.xlsx")
            
            elif self.sector == "Revenue":# have to see how to get the last cell in excel
                table = Table(title="Revenue")

                for line in copy_sold_reader:
                    key_list.extend(line.keys())
                    for key , letter in zip(key_list, ALPHABET[:len(key_list)]):
                        table.add_column(key)
                        sheet[letter + "1"] = key
                    break
                
                row = 2
                total_rev = SuperPy.add_value(
                    self.sta_dat, self.end_dat, copy_sold_reader, "sold")
                for line in copy_sold_reader:
                    for key ,letter in zip(key_list , ALPHABET[:len(key_list)]): # write eache row to the excell file

                        sheet[letter + str(row)] = line[key]
                    row +=1
                
                
                
                rev_str ="Your Revenue from "+time_str +f" was {total_rev}"
                print(rev_str)
                
                
                sheet["A" + str(row +1)] = rev_str
                
                
                if self.ex:
                    workbook.save(filename="Revenue_rep.xlsx")

            elif self.sector == "Profit":
                total_rev = SuperPy.add_value(
                    self.sta_dat, self.end_dat, copy_sold_reader, "sold")
                total_spent = SuperPy.add_value(
                    self.sta_dat, self.end_dat, copy_bought_reader, "bought")
                profit = total_rev - total_spent

                print("Your Profit from "+time_str +f" was {profit}")
                
        except FileNotFoundError:
            print("You havent created your inventory file or your sold file yet")
            print("Your inventory is empty")


#################################################################################################################
def main():
    args = parser_function()

    if args.command == "Buy":
        Store = Buy(args.Product, args.Quantity, args.Bought, args.Expiration)
        Store.add_inventory()
        print(f"OK, {args.Quantity} {args.Product} added to your inventory")
    elif args.command == "Sell":
        Store = Sell(args.Product,args.Quantity, args.Sell)
        Store.sell_products()

    elif args.command == "Stock":
        if args.print:
            SuperPy.print_stock_or_waste("True")
    elif args.command == "Search_Report":
        if args.Department == "Waste":
            SuperPy.print_stock_or_waste("Expired")

        else:
            Store = Report(args.Department, args.Start, args.End, args.Export)
            Store.records()
    elif args.command == "Advance_time":
        create_time_file(args.Advance)
        
       

if __name__ == '__main__':
    main()
